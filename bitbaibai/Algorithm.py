#!/usr/bin/env python 
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class Algorithm(ABC):

    def __init__(self, min_samples):
        """

        Parameters
        ----------

        min_samples:

        """
        self.min_samples = min_samples

    @abstractmethod
    def make_decision(self, samples):
        """

        """
        if len(samples) < self.min_samples:
            return False


class NagatomoAlgorithm(Algorithm):

    def make_decision(self, samples):
        super().make_decision(samples)
        # asdfasdf
        # adsfasfda
        return False
        return True