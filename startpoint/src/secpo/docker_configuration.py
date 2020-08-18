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
from re import search
from secpo.command_builder import CommandBuilder
from secpo.docker_images import ApparmorDockerImageFactory, \
    CustomDockerImageFactory, AbstractDockerImageFactory


class DirectoryToImageAndTools(Enum):
    CL = {'CL': 'ubuntu', 'os_tools': ['cppcheck'],
          'specific_tools': [],
          'other': ['WORKDIR /home/C/app',
                    'RUN cppcheck --enable=all '
                    '--suppress=missingIncludeSystem . 2> result.txt',
                    'RUN cat result.txt']}
    CPP = {'CPP': 'ubuntu', 'os_tools': ['cppcheck'],
           'specific_tools': [],
           'other': ['WORKDIR /home/C++/app',
                     'RUN cppcheck --enable=all '
                     '--suppress=missingIncludeSystem . 2> result.txt']}
    CS = {'CS': 'vagrant', 'os_tools': ['Roslynator'],
          'specific_tools': [],
          'other': [],}
    GO = {'GO': 'golang', 'os_tools': ['golang.org/x/lint/golint',
                                    'honnef.co/go/tools/cmd/staticcheck'],
          'specific_tools': [],
          'other': ['WORKDIR /go/src/app', 'COPY . .',
                    'RUN go get -d -v ./...', 'RUN go install -v ./...']}
    HASKELL = {'HASKELL': 'haskell', 'os_tools': ['pandoc pandoc-citeproc'],
               'specific_tools': [],
               'other': ['RUN cabal update', 'RUN cabal install hlint',
                         'ENTRYPOINT ["pandoc"]', 'WORKDIR /home/haskell/app']}
    JAVA = {'JAVA': 'java', 'os_tools': ["checkstyle", "gradle"],
            'specific_tools': [],
            'other': ["RUN gradle init", "COPY build.gradle .", "RUN gradlew build"]}
    JAVASCRIPT = {'JAVASCRIPT': 'node',
                  'os_tools': ['git gzip'],
                  'specific_tools': ["-g jshint --save-dev", "eslint --save-dev",
                                     "eslint-plugin-import --save-dev",
                                     "eslint-plugin-node --save-dev",
                                     "eslint-plugin-promise --save-dev",
                                     "eslint-plugin-standard --save-dev"],
                  'other': ["WORKDIR /home/javascript/app",
                            "RUN jshint . || true",
                            "RUN npx eslint . > result.txt || true"]}
    # http://jslint.com/
    KOTLIN = {'KOTLIN': 'codesignal/java:v5.6.1', 'os_tools': [],
              'specific_tools': [],
              'other': ['RUN KOTLIN_VERSION=1.3.61 \
                         KOTLIN_COMPILER_URL=https://github.com/JetBrains/'
                        'kotlin/releases/download/v${KOTLIN_VERSION}/' +
                        'kotlin-compiler-${KOTLIN_VERSION}.zip ; \
                         apt-get update \
                         && apt-get install -y --no-install-recommends zip unzip \
                         && wget $KOTLIN_COMPILER_URL -O /tmp/a.zip \
                         && unzip /tmp/a.zip -d /opt  \
                         && rm /tmp/a.zip \
                         && rm -rf /var/lib/apt/lists/*',
                        'ENV PATH $PATH:/opt/kotlinc/bin',
                        'RUN gradle init --dsl kotlin'
                        'COPY build.gradle .',
                        'RUN gradlew build']}
    LUA = {'LUA': 'ubuntu', 'os_tools': ['lua', 'luarocks'],
           'specific_tools': [],
           'other': ['RUN luarocks install luacheck', 'WORKDIR /home/lua/app']}
    OCAML = {'OCAML': 'ubuntu', 'os_tools': [],
             'specific_tools': [],
             'other': ['WORKDIR /home/ocaml/app']}
    OPENCL = {'OPENCL': 'ubuntu', 'os_tools': [],
              'specific_tools': [],
              'other': ['WORKDIR /home/opencl/app']}
    PHP = {'PHP': 'php', 'os_tools': ['zip', 'unzip', 'libzip-dev', 'git'],
           'specific_tools': [('phpstan/phpstan', '^0.12.37'), 'phan/phan'],
           'other': ['RUN curl -sS https://getcomposer.org/installer | php -- '
                     '--install-dir=/usr/local/bin --filename=composer',
                     'WORKDIR /home/php/app',
                     'RUN php /usr/local/bin/composer install',
                     'RUN ./vendor/phan/phan/phan --init']}
    PROLOG = {'PROLOG': 'swipl', 'os_tools': [],
              'specific_tools': [],
              'other': []}
    PYTHON = {'PYTHON': 'python', 'os_tools': ['python2', 'py-pip', 'py3-pip'],
              'specific_tools': [],
              'other': ['WORKDIR /usr/src/app',
                        'COPY requirements.txt ./',
                        # 'RUN pip install --no-cache-dir -r requirements.txt',
                        # 'RUN pip install bandit jedi',
                        'RUN python2 -m ensurepip --default-pip',
                        'RUN pip2 install --no-cache-dir -r requirements.txt',
                        'RUN pip2 install bandit jedi',
                        'RUN python2 -m bandit -f html -o result2.html -r . || true',
                        'RUN bandit -f html -o result.html -r . || true']}
    RL = {'RL': 'ubuntu', 'os_tools': [],
          'specific_tools': [],
          'other': ['WORKDIR /home/r/app']}
    RUBY = {'RUBY': 'ruby', 'os_tools': [],
            'specific_tools': ['brakeman', 'reek'],
            'other': ['# throw errors if Gemfile has been modified since Gemfile.lock',
                      # 'RUN bundle config --global frozen 1',
                      'WORKDIR /usr/src/app', 'COPY Gemfile ./',
                      'RUN bundle install',
                      # 'RUN brakeman --color -o result.html -o result.json',
                      'RUN reek --help',
                      'RUN reek -t -f html > result.html']}
    RUST = {'RUST': 'rust', 'os_tools': [],
            'specific_tools': [],
            'other': ['WORKDIR /usr/src/rust/app', 'COPY . .',
                      'RUN cargo install --path .',
                      "RUN curl --proto '=https' --tlsv1.2 "
                      "-sSf https://sh.rustup.rs | sh",
                      "RUN rustup update",
                      "RUN rustup component add clippy",
                      "RUN cargo clippy",
                      "RUN cargo install cargo-fix",
                      ]}
    SCALA = {'SCALA': 'ubuntu', 'os_tools': ['-y scala'],
             'specific_tools': [],
             'other': ['WORKDIR /home/scala/app']}
    SMALLTALK = {'SMALLTALK': 'codesignal/ubuntu-base:v5.6', 'os_tools': [],
                 'specific_tools': [],
                 'other': ['RUN apt-get update \
                            && apt-get install -y --no-install-recommends gnu-smalltalk \
                            && rm -rf /var/lib/apt/lists/*',
                           'WORKDIR /home/smalltalk/app']}
    SQL = {'SQL': 'ubuntu', 'os_tools': ['ruby', 'gem'],
           'specific_tools': [],
           'other': ['RUN wget https://github.com/jarulraj/sqlcheck/releases/download/v1.2/sqlcheck-x86_64.deb',
                     'RUN dpkg -i sqlcheck-x86_64.deb',
                     'RUN gem install sqlint']}
    SHELL = {'SHELL': 'bash', 'os_tools': ['shellcheck'],
             'specific_tools': [],
             'other': []}


