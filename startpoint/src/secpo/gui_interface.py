# This module is created by Martin Vasko
# It contains simple GUI application that is intuitive and
# straight forward. It is expected to use GUI for one purpose task.
# However for users that are interested in complex testing the CLI
# interface provides simpler automation of testing.
# It is expected that running from GUI by pressing button takes long time.
import io
import os
import pathlib
import multiprocessing
import signal
import subprocess
import sys
import time
import threading

import PySide2
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton, QAction,
                               QFormLayout, QFileSystemModel, QTextBrowser,
                               QWidget, QFileDialog, QMenuBar,
                               QProgressDialog, QDialog, QHBoxLayout)
from PySide2.QtCore import Qt, QSortFilterProxyModel, QIdentityProxyModel, \
  QThread, QObject, QUrl
from PySide2.QtGui import QIcon, QKeySequence, QTextDocument
from secpo.path_operation import ProgramTypes
from secpo.run_facade import divide_chunks


class ProxyModel(QIdentityProxyModel):
    def flags(self, index):
        flags = super(ProxyModel, self).flags(index)
        if not self.sourceModel().isDir(index):
            flags &= ~Qt.ItemIsSelectable
            # or disable all files
            # flags &= ~Qt.ItemIsEnabled
        return flags


class DirFileFilterProxyModel(QSortFilterProxyModel):
    def filterAcceptsRow(self, source_row:int,
                         source_parent:PySide2.QtCore.QModelIndex) -> bool:
        file_model = QFileSystemModel(self.sourceModel())
        if (file_model and file_model.isDir(self.sourceModel()
                                                .index(source_row, 0,
                                                       source_parent))):
            return True
        if super(DirFileFilterProxyModel, self).filterAcceptsRow(source_row,
                                                                 source_parent):
            return True
        return False


