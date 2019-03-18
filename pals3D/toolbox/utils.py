# This file is part of Pals3D
#
# ---------------------------------------------
#
# Copyright (c) 2018-2019 Aurelie Vancraeyenest 
# ---------------------------------------------
#
# Pals3D is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pals3D is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pals3D.  If not, see <http://www.gnu.org/licenses/>.
#

import itertools
from PyQt5 import QtWidgets


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."

    a, b = itertools.tee(iterable, 2)
    next(b, None)
    return zip(a, b)


def tripletwise(iterable):
    "s -> (s0,s1,s2), (s1,s2,s3), (s2,s3,s4), ..."

    a, b, c = itertools.tee(iterable, 3)
    next(b, None)
    next(c, None)
    next(c, None)
    return zip(a, b, c)


def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in itertools.filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


def disableChildOf(widget, exceptThis=None):
    """
    Disable all the interactive widgets of a group/parent

    Parameters
    ----------
    widget : QtWidget name, e.g. self.widgetName
        parent/group widget name for which all members will be disabled
    exceptThis : QtWidget name, e.g. self.widgetName
        name of the widget that remains enabled

    """
    for widg in widget.findChildren((QtWidgets.QLineEdit,
                                     QtWidgets.QRadioButton,
                                     QtWidgets.QCheckBox,
                                     QtWidgets.QPushButton)):
        if widg == exceptThis:
            continue
        widg.setEnabled(False)


def enableChildOf(widget, exceptThis=None):
    """
    Enable all the interactive widgets of a group/parent

    Parameters
    ----------
    widget : QtWidget name, e.g. self.widgetName
        parent/group widget name for which all members will be enabled
    exceptThis : QtWidget name, e.g. self.widgetName
        name of the widget that remains disabled

    """
    for widg in widget.findChildren((QtWidgets.QLineEdit,
                                     QtWidgets.QRadioButton,
                                     QtWidgets.QCheckBox,
                                     QtWidgets.QPushButton)):
        if widg == exceptThis:
            continue
        widg.setEnabled(True)