class AbstractDockerSecurity(metaclass=ABCMeta):
    """
    Abstract Docker configuration class which consists of 4 parts.
    """
    CPP = 'C++'
    CS = 'C#'
    OS_TOOLS = 'os_tools'
    SPECIFIC_TOOLS = 'specific_tools'
    OTHER_CMD = 'other'
    WORKDIR = 'WORKDIR '

    @abstractmethod
    def __init__(self):
        self.enum_directory = None
        self.image = None
        self.os_tools = None
        self.specific_tools = None
        self.other_commands = None
        self.docker_workdir = None

    def convert_directory_to_image(self, prog_language):
        dict_values = DirectoryToImageAndTools[prog_language].value
        self.image = dict_values[prog_language]
        if isinstance(dict_values[self.OS_TOOLS], list):
            self.os_tools = dict_values[self.OS_TOOLS]
        if isinstance(dict_values[self.SPECIFIC_TOOLS], list):
            self.specific_tools = dict_values[self.SPECIFIC_TOOLS]
        if isinstance(dict_values[self.OTHER_CMD], list):
            self.other_commands = dict_values[self.OTHER_CMD]

        # Parse working directory for concrete image_factory
        pattern = "(?<=" + self.WORKDIR + ").*$"
        self.docker_workdir = [search(pattern, cmd).group(0)
                               for cmd in self.other_commands
                               if self.WORKDIR in cmd][0]

    @abstractmethod
    def create_image_factory(self, prog_language):
        """
        Creates image for dockerfile configuration. It is expected
        that image is without security issues.
        :return: Concrete realization of class:`AbstractDockerImage`.
        :rtype: class:`AbstractDockerImage`
        """
        self.convert_directory_to_image(prog_language)

    @abstractmethod
    def create_toolset(self, package_manager, program_package_installer=None,
                       os_tools=None, specific_tools=None, other_commands=None):
        """
        Creates unique toolset for one docker configuration purposes.

        :param package_manager: Package manager is tool that is used
                                for particular OS distribution to install
                                prerequisite tools.
        :param program_package_installer: Package installer for specific
                                          programming language. Not all of the
                                          programming languages contains
                                          such installer.
        :param os_tools: list of tools that are required to run OS configuration.
        :type os_tools: list
        :param specific_tools: list of tools that are specific for OS familly
                               or package manager for programming language.
        :type specific_tools: list
        :param other_commands: Other commands that are part of
                               configuration of virtual environment.
        :return: tools: Concrete realization of class:`AbstractToolset`
        """
        pass


