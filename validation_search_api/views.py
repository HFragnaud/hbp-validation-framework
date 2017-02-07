"""


"""

import json
import logging
from datetime import date
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.views.generic import View, ListView, DetailView
from django.http import (HttpResponse, JsonResponse,
                         HttpResponseBadRequest,     # 400
                         HttpResponseForbidden,      # 403
                         HttpResponseNotFound,       # 404
                         HttpResponseNotAllowed,     # 405
                         HttpResponseNotModified,    # 304
                         HttpResponseRedirect)       # 302
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
import requests
#from hbp_app_python_auth.auth import get_auth_header

from .models import ValidationTestDefinition
from .forms import ValidationTestDefinitionForm

CROSSREF_URL = "http://api.crossref.org/works/"
VALID_FILTER_NAMES = ('brain_region', 'cell_type',
                      'data_type', 'data_modality', 'test_type',
                      'author', 'species')

logger = logging.getLogger("validation_search_api")


def get_authorization_header(request):
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    if auth is None:
        try:
#            auth = get_auth_header(request.user.social_auth.get())
            logger.debug("Got authorization from database")
        except AttributeError:
            pass
    # in case of 401 error, need to trap and redirect to login
    else:
        logger.debug("Got authorization from HTTP header")
    return {'Authorization': auth}


# def get_admin_list(request):
#     url = 'https://services.humanbrainproject.eu/idm/v1/api/group/hbp-neuromorphic-platform-admin/members'
#     headers = get_authorization_header(request)
#     res = requests.get(url, headers=headers)
#     logger.debug(headers)
#     if res.status_code != 200:
#         raise Exception("Couldn't get list of administrators." + res.content + str(headers))
#     data = res.json()
#     assert data['page']['totalPages'] == 1
#     admins = [user['id'] for user in data['_embedded']['users']]
#     return admins


# def is_admin(request):
#     try:
#         admins = get_admin_list(request)
#     except Exception as err:
#         logger.warning(err.message)
#         return False
#     try:
#         user_id = get_user(request)["id"]
#     except Exception as err:
#         logger.warning(err.message)
#         return False
#     return user_id in admins


def get_user(request):
    url = "{}/user/me".format(settings.HBP_IDENTITY_SERVICE_URL)
    headers = get_authorization_header(request)
    logger.debug("Requesting user information for given access token")
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        logger.debug("Error" + res.content)
        raise Exception(res.content)
    logger.debug("User information retrieved")
    return res.json()


# def notify_coordinators(request, project):
#     coordinators = get_admin_list(request)
#     url = 'https://services.humanbrainproject.eu/stream/v0/api/notification/'
#     #url = 'https://stream.humanbrainproject.eu/api/v0/notifications/'
#     headers = get_authorization_header(request)
#     targets = [{"type": "HBPUser", "id": id} for id in coordinators]
#     payload = {
#         "summary": "New access request for the Neuromorphic Computing Platform: {}".format(project.title),
#         "targets": targets,
#         "object": {
#             "type": "HBPCollaboratoryContext",
#             "id": "346173bb-887c-4a47-a8fb-0da5d5980dfc"
#         }
#     }
#     res = requests.post(url, json=payload, headers=headers)
#     if res.status_code not in (200, 204):
#         logger.error("Unable to notify coordinators. {}: {}".format(res.status_code, res.content))
#         return False
#     return True


class ValidationTestDefinitionSerializer(object):

    @staticmethod
    def _to_dict(test):
        data = {
            "brain_region": test.brain_region,
            "cell_type": test.cell_type,
            "data_location": test.data_location,
            "data_type": test.data_type,
            "data_modality": test.data_modality,
            "test_type": test.test_type,
            "protocol": test.protocol,
            "code_location": test.code_location,
            "author": test.author,
            "resource_uri": "/validation-tests/{}".format(test.pk)
        }
        return data

    @classmethod
    def serialize(cls, tests):
        if isinstance(tests, ValidationTestDefinition):
            data = cls._to_dict(tests)
        else:
            data = [cls._to_dict(test) for test in tests]
        encoder = DjangoJSONEncoder(ensure_ascii=False, indent=4)
        return encoder.encode(data)


