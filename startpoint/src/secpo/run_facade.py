""" This module is created by Martin Vasko.
    Output of the finished container or VM task is result.
    It is expected to retrieve this result by copying it back to host OS.
    On this result can be applied filter or highlighter because of
    possible false positives, true negatives etc.
"""
import asyncio
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
    NUM_OF_CONCURRENT_PROCESSES = 2
    PORTABLE_LANGUAGES = ['JAVASCRIPT', 'SHELL', 'CS', 'RUBY', 'SQL']

    def __init__(self, operation_system=None):
        # Parse arguments from command line
        self._path_subsystem = PathOperation()
        self._path_subsystem.resolve_containers()
        # Touch docker configuration files
        self._path_subsystem.create_configuration_files()
        self._config_subsystem = ConfigCreator(self._path_subsystem,
                                               operation_system)
        # Put all directories to virtualization starter
        self._run_subsystem = VirtualStarter(self._path_subsystem.path_components)
        self._result_subsystem = ResultRetriever()
        configuration = self._config_subsystem.create_configuration()
        self._path_subsystem.write_configuration(configuration)
        # Set docker working directory to result retriever for copying
        self._result_subsystem.config_creator = self._config_subsystem

    async def docker_operation(self):
        """
        Asynchronous running of multiple docker processes. This function
        ends with error or succesfully when deployment of container is done
        and when results are retrieved.

        :return:
        """
        run_tasks = []
        retrieve_tasks = []
        for count, key in enumerate(self._path_subsystem.path_components.keys()):
            component = self._path_subsystem.path_components.get(key)
            run_tasks.append(asyncio.create_task(
                self._run_subsystem.create_container(component[0],
                                                     key.lower()
                                                     + str(count))))
            retrieve_tasks.append((self._result_subsystem.retrieve_docker,
                                   component[0],
                                   key.lower() + str(count)))
        runnable_chunks = list(
            divide_chunks(run_tasks, self.NUM_OF_CONCURRENT_PROCESSES))
        finished = []
        try:
            for chunk in runnable_chunks:
                finished.append(await asyncio.gather(*chunk))
        except KeyboardInterrupt:
            self._run_subsystem.kill_processes()
            raise
        runnable_chunks = list(divide_chunks(retrieve_tasks,
                                             self.NUM_OF_CONCURRENT_PROCESSES))
        for chunk in runnable_chunks:
            for function in chunk:
                function[0](function[1], function[2])

    async def vagrant_operation(self):
        """
        Asynchronous vagrant boxes creation and testing the code.
        :return:
        """
        tasks = []
        result_tasks = []
        for key in self._path_subsystem.path_components.keys():
            if key in self.PORTABLE_LANGUAGES:
                print("{language} programs are portable, nothing to test!"
                      .format(language=key.lower()))
                continue
            component = self._path_subsystem.path_components.get(key)
            tasks.append(asyncio.create_task(
                self._run_subsystem.create_box(component[0])))
            result_tasks.append((self._result_subsystem.retrieve_vagrant, component[0]))
        runnable_chunks = list(
            divide_chunks(tasks, self.NUM_OF_CONCURRENT_PROCESSES))
        finished = []
        try:
            for chunk in runnable_chunks:
                finished.append(await asyncio.gather(*chunk))
        except KeyboardInterrupt:
            self._run_subsystem.kill_processes()
            raise
        runnable_chunks = list(divide_chunks(result_tasks,
                                             self.NUM_OF_CONCURRENT_PROCESSES))
        for chunk in runnable_chunks:
            for function in chunk:
                function[0](function[1])

    def operation(self):
        # todo: create simultaneous running of vagrant and docker
        pass

    def list_filters(self):
        # List filters when desired.
        if self._path_subsystem.list_filters:
            self._path_subsystem.show_filters()

    def kill_processes(self):
        self._run_subsystem.kill_processes()
        self.delete_configurations()

    def delete_configurations(self):
        self._path_subsystem.delete_configurations()
        self._run_subsystem.prune()
        self._run_subsystem.vagrant_destroy()
        self._path_subsystem.destroy_images(self._run_subsystem.tags)
        self._path_subsystem.destroy_boxes()
        self._path_subsystem.destroy_everything(self._run_subsystem.tags)


def divide_chunks(list_var, num_of_chunks):
    # looping till length l
    for i in range(0, len(list_var), num_of_chunks):
        yield list_var[i:i + num_of_chunks]


def console_main():
    # Put command line arguments to Facade
    # Run docker and vagrant
    facade = RunFacade()
    facade.list_filters()
    try:
        asyncio.run(facade.docker_operation())
        # asyncio.run(facade.vagrant_operation())
    except KeyboardInterrupt:
        facade.kill_processes()
        raise
    facade.delete_configurations()