class SimpleSecurity(AbstractDockerSecurity):
    """
    Implement operations of docker configuration to create simple security config.
    """
    ALLOWED_OS = ['ubuntu', 'python', 'ruby', 'haskell', 'sql', 'java', 'go',
                  'php', 'node']
    PHP = 'PHP'
    JAVASCRIPT = 'JAVASCRIPT'
    PHP_VERSION = '7.4-cli'
    MAINLINE = 'mainline'

    def __init__(self):
        super(SimpleSecurity, self).__init__()

    def create_image_factory(self, prog_language):
        super(SimpleSecurity, self).create_image_factory(prog_language)
        image_factory = CustomDockerImageFactory(self.docker_workdir)
        if self.PHP in prog_language:
            image_factory.create_image(self.image, self.ALLOWED_OS,
                                       self.PHP_VERSION)
        # elif self.JAVASCRIPT in prog_language:
        #     image_factory.create_image(self.image, self.ALLOWED_OS,
        #                                self.MAINLINE)
        else:
            image_factory.create_image(self.image, self.ALLOWED_OS)
        return image_factory

    def create_toolset(self, package_manager, program_package_installer=None,
                       os_tools=None, specific_tools=None, other_commands=None):
        if not os_tools:
            os_tools = self.os_tools
        if not specific_tools:
            specific_tools = self.specific_tools
        if not other_commands:
            other_commands = self.other_commands
        return GeneralToolset(package_manager, program_package_installer,
                              os_tools, specific_tools, other_commands)


class CustomizedSecurity(AbstractDockerSecurity):
    """
    Customized security contains customized classes of seccomp and apparmor
    profiles along with general toolset.
    """
    ALLOWED_OS = ['ubuntu']

    def __init__(self):
        super(CustomizedSecurity, self).__init__()

    def create_image_factory(self, prog_language):
        super(CustomizedSecurity, self).create_image_factory(prog_language)
        image_factory = ApparmorDockerImageFactory(self.docker_workdir)
        image_factory.create_image(self.image, self.ALLOWED_OS)
        return image_factory

    def create_toolset(self, package_manager, program_package_installer=None,
                       os_tools=None, specific_tools=None, other_commands=None):
        return GeneralToolset(package_manager, program_package_installer,
                              os_tools, specific_tools, other_commands)


class AbstractToolset(metaclass=ABCMeta):
    """
    Interface used to create unique toolset.
    """
    RUN = 'RUN'
    COPY = 'COPY'
    INSTALL = 'install'
    UPDATE = 'update'
    YES = '-y'
    RECOMMENDS = '--no-install-recommends'
    APT_GET_CLEAN_REGISTRY = 'clean && rm -rf /var/lib/apt/lists/*'
    APK_ADD = 'add'
    APK_CLEAN_REGISTRY = '--no-cache'
    NPM = 'npm'

    @abstractmethod
    def __init__(self, package_manager, program_package_installer, os_tools,
                 specific_tools, other_commands):
        """ Initialize with list of tools """
        self._package_manager = package_manager
        self._program_package_installer = program_package_installer
        self._os_tools = []
        self._specific_tools = []
        if isinstance(os_tools, (list, itertools.chain)):
            self._os_tools = os_tools
        if isinstance(specific_tools, (list, itertools.chain)):
            self._specific_tools = specific_tools
        self._other_commands = other_commands
        self.first_tool = []

    def __add__(self, other):
        self._os_tools.append(other)

    def __iter__(self):
        if isinstance(self._os_tools, itertools.chain):
            self.first_tool = self._os_tools
        elif len(self._os_tools) > 0:
            self.first_tool = iter(self._os_tools)
        return self

    def __next__(self):
        return next(self.first_tool)

    @property
    def specific_tools(self):
        return self._specific_tools

    @abstractmethod
    def specify_tools(self, tools_type):
        """
        Function is used in order to overwrite existing tools that were
        initially constructed.
        """
        pass

    def _update_packages(self):
        command = CommandBuilder()
        if AbstractDockerImageFactory.APTGET in self._package_manager:
            command = CommandBuilder(self.RUN, self._package_manager,
                                     self.UPDATE, self.YES)
        if AbstractDockerImageFactory.APK in self._package_manager:
            command = CommandBuilder(self.RUN, self._package_manager,
                                     self.UPDATE)
        return command

    def _clean_registry(self):
        command = CommandBuilder()
        if AbstractDockerImageFactory.APTGET in self._package_manager:
            command += CommandBuilder(self.RUN, self._package_manager,
                                      self.APT_GET_CLEAN_REGISTRY)
        return command

    def _add_specific_tools(self):
        command = CommandBuilder()
        if self._program_package_installer and \
           self.NPM in self._program_package_installer:
            for specific_tool in self._specific_tools:
                command += CommandBuilder(self.RUN, self.NPM, self.INSTALL,
                                          specific_tool)
        return command

    def _add_other_commands(self):
        command = CommandBuilder()
        if self._other_commands:
            for other_cmd in self._other_commands:
                if AbstractDockerSecurity.WORKDIR in other_cmd:
                    # Add workdir before copying
                    command += other_cmd
                    command += CommandBuilder(self.COPY, '. .')
                else:
                    command += CommandBuilder(other_cmd)
        return command

    @abstractmethod
    def install(self) -> CommandBuilder:
        """
        Specify concrete steps how to install particular tools. Which tools
        should be when executed and pass additional arguments to them.
        """
        # Update packages
        command = self._update_packages()
        if self._os_tools:
            install_cmd = ""
            if AbstractDockerImageFactory.APTGET in self._package_manager:
                install_cmd = CommandBuilder(self.RUN, self._package_manager,
                                             self.INSTALL, self.YES,
                                             self.RECOMMENDS)
            elif AbstractDockerImageFactory.APK in self._package_manager:
                install_cmd = CommandBuilder(self.RUN, self._package_manager,
                                             self.APK_ADD, self.APK_CLEAN_REGISTRY)
            for tool in self:
                install_cmd += tool
            command += install_cmd
        # Clean registry
        command += self._clean_registry()
        # Add specific tools only when they are not part of the file
        command += self._add_specific_tools()
        # Add other commands
        command += self._add_other_commands()
        return command


