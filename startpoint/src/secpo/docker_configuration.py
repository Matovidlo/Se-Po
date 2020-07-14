""" This module is created by Martin Vasko.
    Docker configuration class is abstract factory of docker image with
    specified Seccomp Profile, Apparmor Profile (Ubuntu) SELinux
    Profile (Fedora) and set of tools.
"""

from abc import ABCMeta, abstractmethod
from enum import Enum
from functools import wraps
import itertools
import os
from secpo.command_builder import CommandBuilder
from secpo.docker_images import ApparmorDockerImageFactory, CustomDockerImageFactory


class DirectoryToImageAndTools(Enum):
    C = {'C': ['ubuntu', ['cppcheck']]}
    CPP = {'C++': ['ubuntu']}
    CS = {'C#': ['vagrant']}
    GO = {'Go': ['golang', 'WORKDIR /go/src/app', 'COPY . .',
                 'RUN go get -d -v ./...', 'RUN go install -v ./...']}
    HASKELL = {'Haskell': ['haskell',
                           'RUN stack install pandoc pandoc-citeproc',
                           'ENTRYPOINT ["pandoc"]']}
    JAVA = {'Java': ['java']}
    JAVASCRIPT = {'javascript': ['nginx']}
    KOTLIN = {'Kotlin': ['codesignal/java:v5.6.1', 'RUN KOTLIN_VERSION=1.3.61 \
                          KOTLIN_COMPILER_URL=https://github.com/JetBrains/'
                         'kotlin/releases/download/v${KOTLIN_VERSION}/' +
                         'kotlin-compiler-${KOTLIN_VERSION}.zip ; \
                           apt-get update \
                           && apt-get install -y --no-install-recommends zip unzip \
                           && wget $KOTLIN_COMPILER_URL -O /tmp/a.zip \
                           && unzip /tmp/a.zip -d /opt  \
                           && rm /tmp/a.zip \
                           && rm -rf /var/lib/apt/lists/*',
                         'ENV PATH $PATH:/opt/kotlinc/bin']}
    LUA = {'Lua': ['ubuntu']}
    OCAML = {'OCaml': ['ubuntu']}
    OPENCL = {'OpenCL': ['ubuntu']}
    PHP = {'PHP': ['PHP']}
    PROLOG = {'Prolog': ['swipl']}
    PYTHON = {'Python': ['python', 'WORKDIR /usr/src/app',
                         'COPY requirements.txt ./',
                         'RUN pip install --no-cache-dir -r requirements.txt']}
    R = {'R': ['ubuntu']}
    RUBY = {'Ruby': ['ruby', '# throw errors if Gemfile has been modified since Gemfile.lock',
                     'RUN bundle config --global frozen 1',
                     'WORKDIR /usr/src/app', 'COPY Gemfile Gemfile.lock ./',
                     'RUN bundle install']}
    RUST = {'Rust': ['rust', 'WORKDIR /usr/src/myapp', 'COPY . .',
                     ' RUN cargo install --path .']}
    SCALA = {'Scala': ['ubuntu', 'RUN apt-get install -y scala']}
    SMALLTALK = {'Smalltalk': ['codesignal/ubuntu-base:v5.6',
                 'RUN apt-get update \
                  && apt-get install -y --no-install-recommends gnu-smalltalk \
                  && rm -rf /var/lib/apt/lists/*']}
    SQL = {'SQL': ['mysql']}


class AbstractDockerConfiguration(metaclass=ABCMeta):
    """
    Abstract Docker configuration class which consists of 4 parts.
    """
    CPP = 'C++'
    CS = 'C#'

    @abstractmethod
    def __init__(self):
        self.directory = None
        self.image = None
        self.default_tools = None

    def convert_directory_to_image(self, directory):
        name = directory.name
        if name == self.CPP:
            name = 'CPP'
        elif name == self.CS:
            name = 'CS'
        self.directory = name
        self.image = DirectoryToImageAndTools[self.directory.upper()].value.\
            values()
        dict_values = list(self.image)
        if len(dict_values[0]) > 2:
            self.default_tools = dict_values[0][1:]
        elif len(dict_values[0]) == 2:
            self.default_tools = [dict_values[0][0]]
        self.image = (list(self.image)[0])[0]

    @abstractmethod
    def create_image(self, directory):
        """
        Creates image for dockerfile configuration. It is expected
        that image is without security issues.
        :return: Concrete realization of class:`AbstractDockerImage`.
        :rtype: class:`AbstractDockerImage`
        """
        self.convert_directory_to_image(directory)

    @abstractmethod
    def create_toolset(self, package_manager, tools=None):
        """
        Creates unique toolset for one docker configuration purposes.

        :param package_manager: Package manager is tool that is used
                                for particular OS distribution to install
                                prerequisite tools.
        :param tools: list of tools that are required to run configuration.
        :type tools: list
        :return: tools: Concrete realization of class:`AbstractToolset`
        """
        pass


