""" This test module is created by Martin Vasko.
    After successful run of both virtualization techniques retrieve results from
    docker image and vagrant box. Check whether it was succesfully.
    Additionally perform result comparison with pre-built expected output.
"""

import unittest
import pytest


class RetrieveResults(unittest.TestCase):
    @pytest.mark.run(order=1)
    def test_result_highlighter(self):
        pass

    @pytest.mark.run(order=2)
    def test_container_existance(self):
        """ Container should be undeployed at this time. """
        pass

    @pytest.mark.run(order=3)
    def test_vm_existence(self):
        """ VM should be not running anymore at this time. """
        pass

    def test_retrieve_result(self):
        """ Retrieve results from both container and VM. """
        pass

    def test_existance_of_result(self):
        pass

    def test_compare_result(self):
        pass

    def test_portability_results(self):
        pass

    def test_security_results(self):
        pass

    def test_sysdig_results(self):
        pass

    def test_compare_source_and_changed_code(self):
        """ Expected outcome is that source code differs from output one. """
        pass

