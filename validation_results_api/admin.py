from django.contrib import admin
from .models import ValidationTestResult, ScientificModel, ScientificModelInstance


@admin.register(ValidationTestResult)
class ValidationTestResultAdmin(admin.ModelAdmin):
    list_display = ('model_instance', 'test_definition',
                    'result', 'passed', 'timestamp',
                    'platform')
    search_fields = ('model_instance', 'test_definition')


admin.site.register(ScientificModel)
admin.site.register(ScientificModelInstance)