class SimpleSecurity(AbstractDockerConfiguration):
    """
    Implement operations of docker configuration to create simple security config.
    """
    ALLOWED_OS = ['ubuntu', 'python', 'ruby', 'haskell', 'sql', 'java', 'go',
                  'php']

    def __init__(self):
        super(SimpleSecurity, self).__init__()

    def create_image(self, directory):
        super(SimpleSecurity, self).create_image(directory)
        image_factory = CustomDockerImageFactory()
        image_factory.create_image(self.image, self.ALLOWED_OS)
        return image_factory

    def create_toolset(self, package_manager, tools=None):
        if not tools:
            tools = self.default_tools
        return GeneralToolset(package_manager, tools)


class CustomizedSecurity(AbstractDockerConfiguration):
    """
    Customized security contains customized classes of seccomp and apparmor
    profiles along with general toolset.
    """
    def __init__(self):
        super(CustomizedSecurity, self).__init__()

    def create_image(self, operation_system):
        image_factory = ApparmorDockerImageFactory()
        image_factory.create_image(operation_system)
        return image_factory

    def create_toolset(self, package_manager, tools=None):
        return GeneralToolset(package_manager, tools)


class AbstractToolset(metaclass=ABCMeta):
    """
    Interface used to create unique toolset.
    """
    RUN = 'RUN'
    INSTALL = 'install'

    @abstractmethod
    def __init__(self, package_manager, tools):
        """ Initialize with list of tools """
        self._package_manager = package_manager
        self._tools = []
        if isinstance(tools, (list, itertools.chain)):
            self._tools = tools
        self.first_tool = []

    def __add__(self, other):
        self._tools.append(other)

    def __iter__(self):
        if isinstance(self._tools, itertools.chain):
            self.first_tool = self._tools
        elif len(self._tools) > 0:
            self.first_tool = iter(self._tools)
        return self

    def __next__(self):
        return next(self.first_tool)

    @abstractmethod
    def specify_tools(self):
        """
        Function is used in order to overwrite existing tools that were
        initially constructed.
        """
        pass

    @abstractmethod
    def install(self) -> CommandBuilder:
        """
        Specify concrete steps how to install particular tools. Which tools
        should be when executed and pass additional arguments to them.
        """
        if self._tools:
            command = CommandBuilder(self.RUN, self._package_manager,
                                     self.INSTALL)
            for tool in self:
                command += tool
            return command
        return CommandBuilder()


class GeneralToolset(AbstractToolset):
    """
    Toolset used for single run of specific docker container.
    """
    def __init__(self, package_manager, tools):
        super(GeneralToolset, self).__init__(package_manager, tools)

    def specify_tools(self):
        pass

    def install(self):
        return super(GeneralToolset, self).install()


class ConfigCreator:
    LOW = "low"
    HIGH = "high"
    POSIX = 'posix'
    WINDOWS = 'nt'

    def __init__(self, directories, image=None,
                 security_level=None):
        # Create configuration file for docker and vagrant
        self.directories = directories
        self.docker_conf = None
        if not image:
            if os.name is self.POSIX:
                self.base_image = 'ubuntu:latest'
            elif os.name is self.WINDOWS:
                self.base_image = 'windows:latest'
        if not security_level or security_level is self.LOW:
            self.docker_conf = SimpleSecurity()
        # elif security_level is self.HIGH:
        #     self.docker_conf = AdvancedSecurity(operation_system)
        else:
            self.docker_conf = CustomizedSecurity()
        # Set Image factory and toolset to None
        self.image_factory = None
        self.toolset = None

    def unroll_path(self):
        @wraps(self)
        def _setup_dockerfile(*args, **kwargs):
            config = args[0]
            dockerfile_location = []
            dockerfile_configuration = []
            for path in config.directories:
                # Append path of configuration
                dockerfile_location.append(path)
                # Create desired operation system image
                config.image_factory = config.docker_conf.create_image(path)
                # Create list of profiles that will be applied in built image
                config.profiles = list()
                config.profiles.append(config.image_factory.create_seccomp_profile())
                config.profiles.append(config.image_factory.create_mac_profile())
                # todo: create toolset for each configuration
                # todo: this could be singleton class
                config.toolset = config.docker_conf.create_toolset(
                        config.image_factory.package_manager)
                config.docker_conf.default_tools = None
                for profile in config.profiles:
                    # Skip profiles when not specified
                    if not profile:
                        continue
                    profile.create_profile()
                    profile.parse_profile()
                config.toolset.specify_tools()
                # Add configuration commands to path
                dockerfile_configuration.append(self(*args, **kwargs))
            return zip(dockerfile_location, dockerfile_configuration)
        return _setup_dockerfile

    # Go trough every dockerfile in requested input
    @unroll_path
    def create_configuration(self):
        commands = CommandBuilder()
        commands += self.image_factory.image
        commands += self.toolset.install()
        return commands
