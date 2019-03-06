#
# -------------------------------
#
# (c) Aurelie Vancraeyenest 2019
# -------------------------------
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

    parameters:
    -----------
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

    parameters:
    -----------
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
