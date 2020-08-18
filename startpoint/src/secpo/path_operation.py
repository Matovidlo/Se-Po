""" This module is created by Martin Vasko.
    Module is used to control path and perform necessary operations.
"""

import argparse
from defusedxml.ElementTree import parse
from enum import Enum
import os
from pathlib import Path
import shutil
import subprocess

from secpo.analysis_commands import RunAnalysisCommands
from secpo.template_build_files import kotlin_gradle, requirements_txt, \
    vagrant_config, Gemfile, composer_json, eslint


class ProgramTypes(Enum):
    """
    Class is enumeration of programing language with directory associated as key
    and value as suffix of files associated with programming language.
    """
    CL = {'extensions': ['.c', '.h'], 'tools': ['gcc']}
    CPP = {'extensions': ['.cpp', '.cxx', '.hpp', '.h', '.hxx'], 'tools': ['g++']}
    CS = {'extensions': ['.cs'], 'tools': ['csc']}
    GO = {'extensions': ['.go'], 'tools': ['go']}
    HASKELL = {'extensions': ['.hs'], 'tools': ['go']}
    JAVA = {'extensions': ['.java'], 'tools': ['java']}
    JAVASCRIPT = {'extensions': ['.js'], 'tools': ['firefox']}
    KOTLIN = {'extensions': ['.kt', '.kts'], 'tools': ['kotlin']}
    LUA = {'extensions': ['.lua'], 'tools': ['lua']}
    OCAML = {'extensions': ['.ml', '.mli', '.cmi'], 'tools': ['ocaml']}
    OPENCL = {'extensions': ['.cl', '.cxx', '.cpp'], 'tools': ['g++ -lOpenCL']}
    PHP = {'extensions': ['.php'], 'tools': ['php']}
    PROLOG = {'extensions': ['.pl'], 'tools': ['gprolog']}
    PYTHON = {'extensions': ['.py'], 'tools': ['python']}
    RL = {'extensions': ['.r'], 'tools': ['rscript']}
    RUBY = {'extensions': ['.rb'], 'tools': ['ruby']}
    RUST = {'extensions': ['.rs'], 'tools': ['rustc']}
    SCALA = {'extensions': ['.scala'], 'tools': ['scala']}
    SMALLTALK = {'extensions': ['.st'], 'tools': ['pharo']}
    SQL = {'extensions': ['.sql'], 'tools': ['sql']}


class PathArguments(argparse.ArgumentParser):
    def __init__(self):
        """ Initialize path arguments """
        super(PathArguments, self).__init__(prog="SE&PO testing framework",
                                            description="Security "
                                                        "and portability "
                                                        "testing framework "
                                                        "using "
                                                        "containerization and "
                                                        "vagrant boxes")
        self.add_argument('--input', nargs='+',
                          help='Input file/s or directory which contains '
                               'code files that can be evaluated.')
        self.add_argument('--disable-logging',
                          default=False, action='store_true',
                          help='When present dissables logging of executed'
                               'third party tools such as docker, vagrant etc.')
        self.add_argument('--result-filter', action='store_true',
                          help='Applies filter on results that are given '
                               'from program execution inside container or VM.')
        self.add_argument('--add-filter',
                          help='Adds filter to filters directory '
                               'and automatically apply them on execution.')
        self.add_argument('--list-filters', action='store_true',
                          help='Lists all result filters that are present '
                               'in filters directory.')
        self.add_argument('--add-configuration',
                          help='Apply custom security configuration in YAML.')
        # todo: program this functionality
        self.add_argument('--destroy-images', action='store_true',
                          help='Destroy downloaded docker '
                               'images right after execution.')
        self.add_argument('--destroy-boxes', action='store_true',
                          help='Destroy downloaded vagrant images '
                               'right after exection.')
        self.add_argument('--destroy-everything', action='store_true',
                          help='Destroys everyting that was downloaded stored '
                               'and installed as side process of deployment '
                               'of docker images and vagrant boxes.')
        self.args = self.parse_args()
        if self.args.input is None and self.args.list_filters is False:
            self.error("--input parameter required. No input file "
                       "was chosen.")


