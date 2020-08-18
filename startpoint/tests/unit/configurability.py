""" This test module is created by Martin Vasko.
    Configurability testing tests command line arguments and their applicability.
"""

import os
import pathlib
import pytest
import unittest
from secpo.docker_configuration import ApparmorDockerImageFactory


@pytest.mark.usefixtures("configure")
class Configurability(unittest.TestCase):
    WINDOWS = 'nt'
    POSIX = 'posix'

    def test_classes(self):
        assert hasattr(self, "path_conf")
        self.assertIsInstance(self.apparmor_factory, ApparmorDockerImageFactory)

    def test_present_configuration(self):
        self.assertIsInstance(self.path_conf.input_directories, list)
        self.assertIsInstance(self.path_conf.input_files, list)
        if self.path_conf.input_files:
            if os.name is self.POSIX:
                self.assertIsInstance(self.path_conf.input_files,
                                      pathlib.PosixPath)
            else:
                self.assertIsInstance(self.path_conf.input_files,
                                      pathlib.WindowsPath)

    @pytest.mark.run(order=1)
    def test_no_image_factory(self):
        self.assertGreater(len(self.apparmor_factory.ALLOWED_OS), 0)
        # Image not set yet
        self.assertIsNone(self.apparmor_factory.image)
        self.assertIsNone(self.apparmor_factory.package_manager)

    @pytest.mark.run(order=2)
    @pytest.mark.usefixtures('setup_image')
    def test_image_factory(self):
        self.assertIsNotNone(self.apparmor_factory.image)
        self.assertIsNotNone(self.apparmor_factory.package_manager)
