"""
Django models for the Validation Search API

"""

import json
import uuid
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


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
    author = models.TextField(help_text="Author(s) of this model")
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
    test_definition = models.URLField(help_text="URI of the validation test definition")
    results_storage = models.TextField(help_text="Location of data files produced by the test run")  # or store locations of individual files?
    result = models.FloatField(help_text="A numerical measure of the difference between model and experiment")  # name this 'score'? like sciunit
    # should result be a Quantity?
    passed = models.NullBooleanField(help_text="Whether the test passed or failed")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Timestamp of when the simulation was run")
    platform = models.TextField(help_text="Computer system on which the simulation was run")

    def get_platform_as_dict(self):
        return json.loads(self.platform)

    def __str__(self):
        return "Validation test result {}".format(self.id,)