"""
Django models for the Model Validation API

"""

import json
import uuid
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
    author = models.CharField(max_length=100, help_text="Author of this test")  # H
    publication = models.CharField(max_length=200, null=True, help_text="Publication in which the validation data set was reported")  # E

    # missing fields wrt Lungsi's spreadsheet
    # L - file format  - infer from file suffix?
    # N - registered with NIP?
    # O - language of test code
    # Q - test code version

    def __str__(self):
        return "Test {}: {}".format(self.id, self.name)

    def get_latest_code(self):
        """
        Return the most recent code for this test
        """
        return self.code.latest()


@python_2_unicode_compatible
class ValidationTestCode(models.Model):
    repository = models.CharField(max_length=200, help_text="location of the code that defines the test")
    version = models.CharField(max_length=128, help_text="version of the code that defines the test")
    path = models.CharField(max_length=200, help_text="path to test class within Python code")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="timestamp for this version of the code")
    test_definition = models.ForeignKey(ValidationTestDefinition, help_text="Validation test implemented by this code",
                                        related_name="code")

    class Meta:
        verbose_name_plural = "validation test code"
        get_latest_by = "timestamp"

    def __str__(self):
        return "Code for test {}: {}@{}:{}".format(self.test_definition.pk,
                                                   self.repository,
                                                   self.version,
                                                   self.path)

# separate classes for Dataset, Code, ValidationTestDefinition?


@python_2_unicode_compatible
class ScientificModel(models.Model):
    """
    A model of a subcellular mechanism, cell, neuronal network, or other neural structure.

    The model may change over time or have different parameterisations.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, help_text="short descriptive name")
    description = models.TextField()
    species = models.CharField(max_length=100, blank=True, help_text="species")
    brain_region = models.CharField(max_length=100, blank=True, help_text="brain region, if applicable")
    cell_type = models.CharField(max_length=100, blank=True, help_text="cell type, for single-cell models")
    author = models.TextField(help_text="Author(s) of this model")  # do we need a separate "owner" field?
    source = models.URLField(help_text="Version control repository containing the source code of the model")
    # todo: move `source` field into ModelInstance
    # model_type? (network, single neuron, etc.)?
    # spiking vs rate?

    def __str__(self):
        return "Model: {} ({})".format(self.name, self.id)


@python_2_unicode_compatible
class ScientificModelInstance(models.Model):
    """
    A specific instance of a model with a well defined version and parameterization.
    """
    model = models.ForeignKey(ScientificModel, related_name="instances")
    version = models.CharField(max_length=64)
    parameters = models.TextField()

    def __str__(self):
        return "Model: {} @ version {}".format(self.model.name, self.version)


@python_2_unicode_compatible
class ValidationTestResult(models.Model):

    model_instance = models.ForeignKey(ScientificModelInstance)
    test_definition = models.ForeignKey(ValidationTestCode)
    results_storage = models.TextField(help_text="Location of data files produced by the test run")  # or store locations of individual files?
    result = models.FloatField(help_text="A numerical measure of the difference between model and experiment")  # name this 'score'? like sciunit
    # should result be a Quantity?
    passed = models.NullBooleanField(help_text="Whether the test passed or failed")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Timestamp of when the simulation was run")
    platform = models.TextField(help_text="Computer system on which the simulation was run")
    project = models.CharField(help_text="Project with which this test run is associated(optional)",
                               max_length=200,
                               blank=True)  # project==collab_id for HBP

    class Meta:
        get_latest_by = "timestamp"

    def get_platform_as_dict(self):
        return json.loads(self.platform)

    def __str__(self):
        return "Validation test result {}".format(self.id,)
