""" This testing module is created by Martin Vasko.
    Conftest is file containing general functionality that is tested.
"""

import pytest
from secpo.docker_configuration import ApparmorDockerImageFactory
from secpo.path_operation import PathOperation
from secpo.virtual_starter import VirtualStarter
from secpo.result_retriever import ResultRetriever


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
    request.cls.apparmor_factory = ApparmorDockerImageFactory()


@pytest.fixture(scope="class")
def run_containers(request, configure):
    path_conf = request.cls.path_conf
    request.cls.virtual_starter = VirtualStarter(path_conf.directories)
    request.cls.virtual_starter.deploy_containers()


@pytest.fixture(scope="class")
def run_vms(request, configure):
    path_conf = request.cls.path_conf
    request.cls.virtual_starter = VirtualStarter(path_conf.directories)
    request.cls.virtual_starter.create_boxes()


@pytest.fixture(scope="class")
def retrieve_results(request, run_containers, run_vms):
    request.cls.result_retriever = ResultRetriever()
    request.cls.result_retriever.retrieve()


@pytest.fixture
def setup_image(request):
    request.cls.apparmor_factory.create_image('ubuntu', ['ubuntu'])
    return request.cls.apparmor_factory