class PathOperation:
    # Used for ProgramType selection
    EXTENSIONS = 'extensions'
    TOOLS = 'tools'
    # Virtualization files
    DOCKERFILE = 'Dockerfile'
    VAGRANTFILE = 'Vagrantfile'
    VAGRANT_RESULT_DIR = 'vagrant_result'
    WELCOME_MESSAGE = "Welcome to portability testing using vagrant."
    VM_NAME = 'secpo'
    # Files
    HIDDEN_FILES = '.vagrant'
    SPECIAL_FILES = {'python': ['requirements.txt', '', requirements_txt],
                     'gradle': ['build.properties', '', kotlin_gradle],
                     'php': ['composer.json', '', composer_json],
                     'ruby': ['Gemfile', 'gem', Gemfile],
                     'node': ['.eslintrc.json', '', eslint]}
    FILTERS_FILE = Path('filters.xml')
    FILTER_DIR = Path('result_filters')
    # Destroy commands
    DOCKER_RM = 'docker rm -f {image_tag}'
    VAGRANT_RM = 'vagrant box remove -f {vagrant_box}'

    def __init__(self, command_line_args=None):
        """ Initalize PathOperation. """
        self.input_files = []
        self.input_directories = []
        # Directories where deployment of containers is executed
        self._path_components = dict()
        self._images = list()
        # Get current working directory based on this script location
        self.cwd = Path(os.getcwd())
        # Parsed command line arguments
        if command_line_args:
            args = command_line_args
        else:
            args = PathArguments().args
        # Assign all attributes
        self.list_filters = args.list_filters
        self._is_logging_enabled = not args.disable_logging
        self._filters = args.result_filter
        self._custom_configuration = args.add_configuration
        self._destroy_images = args.destroy_images
        self._destroy_boxes = args.destroy_boxes
        self._destroy_everything = args.destroy_everything
        # Parse input list of file/files/directories
        if args.input:
            for element in args.input:
                if Path(element).is_file():
                    self.input_files.append(Path(element))
                if Path(element).is_dir():
                    self.input_directories.append(Path(element))

    @property
    def path_components(self):
        """
        Return all path components consists of path, image and tools to compile
        or to interpret. The path is part of --input argument
        :return: All path components.
        """
        return self._path_components

    @property
    def images(self):
        return self._images

    @property
    def logging(self):
        """
        Return whether logging of docker and vagrant instances along with
        additional plugins are enabled or disabled.
        :return: Whether logging is enabled.
        """
        return self._is_logging_enabled

    @property
    def custom_configuration(self):
        """
        Returns whether user supplied configuration files in YAML format.
        :return: User configuration list.
        """
        return self._custom_configuration

    @property
    def filters(self):
        """
        Returns filters that are used for ResultRetriever.
        :return: All filters that are saved.
        """
        return self._filters

    def _categorize_files_input(self):
        """
        Categorize --input files based on file suffix. Add directories to
        path using PathLib.
        :return:
        """
        for file in self.input_files:
            for program_type in ProgramTypes:
                for extension in program_type.value[self.EXTENSIONS]:
                    if file.suffix == extension:
                        self._path_components[program_type.name] = \
                            [self.cwd / file.parent,
                             program_type.value[self.TOOLS]]

    def resolve_containers(self):
        """
        Resolve containers based on directories and files inside.
        :return:
        """
        # Input is only one file
        self._categorize_files_input()
        # Input is directory
        for directory in self.input_directories:
            # Iterate over enumeration of program types
            for program_type in ProgramTypes:
                # Iterate over dictionary that consists of path to folder
                # where Dockerfiles are present and values contains extensions
                # of program files that the program is looking for
                for extensions in program_type.value[self.EXTENSIONS]:
                    files_and_dirs = directory.glob('**/*' + extensions)
                    files = [x for x in files_and_dirs if x.is_file()]
                    if files:
                        for file in files:
                            if self.HIDDEN_FILES in file.parts:
                                files.remove(file)
                        # Add from current working directory path to
                        # concrete folder where are located virtual
                        # machines and docker containers prescription.
                        self._path_components[program_type.name] = \
                            [self.cwd / files[0].parent,
                             program_type.value[self.TOOLS]]
        if not self._path_components:
            print("No path was selected!")
            exit(1)

    def show_filters(self):
        """
        Show current added filters.
        """
        if not self._filters:
            print("No filters available!")
            return False
        for num, filtered in enumerate(self._filters):
            print("Applied result filter {}: {}".format(num, filtered))
        return True

    def add_filter(self):
        """
        Add filter to list of filters.
        """
        pass

    def load_filters(self):
        """
        Load all result filters that user supplied as argument --add_filter.
        :return: Success
        """
        if self.FILTERS_FILE.exists():
            et = parse(self.FILTERS_FILE)
            self._filters = et
        if self.FILTER_DIR.exists():
            files_and_dirs = self.FILTER_DIR.glob("**/*")
            files = [x for x in files_and_dirs if x.is_file()]
            for file in files:
                with open(file, 'r') as read_file:
                    data = read_file.read()
                    self._filters.append(data)
        return True

    def add_configuration(self):
        """
        Configuration YAML file is added, parsed and used as custom
        configuration.
        :return:
        """
        pass

    def create_configuration_files(self):
        """
        Create docker and Vagrant configuration files.
        """
        for directory in self._path_components.values():
            dockerfile = directory[0] / self.DOCKERFILE
            dockerfile.touch()
            vagrantfile = directory[0] / self.VAGRANTFILE
            vagrantfile.touch()
            try:
                vagrant_result_dir = directory[0] / self.VAGRANT_RESULT_DIR
                vagrant_result_dir.mkdir()
            except FileExistsError:
                pass

    def list_analysed_files(self, path):
        files = []
        file_filters = self.path_components.keys()
        for file_filter in file_filters:
            for extension in ProgramTypes[file_filter].value[self.EXTENSIONS]:
                files_and_dirs = path.glob("**/*" + extension)
                files = [x for x in files_and_dirs if x.is_file()]
        # Get all file names as single string line
        compilation_tools = [dir for dir in self.path_components.values()
                             if path is dir[0]][0][1]
        file_names = ""
        vagrant_cmd = ""
        for file in files:
            file_names += ' ' + file.name
            vagrant_pwd = './portability_testing/'
            vagrant_cmd += RunAnalysisCommands['VAGRANT_CMD'].value \
                .format(tool=compilation_tools[0], options='',
                        files=vagrant_pwd + file.name)
        # Create command from listed files, only if it exists in
        # analysis_commands.py file.
        for file_filter in file_filters:
            if file_filter in list(RunAnalysisCommands.__members__):
                commands = RunAnalysisCommands[file_filter].value\
                    .format(files=file_names)
                return commands, vagrant_cmd, compilation_tools
        return "", vagrant_cmd, compilation_tools

    def write_specific_package_file(self, command, path, tools):
        # fixme: try to do it in one if statement with always same
        # functionality
        out = [key for key in self.SPECIAL_FILES.keys() if key in str(command)]
        if out:
            out = out[0]
            special_file = path / self.SPECIAL_FILES.get(out)[0]
            tools = []
            if tools:
                for tool in tools.specific_tools:
                    # Remove last newline
                    if isinstance(tool, tuple):
                        tools.append("\t\t\"" + tool[0] + "\":\"" + tool[1]
                                        + "\",\n")
                    else:
                        tools.append(self.SPECIAL_FILES.get(out)[1] + " \'" + tool + "\'")
                    # todo:
                    # else:
                    #     packages.append("\t\t\"" + tool + "\":\"@dev\",\n")
                special_file.write_text(self.SPECIAL_FILES.get(out)[2]
                                        .format('\n\t'.join(tools)))
            else:
                special_file.write_text(self.SPECIAL_FILES.get(out)[2])

    def write_configuration(self, configuration):
        # Write docker configuration
        for path, config in configuration:
            command = config[0]
            analysed_files, vagrant_cmd, compilation_tools = \
                self.list_analysed_files(path)
            command += analysed_files
            tools = config[1]
            dockerfile = path / self.DOCKERFILE
            # Write all specific package files for particular
            # programming language
            self.write_specific_package_file(command, path, tools)
            with dockerfile.open('w') as write_file:
                write_file.write(str(command))
            # Check whether is written everything inside file correctly
            with dockerfile.open('r') as read_file:
                assert read_file.read() == str(command)
            # Write vagrantfile
            vagrantfile = path / self.VAGRANTFILE
            with vagrantfile.open('w') as write_file:
                vm_identifier = [identifier for identifier in
                                 self.path_components.keys()
                                 if
                                 path in self.path_components.get(identifier)][0]
                output = vagrant_config.format(msg=self.WELCOME_MESSAGE,
                                               sync_folder=str(path.resolve()),
                                               name=self.VM_NAME
                                                    + str(vm_identifier),
                                               tools=' '.join(compilation_tools),
                                               cmds=vagrant_cmd)
                write_file.write(output)

    def delete_configurations(self):
        """
        Delete configuration files after results retrieved.
        """
        for component in self._path_components.values():
            dockerfile = component[0] / self.DOCKERFILE
            if dockerfile.exists():
                dockerfile.unlink()
            vagrantfile = component[0] / self.VAGRANTFILE
            if vagrantfile.exists():
                vagrantfile.unlink()
            for value in self.SPECIAL_FILES.values():
                path = component[0] / value[0]
                if path.exists():
                    path.unlink()

    def delete_result_directory(self):
        for component in self.path_components:
            vagrant_result_dir = component[0] / self.VAGRANT_RESULT_DIR
            shutil.rmtree(str(vagrant_result_dir))

    def destroy_images(self, tags):
        if self._destroy_images:
            cmd = self.DOCKER_RM.format(' '.join(tags))
            process = subprocess.Popen(cmd.split(' '))
            process.wait()

    def destroy_boxes(self):
        if self._destroy_boxes:
            cmd = self.VAGRANT_RM.format('centos/7')
            process = subprocess.Popen(cmd.split(' '))
            process.wait()

    def destroy_everything(self, tags):
        if self._destroy_everything:
            self._destroy_images(tags)
            self._destroy_boxes()

