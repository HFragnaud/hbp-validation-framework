from django.contrib import admin
from .models import ValidationTestDefinition


@admin.register(ValidationTestDefinition)
class ValidationTestDefinitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'brain_region', 'cell_type',
                    'data_type', 'data_modality', 'test_type',
                    'publication', 'author')
    list_filter = ('brain_region', 'cell_type', 'test_type')
    search_fields = ('name', 'protocol')
