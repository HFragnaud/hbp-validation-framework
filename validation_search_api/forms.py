from django.forms import ModelForm
from .models import ValidationTestDefinition


class ValidationTestDefinitionForm(ModelForm):

    class Meta:
        model = ValidationTestDefinition
        fields = "__all__"
