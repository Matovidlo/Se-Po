""" This testing module is created by Martin Vasko.
    Conftest is file containing general functionality that is tested.
"""

import pytest
from secpo.docker_configuration import AbstractToolset
from secpo.command_builder import CommandBuilder
from secpo.docker_configuration import ApparmorDockerImageFactory, \
    SimpleSecurity, ConfigCreator
from secpo.path_operation import PathOperation
from secpo.virtual_starter import VirtualStarter
from secpo.result_retriever import ResultRetriever


class MockGeneralToolset(AbstractToolset):
    WORKDIR = 'WORKDIR'
    def __init__(self, package_manager, tools, other_commands):
        super(MockGeneralToolset, self).__init__(package_manager, tools,
                                                 other_commands)

    def specify_tools(self):
        """
        Function is used in order to overwrite existing tools that were
        initially constructed.
        """
        pass

    def install(self) -> CommandBuilder:
        """
        Specify concrete steps how to install particular tools. Which tools
        should be when executed and pass additional arguments to them.
        """
        command = CommandBuilder(self.RUN, self._package_manager, self.UPDATE)
        if self._tools:
            install_cmd = CommandBuilder(self.RUN, self._package_manager,
                                         self.INSTALL, self.RECOMMENDS)
            for tool in self:
                install_cmd += tool
            command += install_cmd
        # Clean registry
        command += CommandBuilder(self.RUN, self._package_manager,
                                  self.CLEAN_REGISTRY)
        if self._other_commands:
            for other_cmd in self._other_commands:
                if self.WORKDIR in other_cmd:
                    # Add workdir before copying
                    command += other_cmd
                    command += CommandBuilder(self.COPY, '. .')
                else:
                    command += other_cmd
        return command


class MockSimpleSecurity(SimpleSecurity):
    def create_toolset(self, package_manager, tools=None, other_commands=None):
        if not tools:
            tools = self.default_tools
        if not other_commands:
            other_commands = self.other_commands
        return MockGeneralToolset(package_manager, tools, other_commands)


class MockConfigCreator(ConfigCreator):
    def __init__(self, directories, image=None,
                 security_level=None):
        super(MockConfigCreator, self).__init__(directories, image,
                                                security_level)
        self.docker_conf = MockSimpleSecurity()


class MockVirtualStarter(VirtualStarter):
    def check_single_source(self, source):
        dockerfile = source / "Dockerfile"
        with open(dockerfile, 'r') as f:
            text = f.read()
        return source, text

    def check_code_files(self):
        path_list = []
        result = []
        for path in self.directories:
            path_list.append(path)
            dockerfile = path / "Dockerfile"
            with open(dockerfile, 'r') as f:
                text = f.read()
            result.append(text)
        return zip(path_list, result)


def pytest_addoption(parser):
    parser.addoption('--input', nargs='+', required=True,
                     help='Input file/s or directory which contains '
                          'code files that can be evaluated.')
    parser.addoption('--disable-logging',
                     default=False, action='store_true',
                     help='When present dissables logging of executed'
                          'third party tools such as docker, vagrant etc.')
    parser.addoption('--result-filter',
                     help='Applies filter on results that are given '
                          'from program execution inside container or VM.')
    parser.addoption('--add-filter',
                     help='Adds filter to filters directory '
                          'and automatically apply them on execution.')
    parser.addoption('--list-filters',
                     help='Lists all result filters that are present '
                          'in filters directory.')
    parser.addoption('--add-configuration',
                     help='Apply custom security configuration in YAML.')


@pytest.fixture(scope="class")
def configure(request):
    request.cls.path_conf = PathOperation(request.config.option)
    # Try to setup cwd as working directory for image factory
    request.cls.apparmor_factory = ApparmorDockerImageFactory(request.cls.
                                                              path_conf.cwd)
    request.cls.config_creator = ConfigCreator(request.cls.path_conf.directories)
    # Mock classes and override some of the functionality to lightweight tests
    request.cls.mock_config_creator = MockConfigCreator(request.cls.path_conf.
                                                        directories)


@pytest.fixture
def setup_configuration(request, configure, spawnu):
    """ Setup configuration files for docker and vagrant

    :param request: pytest request.
    :param configure: Configure fixture is prerequisite to instantiate classes.
    """
    path_conf = request.cls.path_conf
    path_conf.resolve_containers()
    path_conf.create_configuration_files()
    # Use mock config creator with overriden functionality.
    config_creator = request.cls.mock_config_creator
    config = config_creator.create_configuration()
    path_conf.write_configuration(config)
    request.cls.docker_spawn = spawnu
    request.cls.virtual_starter = MockVirtualStarter(path_conf.directories,
                                                     config_creator.
                                                     dict_enum_directories)


@pytest.fixture
def run_containers(request, setup_configuration):
    request.cls.virtual_starter.create_container()


@pytest.fixture(scope="class")
def run_vms(request, configure):
    path_conf = request.cls.path_conf
    request.cls.virtual_starter = VirtualStarter(path_conf.directories,
                                                 request.cls
                                                 .mock_config_creator
                                                 .dict_enum_directories)
    request.cls.virtual_starter.create_boxes()


@pytest.fixture(scope="class")
def remove_configuration(request, run_containers, run_vms):
    request.cls.path_conf.delete_configurations()


@pytest.fixture(scope="class")
def retrieve_results(request, run_containers, run_vms):
    request.cls.result_retriever = ResultRetriever()
    request.cls.result_retriever.retrieve()


@pytest.fixture
def setup_image(request):
    request.cls.apparmor_factory.create_image('ubuntu', ['ubuntu'])
    return request.cls.apparmor_factory
