from django.forms import ModelForm, Field
from .models import ValidationTestResult, ScientificModel



class DictField(Field):
    validators = []

    def __init__(self, required=False, label="", initial="", widget=None, help_text=""):
        pass

    def clean(self, value):
        raise Exception(str(value))


class ValidationTestResultForm(ModelForm):
    model_instance = DictField()

    class Meta:
        model = ValidationTestResult
        fields = "__all__"




class ScientificModelForm(ModelForm):

    class Meta:
        model = ScientificModel
        fields = "__all__"
