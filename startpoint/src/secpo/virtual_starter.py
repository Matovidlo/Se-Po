""" This module is created by Martin Vasko.
    Start.py is start point for deploying the containers or vagrant boxes
    according to user input files, written code
"""

import copy
import os
from subprocess import run


class VirtualStarter:
    DOCKER_BUILD = ['docker', 'build']
    VAGRANT_BOXES = ['vagrant', 'up']

    def __init__(self, path_list):
        """ Initialize """
        self.directories = path_list

    def deploy_containers(self):
        """
        Deploy containers in path directories based on the programming language.
        :return:
        """
        for path in self.directories:
            # Create copy of class constant
            command = copy.copy(self.DOCKER_BUILD)
            command.append(str(path))
            run(command)

    def create_boxes(self):
        """
        Create virtual boxes using Vagrant in path directories based on
        the programming language.
        :return:
        """
        for path in self.directories:
            command = copy.copy(self.VAGRANT_BOXES)
            command.append(str(path))
            run(command)

    def deploy(self):
        """
        Deploy both containers and vagrant boxes in all directories specified
        by user as input argument.
        :return:
        """
        for path in self.directories:
            # Deploy docker containers
            command = copy.copy(self.DOCKER_BUILD)
            command.append(str(path))
            run(command)
            # Create vagrant boxes
            command = copy.copy(self.VAGRANT_BOXES)
            os.putenv('VAGRANT_CWD', path)
            run(command, env=os.environ)
            # todo: unset env variable?

