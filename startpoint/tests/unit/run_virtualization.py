""" This test module is created by Martin Vasko.
    Run both virtualization techniques, VMs and containers. Check whether
    run was successful.
"""

import pytest
import sys
import unittest
import pexpect
import subprocess
from secpo.path_operation import ProgramTypes


@pytest.mark.usefixtures('setup_configuration')
class RunVirtualization(unittest.TestCase):
    DOCKER_CP = "docker cp {src} {cont_id}:{dst}"

    @pytest.mark.run(order=1)
    def test_single_code_presence(self):
        # Choose first directory to be examined
        directory = self.mock_config_creator.directories.pop()
        self.mock_config_creator.directories.add(directory)
        path, text = self.virtual_starter.check_single_source(directory)
        if text:
            image_factory = self.mock_config_creator.image_factory[path.name]
            lang_enum_name = self.mock_config_creator.dict_enum_directories[path.name]
            proc = self.docker_spawn('pytest/' + lang_enum_name.lower(),
                                     text, u'bash')
            proc.logfile = sys.stdout
            print("Listing directory inside docker.")
            proc.sendline(u'ls -al')
            # Copy files into temporary container
            proc.expect("Dockerfile")
            docker_id = proc.docker_inspect()["Id"]
            destination = image_factory.docker_workdir
            cmd = self.DOCKER_CP.format(src=str(self.path_conf.cwd), cont_id=docker_id,
                                        dst=destination)
            subprocess.check_call(cmd.split())
            # Check files inside
            for suffixes in ProgramTypes[lang_enum_name.upper()].value.values():
                for suffix in suffixes:
                    proc.expect(".*" + suffix)
                    file = proc.match.group(0)
                    print("Detected file: {}".format(file))
            proc.sendline(u'cat Dockerfile')
            proc.expect(image_factory.image)
            # Expect end of file, no specific pattern
            try:
                proc.expect(pexpect.EOF)
            except pexpect.TIMEOUT:
                pass
        self.virtual_starter.check_code_files()

    @pytest.mark.run(order=2)
    def test_docker_code_presence(self):
        for path, text in self.virtual_starter.check_code_files():
            proc = self.docker_spawn('pytest/' + self.mock_config_creator.
                                     dict_enum_directories[path.name].lower(),
                                     text, u'bash')
            proc.logfile = sys.stdout
            print("Listing directory inside docker.")
            proc.sendline(u'ls -al')
            proc.expect("Dockerfile")
            proc.sendline(u'cat Dockerfile')
            image = self.mock_config_creator.image_factory[path.name].image
            proc.expect(image)
            # Check files inside
            # Expect end of file
            try:
                proc.expect(pexpect.EOF)
            except pexpect.TIMEOUT:
                pass

    @pytest.mark.run(order=3)
    @pytest.mark.usefixtures('run_containers')
    def test_container_run(self):
        pass

    @pytest.mark.run(order=4)
    @pytest.mark.usefixtures('run_vms')
    def test_vm_run(self):
        pass

    def test_logs(self):
        # self.virtual_starter.logs()
        pass

    def test_config_container(self):
        pass

    def test_vm_config(self):
        pass

    def test_container_monitoring(self):
        """todo: sysdig output"""
        pass


