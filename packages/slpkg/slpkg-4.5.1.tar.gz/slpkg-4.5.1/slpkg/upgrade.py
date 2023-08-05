#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.queries import SBoQueries
from slpkg.utilities import Utilities
from slpkg.blacklist import Blacklist
from slpkg.dependencies import Requires


class Upgrade:
    """ Upgrade the installed packages. """

    def __init__(self):
        self.utils = Utilities()

    def packages(self):
        """ Compares version of packages and returns the maximum. """
        repo_packages = SBoQueries('').sbos()
        black = Blacklist().get()
        upgrade, requires = [], []

        installed = self.utils.all_installed()

        for pkg in installed:
            inst_pkg_name = self.utils.split_installed_pkg(pkg)[0]

            if inst_pkg_name not in black and inst_pkg_name in repo_packages:

                if self.utils.is_repo_version_bigger(inst_pkg_name):
                    requires += Requires(inst_pkg_name).resolve()
                    upgrade.append(inst_pkg_name)

        # Clean the packages if they are dependencies
        for pkg in upgrade:
            if pkg not in requires:
                yield pkg
