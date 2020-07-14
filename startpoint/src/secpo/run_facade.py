""" This module is created by Martin Vasko.
    Output of the finished container or VM task is result.
    It is expected to retrieve this result by copying it back to host OS.
    On this result can be applied filter or highlighter because of
    possible false positives, true negatives etc.
"""
from secpo.docker_configuration import ConfigCreator
from secpo.path_operation import PathOperation
from secpo.result_retriever import ResultRetriever
from secpo.virtual_starter import VirtualStarter


class RunFacade:
    """
    Facade for configuration, running and result retrieving.
    Makes easier operation division and extendability and configurability.
    Delegate client requests to appropriate subsystem objects.
    """
    def __init__(self, operation_system=None):
        # Parse arguments from command line
        self._path_subsystem = PathOperation()
        self._path_subsystem.resolve_containers()
        # Touch docker configuration files
        self._path_subsystem.create_configuration_files()
        self._config_subsystem = ConfigCreator(self._path_subsystem.directories,
                                               operation_system)
        # Put all directories to virtualization starter
        self._run_subsystem = VirtualStarter(self._path_subsystem.directories)
        self._result_subsystem = ResultRetriever()

    def docker_operation(self):
        configuration = self._config_subsystem.create_configuration()
        self._path_subsystem.write_configuration(configuration)
        self._run_subsystem.deploy_containers()
        self._path_subsystem.delete_configurations()
        self._result_subsystem.retrieve()

    def vagrant_operation(self):
        self._run_subsystem.create_boxes()
        self._result_subsystem.retrieve()

    def operation(self):
        self.docker_operation()
        self.vagrant_operation()


def console_main():
    # Put command line arguments to Facade
    # Run docker and vagrant
    facade = RunFacade()
    facade.docker_operation()
    facade.vagrant_operation()


if __name__ == '__main__':
    # Put command line arguments to Facade
    # Run docker and vagrant
    facade = RunFacade()
    facade.docker_operation()
    facade.vagrant_operation()
