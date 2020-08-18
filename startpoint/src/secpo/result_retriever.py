""" This module is created by Martin Vasko.
    Output of the finished container or VM task is result.
    It is expected to retrieve this result by copying it back to host OS.
    On this result can be applied filter or highlighter because of
    possible false positives, true negatives etc.
"""

import functools
import os
from pathlib import Path
import subprocess

from secpo.path_operation import PathOperation


class ResultRetriever:
    DOCKER_CP = ['docker', 'cp', '{cont_id}:{src}', '{dst}']
    BRIDGE = 'bridge'
    DOCKER_DISCONNECT = ['docker', 'network', 'disconnect', '{network}',
                         '{cont_id}']
    # Vagrant commands
    VAGRANT_SSH = ['vagrant', 'ssh']
    VAGRANT_SCP = ['vagrant', 'scp', '{vm_name}:{src}', '{dst}']
    RESULT_FILE = 'result'
    SUFFIXES = ['.html', '.json', '.txt']

    def __init__(self, result_highlighter=None):
        """ Initialize """
        self._config_creator = None
        self.security_results = None
        self.portability_results = None
        if result_highlighter and isinstance(result_highlighter,
                                             ResultHighlighter):
            self.highlighter = result_highlighter
        else:
            self.highlighter = ResultHighlighter()

    @property
    def config_creator(self):
        return self._config_creator

    @config_creator.setter
    def config_creator(self, config):
        self._config_creator = config

    def _exec_cmd(self, cmd, input_cmds=None, **kwargs):
        process = subprocess.Popen(' '.join(cmd), stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, shell=True, **kwargs)
        stdout = b""
        stderr = b""
        while True:
            if input_cmds:
                for input_cmd in input_cmds:
                    stdout, stderr = process.communicate(input=input_cmd)
                    process.wait()
                    print(stdout.decode('utf-8'), end='')
                    print(stderr.decode('utf-8'), end='')
                    process = subprocess.Popen(' '.join(cmd), stdin=subprocess.PIPE,
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE, shell=True,
                                               **kwargs)
                input_cmds = []
            if (isinstance(process.returncode, int) and process.returncode >= 0) or \
                    stdout.decode('utf-8') or stderr.decode('utf-8'):
                try:
                    process.wait(timeout=5)
                    # stdout, stderr = process.communicate()
                    # print(stdout, end='')
                    # print(stderr, end='')
                    break
                except subprocess.TimeoutExpired:
                    process.kill()
                    break
            stdout, stderr = process.communicate()
            print(stdout)
            print(stderr)


    def _docker_disconnect(self, programming_language):
        cmd = self.DOCKER_DISCONNECT[:3]
        cmd.append(self.DOCKER_DISCONNECT[3].format(network=self.BRIDGE))
        cmd.append(self.DOCKER_DISCONNECT[4].format(cont_id=programming_language))
        self._exec_cmd(cmd)

    def retrieve_docker(self, path, programming_language):
        """
        Retrieve results from docker container. Copy files from execution of
        external tools.
        :return:
        """
        self._docker_disconnect(programming_language)
        cmd = self.DOCKER_CP[:2]
        cmd.append(self.DOCKER_CP[2].format(src=self._config_creator.docker_conf.
                                            docker_workdir,
                                            cont_id=programming_language))
        string_path = str(path).replace(' ', '\\ ')
        cmd.append(self.DOCKER_CP[3].format(dst=string_path))
        self._exec_cmd(cmd)

        result_path = Path(self._config_creator.docker_conf.docker_workdir)
        odd = path / result_path.name / self.RESULT_FILE
        for suffix in self.SUFFIXES:
            odd = odd.with_suffix(suffix)
            if odd.exists():
                with open(str(odd), 'r') as read_result:
                    print(read_result.read())
        # todo: copy only result file

    def retrieve_vagrant(self, path):
        """
        Retrieve result files of portability testing from vagrant environment.
        Copy all necessary files as output.
        :return:
        """
        env = os.environ.copy()
        env['VAGRANT_CWD'] = str(path)
        cmd = self.VAGRANT_SSH
        self._exec_cmd(cmd, [b'ls -al', b'pwd', b'exit'], env=env)
        cmd = self.VAGRANT_SCP[:2]
        # cmd.append(self.VAGRANT_SCP[2].format(vm_name=PathOperation.VM_NAME,
        #                                       src=)])

    def retrieve(self):
        """ Method should retrieve from both docker and vagrant the results.

        :return:
        """
        # fixme: does not work yet
        self.retrieve_docker()
        self.retrieve_vagrant()

    def perform_filter(self):
        """
        Perform filtering using ResultHighlighter and custom driven function.
        :return:
        """
        self.highlighter.highlight()


class ResultHighlighter:
    def __init__(self, user_function=None, *args, **kwargs):
        """ Initialize """
        self.user_function = self._config
        if user_function:
            self.user_function = user_function
        self.args = args
        self.kwargs = kwargs

    def _config(self, *args, **kwargs):
        """
        User driven function for pre configuration of highlighting.
        This function should be blank and custom user function
        should be implemented in order to highlight.
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def _highlight(self, *args, **kwargs):
        """
        Common highlight function of retrieved result.
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def highlight(self):
        @functools.wraps(self.user_function)
        def run(*args, **kwargs):
            self.user_function(*args, **kwargs)
            self._highlight(*args, **kwargs)
        return run(*self.args, **self.kwargs)


def my_highlight(config):
    print(config)
    pass


if __name__ == '__main__':
    highlighter = ResultHighlighter(my_highlight, ['file'])
    result = ResultRetriever(highlighter)
    result.perform_filter()