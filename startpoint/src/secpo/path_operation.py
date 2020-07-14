""" This module is created by Martin Vasko.
    Module is used to control path and perform necessary operations.
"""

import argparse
import os
from enum import Enum
from pathlib import Path



class ProgramTypes(Enum):
    """
    Class is enumeration of programing language with directory associated as key
    and value as suffix of files associated with programming language.
    """
    C = {'C': ['.c', '.h']}
    CPP = {'C++': ['.cpp', '.cxx', '.hpp', '.h', '.hxx']}
    CS = {'C#': ['.cs']}
    GO = {'Go': ['.go']}
    HASKELL = {'Haskell': ['.hs']}
    JAVA = {'Java': ['.java']}
    JAVASCRIPT = {'javascript': ['.js']}
    KOTLIN = {'Kotlin': ['.kt', '.kts']}
    LUA = {'Lua': ['.lua']}
    OCAML = {'OCaml': ['.ml', '.mli', '.cmi']}
    OPENCL = {'OpenCL': ['.cl', '.cxx', '.cpp']}
    PHP = {'PHP': ['.php']}
    PROLOG = {'Prolog': ['.pl']}
    PYTHON = {'Python': ['.py']}
    R = {'R': ['.r']}
    RUBY = {'Ruby': ['.rb']}
    RUST = {'Rust': ['.rs']}
    SCALA = {'Scala': ['.scala']}
    SMALLTALK = {'Smalltalk': ['.st']}
    SQL = {'SQL': ['.sql']}


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
        self.add_argument('--input', nargs='+', required=True,
                          help='Input file/s or directory which contains '
                               'code files that can be evaluated.')
        self.add_argument('--disable-logging',
                          default=False, action='store_true',
                          help='When present dissables logging of executed'
                               'third party tools such as docker, vagrant etc.')
        self.add_argument('--result-filter',
                          help='Applies filter on results that are given '
                               'from program execution inside container or VM.')
        self.add_argument('--add-filter',
                          help='Adds filter to filters directory '
                               'and automatically apply them on execution.')
        self.add_argument('--list-filters',
                          help='Lists all result filters that are present '
                               'in filters directory.')
        self.add_argument('--add-configuration',
                          help='Apply custom security configuration in YAML.')
        self.args = self.parse_args()


class PathOperation:
    DOCKERFILE = 'Dockerfile.tmp'

    def __init__(self, command_line_args=None):
        """ Initalize PathOperation. """
        self.input_files = []
        self.input_directories = []
        # Directories where deployment of containers is executed
        self._directories = set()
        # Get current working directory based on this script location
        self.cwd = Path(os.getcwd())
        # Parsed command line arguments
        if command_line_args:
            args = command_line_args
        else:
            args = PathArguments().args
        self._is_logging_enabled = not args.disable_logging
        self._filters = args.result_filter
        self._custom_configuration = args.add_configuration
        # Parse input list of file/files/directories
        for element in args.input:
            if Path(element).is_file():
                self.input_files.append(Path(element))
            if Path(element).is_dir():
                self.input_directories.append(Path(element))

    @property
    def directories(self):
        """
        Return all directories that are as part of --input argument
        :return: All directories.
        """
        return self._directories

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
                for path, value in program_type.value.items():
                    for extension in value:
                        if file.suffix in extension:
                            self._directories.add(self.cwd / file.parent)

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
                for path, value in program_type.value.items():
                    for extensions in value:
                        files_and_dirs = directory.glob('**/*' + extensions)
                        files = [x for x in files_and_dirs if x.is_file()]
                        if files:
                            # Add from current working directory path to
                            # concrete folder where are located virtual
                            # machines and docker containers prescription.
                            self._directories.add(self.cwd / files[0].parent)

    def show_filters(self):
        """
        Show current added filters.
        :return: List of result filters
        """
        pass

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
        pass

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
        for directory in self._directories:
            dockerfile = directory / self.DOCKERFILE
            dockerfile.touch()

    def write_configuration(self, configuration):
        for path, config in configuration:
            dockerfile = path / self.DOCKERFILE
            with dockerfile.open('w') as write_file:
                write_file.write(str(config))
            # Check whether is written everything inside file correctly
            with dockerfile.open('r') as read_file:
                print(read_file.read())

    def delete_configurations(self):
        """
        Delete configuration files after results retrieved.
        """
        for path in self.directories:
            dockerfile = path / self.DOCKERFILE
            dockerfile.unlink()
