""" This module is created by Martin Vasko.
    Start.py is start point for deploying the containers or vagrant boxes
    according to user input files, written code
"""

import asyncio
from asyncio import create_subprocess_shell
import copy
import os
import time
import signal
import subprocess
import sys
from secpo.path_operation import PathOperation


class VirtualStarter:
    # Colors define
    RED_COLOR = '\033[91m{}\033[00m'
    DOCKER_BUILD = ['docker', 'build', '-t']
    DOCKER_CREATE = 'docker create --name {0} {1}'
    DOCKER_PRUNE = 'docker {prune_type} prune -f'
    # Vagrant commands
    VAGRANT_BOXES = ['vagrant', 'up']
    VAGRANT_DESTROY = 'vagrant destroy -f'
    VBOXMANAGE_LISTVM = 'vboxmanage list runningvms'
    VBOXMANAGE_CONTROLVM = 'vboxmanage controlvm {name} poweroff'
    VBOXMANAGE_UNREGISTERVM = 'vboxmanage unregistervm --delete {name}'
    # Return constants
    SUCCESSFUL = "Successfully built"
    COPY_ERROR = "COPY failed:"
    DAEMON_ERROR = "Error response from daemon:"
    ERROR = "E: "
    RETURN_NON_ZERO = "returned a non-zero code:"
    VBOXMANAGE_ERROR = "VBoxManage --version"
    HOSTNAME_ERROR = "hostname set for the VM should only contain letters"
    NAME_ERROR = 'VirtualBox machine with the name'
    WORKING_ERROR = "The working directory for Vagrant doesn't exist!"
    CONFIGURATION_ERROR = "There are errors in the configuration"

    def __init__(self, path_list):
        """ Initialize """
        self._processes = []
        self.directories = path_list
        self.tags = []

    async def log_output(self, process):
        # Rest of the output
        await process.wait()
        stdout, stderr = await process.communicate()
        print(stdout.decode('utf-8'), end='')
        # Show stderr only when present
        if stderr:
            print(self.RED_COLOR.format(stderr.decode('utf-8')), end='')
            return False
        return True

    async def create_container(self, path, tag):
        """
        Deploy containers in path directories based on the programming language
        add tag to image and create container after building image.
        :return:
        """
        # Create copy of class constant
        command = copy.copy(self.DOCKER_BUILD)
        command.append(tag)
        self.tags.append(tag)
        command.append(str(path).replace(' ', '\\ '))

        process = await create_subprocess_shell(' '.join(command),
                                                stdout=asyncio.subprocess.PIPE,
                                                stderr=asyncio.subprocess.PIPE)
        self._processes.append(process)
        stdout = b""
        stderr = b""
        success = True
        while True:
            if self.SUCCESSFUL in stdout.decode('utf-8') or \
               self.ERROR in stdout.decode('utf-8') or \
               self.RETURN_NON_ZERO in stderr.decode('utf-8') or \
               self.COPY_ERROR in stderr.decode('utf-8') or \
               self.DAEMON_ERROR in stderr.decode('utf-8'):
                await self.log_output(process)
                break
            stdout = await process.stdout.readline()
            print(stdout.decode('utf-8'), end='')
            # Continue when stdout is not empty
            if stdout:
                continue
            # Otherwise error message could be in StreamReader
            stderr = await process.stderr.readline()
            print(self.RED_COLOR.format(stderr.decode('utf-8')), end='')
            if self.RETURN_NON_ZERO not in stderr.decode('utf-8'):
                success = False
        # Clear all processes after execution
        self._processes = []
        if success:
            # Create container from image
            process = await create_subprocess_shell(self.DOCKER_CREATE.format(tag,
                                                                              tag))
            await process.wait()
        else:
            # Exit program because of docker fail
            sys.exit(1)
        return stdout

    async def create_box(self, path):
        """
        Create virtual boxes using Vagrant in path directories based on
        the programming language.
        :return:
        """
        command = copy.copy(self.VAGRANT_BOXES)
        env = os.environ.copy()
        env['VAGRANT_CWD'] = str(path)
        process = await create_subprocess_shell(' '.join(command),
                                                stdout=asyncio.subprocess.PIPE,
                                                stderr=asyncio.subprocess.PIPE,
                                                env=env)
        self._processes.append(process)
        stdout = b""
        stderr = b""
        success = True
        while True:
            if self.VBOXMANAGE_ERROR in stderr.decode('utf-8') or \
               self.HOSTNAME_ERROR in stderr.decode('utf-8') or \
               self.WORKING_ERROR in stderr.decode('utf-8') or \
               self.CONFIGURATION_ERROR in stderr.decode('utf-8') or \
               self.NAME_ERROR in stderr.decode('utf-8') or \
               PathOperation.WELCOME_MESSAGE in stdout.decode('utf-8'):
                await self.log_output(process)
                break
            stdout = await process.stdout.readline()
            print(stdout.decode('utf-8'), end='')
            # If stdout is not empty continue reading
            if stdout:
                continue
            # Otherwise error output was given
            stderr = await process.stderr.readline()
            print(self.RED_COLOR.format(stderr.decode('utf-8')), end='')
            success = False
        # Clear all processes
        self._processes = []
        if not success:
            sys.exit(1)
        return stdout

    async def deploy(self):
        """
        Deploy both containers and vagrant boxes in all directories specified
        by user as input argument.
        """
        for path in self.directories:
            # Deploy docker containers
            asyncio.run(self.create_container(path, path.name))
            # Create boxes
            asyncio.run(self.create_box(path))

    def kill_processes(self):
        """
        Kill all processes when end of program was initiated
        (KeyboardInterrupt, SIGINT, SIGABART etc.)
        """
        for process in self._processes:
            if process:
                spawned_pid = process.pid
                try:
                    os.kill(spawned_pid + 1, signal.SIGINT)
                except ProcessLookupError:
                    continue
                process.kill()
        self._processes = []

    def prune(self):
        """ Prune all unsed docker containers and images."""
        process = subprocess.Popen(self.DOCKER_PRUNE.format(
                prune_type='container').split(' '))
        process.wait()
        process = subprocess.Popen(self.DOCKER_PRUNE.format(
                prune_type='image').split(' '))
        process.wait()

    def vagrant_destroy(self):
        """ Destroy all vagrant and virtualbox images."""
        process = subprocess.Popen(self.VAGRANT_DESTROY.split(' '))
        process.wait()
        process = subprocess.Popen(self.VBOXMANAGE_LISTVM.split(' '),
                                   stdout=subprocess.PIPE)
        process.wait()
        output, _ = process.communicate()
        vms = output.decode('utf-8').split('\n')
        for vm in vms:
            if not vm:
                break
            index = vm.rfind('\"')
            output = vm[1:index]
            cmd = self.VBOXMANAGE_CONTROLVM.format(name=output)
            process = subprocess.Popen(cmd.split(' '))
            process.wait()
            cmd = self.VBOXMANAGE_UNREGISTERVM.format(name=output)
            process = subprocess.Popen(cmd.split(' '))
            process.wait()
