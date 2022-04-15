#!/usr/bin/env python3

from communication.arguments.Comparison import Comparison
from communication.arguments.CoupleValue import CoupleValue


class Argument:
    """Argument class.
    This class implements an argument used in the negotiation.

    attr:
        decision:
        item:
        comparison_list:
        couple_values_list:
    """

    def __init__(self, boolean_decision, item):
        """Creates a new Argument.
        """
        self._decision = boolean_decision
        self._item = item
        self._comparison_list = []
        self._couple_values_list = []

    def __str__(self):
        ret = ("" if self._decision else "not ") + self._item.get_name() + " <= "
        for couple in self._couple_values_list:
            ret += str(couple) + ", "
        for comparison in self._comparison_list:
            ret += str(comparison) + ", "
        return ret[:-2]
        

    def add_premiss_comparison(self, criterion_name_1, criterion_name_2):
        """Adds a premiss comparison in the comparison list.
        """
        self._comparison_list.append(Comparison(criterion_name_1, criterion_name_2))

    def add_premiss_couple_values(self, criterion_name, value):
        """Add a premiss couple values in the couple values list.
        """
        self._couple_values_list.append(CoupleValue(criterion_name, value))
