""" This module is created by Martin Vasko.
    Module contains AbstractProfile interface that should be implemented
    in order to create and use security profiles such as MAC or seccomp.
"""

from abc import ABCMeta, abstractmethod


class AbstractProfile(metaclass=ABCMeta):
    """
    Abstract class to create Seccomp Profile
    """
    @abstractmethod
    def create_profile(self):
        """
        Creates concrete profile for seccomp rules, for apparmor or any other
        profiles that are desired by user.

        :return: Created profile that is used for particular purposes with
                 specific steps to create.
        :rtype: class:`AbstractProfile`
        """
        pass

    @abstractmethod
    def parse_profile(self):
        """
        Profile has to be parsed in order to apply its rules within dockerfile.
        """
        pass


class SimpleSeccompProfile(AbstractProfile):
    """
    Create seccomp profile using abstract interface.
    """
    def create_profile(self):
        pass

    def parse_profile(self):
        pass


class CustomizedSeccompProfile(AbstractProfile):
    """
    Create user customized seccomp profile using abstract interface.
    """
    def create_profile(self):
        pass

    def parse_profile(self):
        pass


class SimpleApparmorProfile(AbstractProfile):
    """
    Create apparmor profile using abstract interface.
    """
    def create_profile(self):
        pass

    def parse_profile(self):
        pass


class CustomizedApparmorProfile(AbstractProfile):
    """
    Create user customized apparmor profile using abstract interface.
    """
    def create_profile(self):
        pass

    def parse_profile(self):
        pass
