#!/usr/bin/env python3


class CoupleValue:
    """CoupleValue class.
    This class implements a couple value used in argument object.

    attr:
        criterion_name:
        value:
    """

    def __init__(self, criterion_name, value):
        """Creates a new couple value.
        """
        self._criterion_name = criterion_name
        self._value = value

    def __str__(self):
        return str(self._criterion_name) +" = "+ str(self._value) 
