from django.conf.urls import url
from .views import (ValidationTestDefinitionResource,
                    ValidationTestDefinitionListResource,
                    ValidationTestDefinitionSearchResource,
                    SimpleListView,
                    SimpleDetailView)

uuid_pattern = "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"
# simplified from http://stackoverflow.com/questions/11384589/what-is-the-correct-regex-for-matching-values-generated-by-uuid-uuid4-hex
# will accept some patterns that are not strictly UUID v4

urlpatterns = (
    url(r'^tests/$',
        ValidationTestDefinitionListResource.as_view(),
        name="list-resource"),
    url(r'^tests/(?P<test_id>\d+)$',
        ValidationTestDefinitionResource.as_view(),
        name="item-resource"),
    url(r'^search',
        ValidationTestDefinitionSearchResource.as_view(),
        name="search-resource"),
    url(r'^simple/$',
        SimpleListView.as_view(),
        name="simple-list-view"),
    url(r'^simple/(?P<pk>\d+)$',
        SimpleDetailView.as_view(),
        name="simple-detail-view"),
)