class Worker(QObject):
    RED_COLOR = '\033[91m{}\033[00m'
    SUCCESSFUL = "Successfully built"
    DELETED_CONTAINERS = "Deleted Containers:"
    TOTAL_RECLAIMED_SPACE = "Total reclaimed space:"

    def __init__(self, parent, file_names, queues):
        super(Worker, self).__init__()
        self.manager = multiprocessing.Manager()
        self.steps = self.manager.Value('i', 0)
        self.parent_pipe, self.child_pipe = multiprocessing.Pipe()
        self.configuration = parent.configuration
        self.disable_logging = parent.disable_logging
        self.file_names = file_names
        self.parent = parent
        self.queues = queues
        self.result_filter = parent.result_filter

    def log_output_fill_queue(self, stdout, stderr):
        print(stdout.decode('utf-8'), end='', flush=True)
        # Show stderr only when present
        if stderr:
            print(self.RED_COLOR.format(stderr.decode('utf-8')),
                  end='', flush=True)
        self.steps.value += 1
        self.queues[0].put(self.steps)

    def fill_args(self, file):
        """ Fill arguments for CLI script

        :param file: input file/files that are examined.
        :return: Script arguments that are filled instead of user.
        """
        script_args = ['secpo', '--input', file]
        if self.disable_logging:
            script_args.append('--disable-logging')
        if self.result_filter:
            script_args.append('--result-filter')
        if self.configuration:
            script_args.append('--add-configuration')
        return script_args

    def _check_end(self, process):
        if not self.queues[1].empty():
            item = self.queues[1].get()
            if item == process.pid:
                if os.name == 'nt':
                    process.send_signal(signal.CTRL_C_EVENT)
                else:
                    process.send_signal(signal.SIGINT)
                return True
            else:
                # Return pid if it is not correct
                self.queues[1].put(process.pid)
        return False

    def create_process(self, file):
        # todo: do command line buffering using pexpect
        process = subprocess.Popen(self.fill_args(file),
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout = b''
        stderr = b''
        while True:
            if self._check_end(process):
                break
            # End of docker build
            if self.DELETED_CONTAINERS in stdout.decode('utf-8'):
                self.log_output_fill_queue(stdout, stderr)
            if self.TOTAL_RECLAIMED_SPACE in stdout.decode('utf-8'):
                process.wait()
                stdout, stderr = process.communicate()
                self.log_output_fill_queue(stdout, stderr)
                break
            stdout = process.stdout.readline()
            print(stdout.decode('utf-8'), end='', flush=True)
            if stdout:
                continue
            stderr = process.stderr.readline()
            print(self.RED_COLOR.format(stderr.decode('utf-8'),
                                        end='', flush=True))

    def run(self):
        # Run Sec&Po CLI on background
        tasks = []
        for file in self.file_names:
            process = multiprocessing.Process(target=self.create_process,
                                              args=(file, ))
            tasks.append(process)
        runnable_chunks = list(divide_chunks(tasks, self.parent.PROCESS_NUMBER))
        # Run all chunks one by one
        self.queues[0].put(self.steps)
        for chunk in runnable_chunks:
            self.parent.processes = chunk
            for process in chunk:
                process.start()
            for process in chunk:
                process.join()


class MyWidget(QWidget):
    MAX_SHOWN_LINES = 10
    PROCESS_NUMBER = 2
    STOP_THREADS = False
    # Files
    APP_DIR = 'app'
    HTML = '.html'
    XML = '.xml'
    TXT = '.txt'
    EXTENSIONS = [TXT, XML, HTML]

    def __init__(self):
        QWidget.__init__(self)
        # Configuration from CLI interface
        self.file_names = []
        self.disable_logging = False
        self.result_filter = None
        self.filters = []
        self.configuration = []
        # Internal subprocess attributes
        # Shared queues, first for steps and second for processes
        self.queues = None
        self.worker = None
        self.processes = []
        self.thread = None
        self.show_steps_thread = None
        self.web_views = []

        # Create Menu bar
        self.setWindowTitle("Sec&Po testing framework")
        self.main_menu = QMenuBar()
        self.file_menu = self.main_menu.addMenu("File")
        self.configure_menu = self.main_menu.addMenu("Configure")
        # Set actions
        file_actions = self.create_file_actions()
        for action in file_actions:
            self.file_menu.addAction(action)
        manage_actions = self.create_management_actions()
        for action in manage_actions:
            self.configure_menu.addAction(action)

        # Create main window
        self.selected_files = QLabel("Here will be printed some of the selected files")
        self.finish_button = QPushButton("&Run security and"
                                         " portability testing")
        # Connecting the signal
        self.finish_button.clicked.connect(self.run_testing)

        self.results_label = QLabel("No results")
        self.show_results_button = QPushButton("&Show results")
        self.show_results_button.clicked.connect(self.load_html_result)

        # Create file dialog
        self.file_dialog = QFileDialog(self)
        # fixme: debug for pycharm
        # self.file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        self.file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_filters = ["All files files (*)"]
        for value in ProgramTypes:
            file_filters.append(value.name + " files (")
            for program_filters in next(iter(value.value.values())):
                file_filters[len(file_filters) - 1] += "*" + program_filters\
                                                       + " "
            file_filters[len(file_filters) - 1] += ")"
        self.file_dialog.setNameFilters(file_filters)
        self.file_dialog.setViewMode(QFileDialog.Detail)
        # Add proxy model to change default behaviour or file selector
        # todo: does not work with files only directories.
        # However selecting of both must be overridden with own QFileDialog
        # proxy = ProxyModel(self.file_dialog)
        # self.file_dialog.setProxyModel(proxy)
        # Set layout of elements
        self._set_layout()

    def _set_layout(self):
        self.layout = QFormLayout()
        self.layout.setFormAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.layout.setVerticalSpacing(150)
        self.layout.setHorizontalSpacing(220)
        self.layout.setLabelAlignment(Qt.AlignRight)
        self.layout.addRow(self.main_menu)
        self.finish_button.setFixedSize(250, 65)
        self.layout.addRow(self.selected_files, self.finish_button)
        self.show_results_button.setFixedSize(250, 65)
        self.layout.addRow(self.results_label, self.show_results_button)
        self.setLayout(self.layout)

    def create_file_actions(self):
        openAct = QAction(QIcon("images/folder.png"), self.tr("&Open..."), self)
        openAct.setShortcuts(QKeySequence.Open)
        openAct.setStatusTip(self.tr("Open an existing file, "
                                     "files or directories"))
        openAct.triggered.connect(self.open)

        addFilter = QAction(QIcon("images/filter.png"), self.tr("&Add filter"),
                            self)
        # addFilter.setShortcuts()
        addFilter.setStatusTip(self.tr("Select filter files to apply "
                                       " result filtering"))
        addFilter.triggered.connect(self.add_filter)

        return [openAct, addFilter]

    def create_management_actions(self):
        manageAct = QAction(QIcon("images/settings.png"),
                            self.tr("&Manage filters"), self)
        # manageAct.setShortcuts(QKeySequence.Open)
        manageAct.setStatusTip(self.tr("Manage added filters"))
        manageAct.triggered.connect(self.manage_filters)

        docker_conf_action = QAction(QIcon("images/docker.png"),
                                     self.tr("&Docker"),
                                     self)
        # docker_conf_action.setShortcuts()
        docker_conf_action.setStatusTip(self.tr("Docker"))
        docker_conf_action.triggered.connect(self.docker_conf)

        apparmor_conf_action = QAction(QIcon("images/apparmor.png"),
                                       self.tr("&Apparmor"),
                                       self)
        # apparmor_conf_action.setShortcuts()
        apparmor_conf_action.setStatusTip(self.tr("Apparmor"))
        apparmor_conf_action.triggered.connect(self.apparmor_conf)

        seccomp_conf_action = QAction(QIcon("images/lock.png"),
                                      self.tr("&Seccomp"),
                                      self)
        # docker_conf_action.setShortcuts()
        seccomp_conf_action.setStatusTip(self.tr("Seccomp"))
        seccomp_conf_action.triggered.connect(self.seccomp_conf)

        return [manageAct, docker_conf_action,
                apparmor_conf_action, seccomp_conf_action]

    def add_filter(self):
        pass

    def manage_filters(self):
        output = subprocess.check_output(['secpo', '--list-filters'])
        dialog = QDialog(self)
        label = QLabel("Managed filters are: {}".format(output.decode('utf-8')))
        # dialog.set
        widgets = QWidget()

        layout = QHBoxLayout()
        layout.addWidget(dialog)
        layout.addWidget(label)

        widgets.setLayout(layout)
        widgets.show()
        dialog.exec()
        pass

    def docker_conf(self):
        pass

    def apparmor_conf(self):
        pass

    def seccomp_conf(self):
        pass

    def check_result_dir(self, file_name):
        result_dir = file_name.parent / self.APP_DIR
        if result_dir.exists():
            self.results_label.setText("Results present")

    def open(self):
        output = 'No files chosen!'
        self.file_names = []
        cnt = 0
        # fixme: running code from pycharm causes to not use
        # regular path system but symlinks
        # https://stackoverflow.com/questions/57646908/pyqt5-qfiledialog-is-not-returning-correct-paths-in-ubuntu
        if self.file_dialog.exec():
            self.file_names = self.file_dialog.selectedFiles()
            if self.file_names:
                output = ''
            for file_name in self.file_names:
                if cnt < self.MAX_SHOWN_LINES and file_name:
                    # Correct the path
                    absolute_path = pathlib.Path(file_name)
                    self.check_result_dir(absolute_path)
                    output += str(pathlib.Path(absolute_path.parts
                                               [len(absolute_path.parts) - 2])\
                                  / pathlib.Path(absolute_path.name)) + '\n'
                    cnt += 1
        self.selected_files.setText(output + "\n")

    def open_single_result_view(self, result_file):
        if isinstance(self.web_views[-1], QWebEngineView):
            self.web_views[-1].load(QUrl(result_file.as_uri()))
            self.web_views[-1].showMaximized()
        elif isinstance(self.web_views[-1], QTextBrowser):
            text_doc = QTextDocument()
            self.web_views[-1].setDocument(text_doc)
            self.web_views[-1].setSource(QUrl(result_file.as_uri(),
                                              QUrl.ParsingMode.TolerantMode))
            self.web_views[-1].show()

    def load_html_result(self):
        for file in self.file_names:
            root_dir = pathlib.Path(file).parent
            root_dir /= self.APP_DIR
            if root_dir.exists():
                for extension in self.EXTENSIONS:
                    result_files = root_dir.glob('**/*' + extension)
                    for result_file in result_files:
                        if extension == self.HTML or extension == self.XML:
                            self.web_views.append(QWebEngineView())
                        elif extension == self.TXT:
                            self.web_views.append(QTextBrowser())
                        self.open_single_result_view(result_file)

    def show_steps(self, progress):
        while True:
            time.sleep(0.5)
            if not self.queues[0].empty():
                steps = self.queues[0].get()
                progress.setValue(steps.value)
                if steps.value == len(self.file_names) * 2:
                    self.thread.quit()
                    self.check_result_dir(pathlib.Path(self.file_names[0]))
                    break
            if self.STOP_THREADS:
                break

    def remove_processes(self):
        self.processes = []

    def cancel(self):
        for process in self.processes:
            self.queues[1].put(process.pid)
            time.sleep(5)
        # Set stop threads to true to indicate end of program
        self.STOP_THREADS = True
        if self.thread:
            self.thread.quit()
        self.processes = []

    def run_testing(self):
        if not self.file_names:
            self.selected_files.setText(
                "No files were selected. Go to menu and "
                "select files to test.")
            return
        # Create new queues every run
        self.queues = [multiprocessing.Queue(maxsize=self.PROCESS_NUMBER),
                       multiprocessing.Queue(maxsize=self.PROCESS_NUMBER)]
        self.STOP_THREADS = False
        progress = QProgressDialog("Starting Docker and VMs",
                                   "Abort start", 0,
                                   len(self.file_names) * 2,
                                   self)
        progress.canceled.connect(self.cancel)
        progress.setWindowModality(Qt.WindowModal)

        # Create Qthread to show progress
        self.thread = QThread()
        self.worker = Worker(self, self.file_names, self.queues)
        self.worker.moveToThread(self.thread)
        # Custom signals connected to own functions for progress dialog
        self.show_steps_thread = threading.Thread(target=self.show_steps,
                                                  args=(progress, ))
        self.show_steps_thread.start()
        # Thread start and stop signals connected with slots
        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.remove_processes)
        # Start thread and force to show progress dialog
        self.thread.start()
        progress.forceShow()

    def closeEvent(self, event:PySide2.QtGui.QCloseEvent):
        event.ignore()
        super(MyWidget, self).closeEvent(event)
        # Indicate end of program
        if self.thread:
            self.thread.quit()
            self.thread.wait()
        for process in self.processes:
            if process:
                if os.name == 'nt':
                    process.send_signal(signal.CTRL_C_EVENT)
                else:
                    process.send_signal(signal.SIGINT)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.setFixedSize(900, 600)
    widget.show()

    sys.exit(app.exec_())