class ValidationTestDefinitionResource(View):
    serializer = ValidationTestDefinitionSerializer

    def _get_test(self, test_id):
        try:
            test = ValidationTestDefinition.objects.get(pk=test_id)
        except ValidationTestDefinition.DoesNotExist:
            test = None
        return test

    def get(self, request, *args, **kwargs):
        """View a test"""
        test = self._get_test(kwargs["test_id"])
        if test is None:
            return HttpResponseNotFound("No such test")
        content = self.serializer.serialize(test)
        return HttpResponse(content, content_type="application/json; charset=utf-8", status=200)


class ValidationTestDefinitionListResource(View):
    serializer = ValidationTestDefinitionSerializer

    def post(self, request, *args, **kwargs):
         """Add a test"""
         # if not is_admin(request):
         #     return HttpResponseForbidden("You do not have permission to add a test.")
         form = ValidationTestDefinitionForm(json.loads(request.body))
         if form.is_valid():
             test = form.save()
             content = self.serializer.serialize(test)
             return HttpResponse(content, content_type="application/json; charset=utf-8", status=201)
         else:
             print(form.data)
             return HttpResponseBadRequest(str(form.errors))  # todo: plain text

    def get(self, request, *args, **kwargs):
        tests = ValidationTestDefinition.objects.all()
        content = self.serializer.serialize(tests)
        return HttpResponse(content, content_type="application/json; charset=utf-8", status=200)


class ValidationTestDefinitionSearchResource(View):
    serializer = ValidationTestDefinitionSerializer

    def get(self, request, *args, **kwargs):
        filters = {}
        for key, value in request.GET.items():
            if key not in VALID_FILTER_NAMES:
                return HttpResponseBadRequest("{} is not a valid filter".format(key))
            else:
                filters[key + "__contains"] = value  # should handle multiple values
        tests = ValidationTestDefinition.objects.filter(**filters)
#        raise Exception(str(filters))
        content = self.serializer.serialize(tests)
        return HttpResponse(content, content_type="application/json; charset=utf-8", status=200)


class SimpleListView(ListView):
    model = ValidationTestDefinition
    template_name = "simple_list.html"

    def get_queryset(self):
        filters = {}
        for key, value in self.request.GET.items():
            print(key, value)
            if key in VALID_FILTER_NAMES:
                filters[key + "__icontains"] = value
        return ValidationTestDefinition.objects.filter(**filters)


class SimpleDetailView(DetailView):
    model = ValidationTestDefinition
    template_name = "simple_detail.html"

    def get_context_data(self, **kwargs):
        context = super(SimpleDetailView, self).get_context_data(**kwargs)
        publication_field = context["object"].publication
        if publication_field.startswith("doi:"):
            crossref_metadata = self._get_crossref_metadata(publication_field)
            context["publication_detail"] = crossref_metadata
            if crossref_metadata:
                context["formatted_publication"] = self._format_publication(crossref_metadata)
        return context

    def _get_crossref_metadata(self, publication_field):
        prefix, doi = publication_field.split(":")
        response = requests.get(CROSSREF_URL + doi)
        if response.ok:
            return response.json()['message']
        else:
            logger.warning("Unable to retrieve metadata for DOI {}".format(doi))
            return {}

    def _format_publication(self, pub_data):
        for author in pub_data["author"]:
            author["initials"] = "".join([name[0] for name in author["given"].split()])
        authors = [u"{family} {initials}".format(**author)
                   for author in pub_data["author"]]
        pub_data["authors"] = u", ".join(authors[:-1]) + u" and " + authors[-1]
        pub_data["year"] = pub_data["created"]["date-parts"][0][0]
        template = u"{authors} ({year}) {title[0]}. {short-container-title[0]} {volume}:{page} {URL}"
        return template.format(**pub_data)
