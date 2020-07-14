""" This test module is created by Martin Vasko.
    Run both virtualization techniques, VMs and containers. Check whether
    run was successful.
"""

import unittest
import subprocess
import pytest


class RunVirtualization(unittest.TestCase):
    @pytest.mark.run(order=1)
    def test_code_presence(self):
        pass

    @pytest.mark.run(order=2)
    @pytest.mark.usefixtures('run_containers')
    def test_container_run(self):
        pass

    @pytest.mark.run(order=3)
    @pytest.mark.usefixtures('run_vms')
    def test_vm_run(self):
        pass

    def test_logs(self):
        pass

    def test_config_container(self):
        pass

    def test_vm_config(self):
        pass

    def test_container_monitoring(self):
        """todo: sysdig output"""
        pass


