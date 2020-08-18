""" This module is created by Martin Vasko.
    Module contains AbstractDockerImage that is used to generate unique
    setup for certain docker image.
"""

from abc import ABCMeta, abstractmethod
from secpo.mac_profiles import SimpleSeccompProfile, SimpleApparmorProfile, \
    CustomizedApparmorProfile, CustomizedSeccompProfile
import os


class AbstractDockerImageFactory(metaclass=ABCMeta):
    """
    Abstract interface for docker images. They can be official, community
    or custom created from scratch.
    """
    SCRATCH = 'scratch'
    UBUNTU = 'ubuntu'
    CENTOS = 'centos'
    FEDORA = 'fedora'
    DEBIAN = 'debian'
    PYTHON = 'python'
    GOLANG = 'golang'
    HASKELL = 'haskell'
    JAVASCRIPT = 'node'
    JAVA = 'java'
    PHP = 'php'
    RUBY = "ruby"
    FROM = 'FROM '

    ALPINE = ':alpine'
    BUSTER = ':buster'
    LATEST = ':latest'
    # Package managers
    APK = 'apk'
    APTGET = 'apt-get'
    DNF = 'dnf'
    YUM = 'yum'
    # Program package installers
    BREW = 'brew'
    COMPOSER = 'composer require'
    GEM = 'gem'
    GRADLE = 'gradlew'
    NPM = 'npm'
    PIP = 'pip'
    STACK = 'stack'

    @abstractmethod
    def __init__(self, cls_object, docker_workdir):
        """ Initialization """
        self.docker_workdir = docker_workdir
        self._image = None
        self._package_manager = None
        self._program_package_installer = None
        cls_object.create_mac_profile()
        cls_object.create_seccomp_profile()

    @property
    def image(self):
        """
        Returns operation system that was filled either by user or automatically
        based on the running OS.
        :return: self._operation_system
        """
        return self._image

    @property
    def package_manager(self):
        """ Returns package manager of operation system"""
        return self._package_manager

    @property
    def program_package_installer(self):
        return self._program_package_installer

    def _set_package_manager(self):
        """
        Sets package manager based on the _image class attribute.
        """
        if self._image in [self.UBUNTU]:
            self._package_manager = self.APTGET
        elif self._image in [self.CENTOS]:
            self._package_manager = self.YUM
        elif self._image in [self.FEDORA]:
            self._package_manager = self.DNF
        elif self._image in [self.PYTHON, self.JAVA]:
            self._package_manager = self.APK
            if self._image in self.PYTHON:
                self._program_package_installer = self.PIP
        elif self._image in [self.HASKELL]:
            self._package_manager = self.APTGET
            self._program_package_installer = self.STACK
        elif self._image in [self.JAVASCRIPT]:
            # Choose alpine
            self._package_manager = self.APTGET
            self._program_package_installer = self.NPM
        elif self._image in [self.PHP]:
            self._package_manager = self.APTGET
            self._program_package_installer = self.COMPOSER
        elif self._image in [self.RUBY]:
            # Choose alpine
            self._package_manager = self.APK
            self._program_package_installer = self.GEM

    @abstractmethod
    def create_image(self, image, allowed_os, version=None):
        """
        Creates simple docker image that is inside official repository.
        :param image: Operation system that user wants to deploy
        :param allowed_os: List of allowed OS.
        :param version: Version of chosen image.
        :raises Exception: When wrong operation system was provided the setup
                   cannot continue and exception is raised.
        """
        self._image = image
        # Set package manager for docker image.
        self._set_package_manager()
        if not self._image or self._image not in allowed_os:
            raise Exception('Wrong image of system selected: {}. Cannot be '
                            'found in list of allowed OS.{} Try one '
                            'of the following: {}, {}, {}, {}, {}, {}, {}'
                            .format(image, os.linesep, self.SCRATCH,
                                    self.UBUNTU,  self.CENTOS, self.PHP,
                                    self.PYTHON, self.GOLANG, self.HASKELL))
        if version:
            self._image = self.FROM + self._image + ":" + str(version)
        elif self._image != self.ALPINE and self.APK in self._package_manager:
            self._image = self.FROM + self._image + self.ALPINE
        elif (self._image != self.DEBIAN and self._image != self.UBUNTU) \
                and self.APTGET in self._package_manager:
            self._image = self.FROM + self._image + self.BUSTER
        elif self._image != self.CENTOS and self.YUM in self._package_manager:
            self._image = self.FROM + self._image + self.CENTOS
        elif self._image != self.FEDORA and self.DNF in self._package_manager:
            self._image = self.FROM + self._image + self.FEDORA
        else:
            self._image = self.FROM + self._image + self.LATEST

    @abstractmethod
    def create_seccomp_profile(self):
        """
        Creates seccomp profile for particular purpose for single instance
        of docker configuration.

        :return: Concrete realization of class:`AbstractProfile`
        :rtype: class:`AbstractProfile`
        """
        pass

    @abstractmethod
    def create_mac_profile(self):
        """
        Creates Mandatory Access Control profile for particular purpose
        for single instance of docker configuration.

        :return: Concrete realization of class:`AbstractProfile`
        :rtype: class:`AbstractProfile`
        """
        pass

    @abstractmethod
    def unix_setup(self):
        """
        Different Unix systems have different packaging managers, tools etc.
        Setup it according to concrete unix system.
        """
        pass


class ApparmorDockerImageFactory(AbstractDockerImageFactory):
    """
    Apparmor docker image factory. Creates family of unix images that use
    as Mandatory access control apparmor.
    todo: test against officiality of image
    """
    SECCOMP = 'seccomp'
    MAC = 'apparmor'

    def __init__(self, docker_workdir):
        super(ApparmorDockerImageFactory, self).__init__(self, docker_workdir)

    def create_image(self, operation_system, allowed_os, version=None):
        """
        Creates image based on operation system given and set of allowed
        operation systems. When user wants to deploy specific version, version
        argument is supplied.
        :param operation_system: Operation system that docker is able to deploy.
        :param allowed_os: Set of allowed Operation systems.
        :param version: Specific version of Operation system.
        """
        super(ApparmorDockerImageFactory, self).\
            create_image(operation_system, allowed_os, version)

    def create_seccomp_profile(self):
        return SimpleSeccompProfile()

    def create_mac_profile(self):
        return SimpleApparmorProfile()

    def unix_setup(self):
        return [self.SECCOMP, self.MAC]


class CustomDockerImageFactory(AbstractDockerImageFactory):
    """
    Ubuntu docker image. todo: test against officiality of image
    """
    SECCOMP = 'seccomp'
    MAC = 'apparmor'

    def __init__(self, docker_workdir):
        """ Initialization """
        super(CustomDockerImageFactory, self).__init__(self, docker_workdir)

    def create_image(self, operation_system, allowed_os, version=None):
        """
        Creates image based on operation system given and set of allowed
        operation systems. When user wants to deploy specific version, version
        argument is supplied.
        :param operation_system: Operation system that docker is able to deploy.
        :param allowed_os: Set of allowed Operation systems.
        :param version: Specific version of Operation system.
        """
        super(CustomDockerImageFactory, self)\
            .create_image(operation_system, allowed_os, version)

    def create_mac_profile(self):
        return CustomizedApparmorProfile()

    def create_seccomp_profile(self):
        return CustomizedSeccompProfile()

    def unix_setup(self):
        return [self.SECCOMP, self.MAC]
