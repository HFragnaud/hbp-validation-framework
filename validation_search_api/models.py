"""
Django models for the Validation Search API

"""

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


DATA_MODALITIES = (("ephys", "electrophysiology"),
                   ("fMRI", "fMRI"),
                   ("2-photon", "2-photon imaging"),
                   ("em", "electron microscopy"),
                   ("histology", "histology"))
TEST_TYPES = (("single cell", "single cell activity"),
              ("network structure", "network structure"),
              ("network activity", "network activity"),
              ("behaviour", "behaviour"),
              ("subcellular", "subcellular"))

@python_2_unicode_compatible
class ValidationTestDefinition(models.Model):
    name = models.CharField(max_length=200, help_text="short descriptive name")
    species = models.CharField(max_length=100, help_text="species") # G
    brain_region = models.CharField(max_length=100, help_text="brain region")  # I
    cell_type = models.CharField(max_length=100, help_text="cell type")  # D
    age = models.CharField(max_length=50, null=True, help_text="age of animal, e.g. '6 weeks'")
    data_location = models.CharField(max_length=200, help_text="location of comparison data")  # M
    data_type = models.CharField(max_length=100, help_text="type of comparison data (number, histogram, time series, etc.)")  # S
    data_modality = models.CharField(max_length=100,  choices=DATA_MODALITIES,
                                     help_text="recording modality for comparison data (ephys, fMRI, 2-photon, etc)")  # J, K
    test_type = models.CharField(max_length=100, choices=TEST_TYPES,
                                 help_text="single cell activity, network structure, network activity, subcellular")  # B, C
    protocol = models.TextField(blank=True, help_text="Description of the experimental protocol")  # R (sort of)
    code_location = models.CharField(max_length=200, help_text="location of the code that defines the test")
    author = models.CharField(max_length=100, help_text="Author of this test")  # H
    publication = models.CharField(max_length=200, null=True, help_text="Publication in which the validation data set was reported")  # E

    # missing fields wrt Lungsi's spreadsheet
    # L - file format  - infer from file suffix?
    # N - registered with NIP?
    # O - language of test code
    # Q - test code version

    def __str__(self):
        return "Test {}".format(self.id,)


# separate classes for Dataset, Code, ValidationTestDefinition?