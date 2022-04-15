#!/usr/bin/env python3


class Comparison:
    """Comparison class.
    This class implements a comparison object used in argument object.

    attr:
        best_criterion_name:
        worst_criterion_name:
    """

    def __init__(self, best_criterion_name, worst_criterion_name):
        """Creates a new comparison.
        """
        self._best_criterion_name = best_criterion_name
        self._worst_criterion_name = worst_criterion_name
    
    def __str__(self):
        return str(self._best_criterion_name) + " > " + str(self._worst_criterion_name)