class GeneralToolset(AbstractToolset):
    """
    Toolset used for single run of specific docker container.
    """
    def __init__(self, package_manager, program_package_installer, os_tools,
                 specific_tools, other_commands):
        super(GeneralToolset, self).__init__(package_manager,
                                             program_package_installer, os_tools,
                                             specific_tools, other_commands)

    def specify_tools(self, tools_type):
        pass

    def install(self):
        return super(GeneralToolset, self).install()


class ConfigCreator:
    LOW = "low"
    HIGH = "high"
    POSIX = 'posix'
    WINDOWS = 'nt'

    def __init__(self, path_conf, image=None,
                 security_level=None):
        # Create configuration file for docker and vagrant
        self.path_components = path_conf.path_components
        self.images_enum = path_conf.images
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
        self.image_factory = {}
        self.profiles = {}
        self.dict_enum_directories = {}
        self.toolset = None

    def unroll_path(self):
        @wraps(self)
        def _setup_dockerfile(*args, **kwargs):
            config = args[0]
            dockerfile_location = []
            dockerfile_configuration = []
            # Reset image factory
            config.image_factory = {}
            for component in config.path_components.items():
                path = component[1][0]
                prog_language = component[0]
                # Append path of configuration
                dockerfile_location.append(path)
                # Create desired operation system image factory based on
                # programming language input.
                config.image_factory[path.name] = config.docker_conf\
                    .create_image_factory(prog_language)
                # Add enum directory for tagging docker machines.
                config.dict_enum_directories[path.name] = config.docker_conf\
                    .enum_directory
                # Create list of profiles that will be applied in built image.
                config.profiles[path.name] = []
                config.profiles[path.name].append(config.
                                                  image_factory[path.name]
                                                  .create_seccomp_profile())
                config.profiles[path.name].append(config.
                                                  image_factory[path.name]
                                                  .create_mac_profile())
                # todo: create toolset for each configuration
                # todo: this could be singleton class
                config.toolset = config.docker_conf.create_toolset(
                        config.image_factory[path.name].package_manager,
                        config.image_factory[path.name].program_package_installer)
                config.docker_conf.default_tools = None
                # Add configuration commands to path
                dockerfile_configuration.append(self(*args, **kwargs))
            # Iterate over all created profiles and create and parse
            # profiles when they are present.
            if config.profiles:
                for prog_language in config.profiles.values():
                    for profile in prog_language:
                        # Skip profiles when not specified
                        if not profile:
                            continue
                        profile.create_profile()
                        profile.parse_profile()
            return zip(dockerfile_location, dockerfile_configuration)
        return _setup_dockerfile

    # Go trough every dockerfile in requested input
    @unroll_path
    def create_configuration(self):
        commands = CommandBuilder()
        image_name = list(self.image_factory.keys())[-1]
        commands += self.image_factory[image_name].image
        commands += self.toolset.install()
        return commands, self.toolset
