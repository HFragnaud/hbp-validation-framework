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

from .models import ValidationTestResult, ScientificModelInstance, ScientificModel
from .forms import ValidationTestResultForm, ScientificModelForm

CROSSREF_URL = "http://api.crossref.org/works/"
VALID_MODEL_FILTER_NAMES = ('brain_region', 'cell_type',
                            'author', 'species')

logger = logging.getLogger("validation_results_api")


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


class ValidationTestResultSerializer(object):

    @staticmethod
    def _to_dict(result):
        data = {
            "model_instance": {
                "model_id": result.model_instance.model.pk,
                "version": result.model_instance.version,
                "parameters": result.model_instance.parameters
            },
            "test_definition": result.test_definition,
            "results_storage": result.results_storage,
            "result": result.result,
            "passed": result.passed,
            "platform": result.get_platform_as_dict(),
            "timestamp": result.timestamp,
            "resource_uri": "/results/{}".format(result.pk)
        }
        return data

    @classmethod
    def serialize(cls, results):
        if isinstance(results, ValidationTestResult):
            data = cls._to_dict(results)
        else:
            data = [cls._to_dict(result) for result in results]
        encoder = DjangoJSONEncoder(ensure_ascii=False, indent=4)
        return encoder.encode(data)


class ScientificModelSerializer(object):

    @staticmethod
    def _to_dict(model):
        data = {
            "name": model.name,
            "description": model.description,
            "species": model.species,
            "brain_region": model.brain_region,
            "cell_type": model.cell_type,
            "author": model.author,
            "source": model.source,
            "resource_uri": "/models/{}".format(model.pk)
        }
        return data

    @classmethod
    def serialize(cls, models):
        if isinstance(models, ScientificModel):
            data = cls._to_dict(models)
        else:
            data = [cls._to_dict(model) for model in models]
        encoder = DjangoJSONEncoder(ensure_ascii=False, indent=4)
        return encoder.encode(data)



class ValidationTestResultResource(View):
    serializer = ValidationTestResultSerializer

    def _get_result(self, result_id):
        try:
            result = ValidationTestResult.objects.get(pk=result_id)
        except ValidationTestResult.DoesNotExist:
            result = None
        return result

    def get(self, request, *args, **kwargs):
        """View a result"""
        result = self._get_result(kwargs["result_id"])
        if result is None:
            return HttpResponseNotFound("No such result")
        content = self.serializer.serialize(result)
        return HttpResponse(content, content_type="application/json; charset=utf-8", status=200)


class ValidationTestResultListResource(View):
    serializer = ValidationTestResultSerializer

    def post(self, request, *args, **kwargs):
        """Add a result"""
         # if not is_admin(request):
         #     return HttpResponseForbidden("You do not have permission to add a result.")

        data = json.loads(request.body)

        sci_model = ScientificModel.objects.get(pk=data["model_instance"]["model_id"])
        model_instance, created = ScientificModelInstance.objects.get_or_create(model=sci_model,
                                                                            version=data["model_instance"]["version"],
                                                                            parameters=data["model_instance"]["parameters"])
        new_test_result = ValidationTestResult(model_instance=model_instance,
                                               test_definition=data["test_definition"],
                                               results_storage=data["results_storage"],
                                               result=float(data["result"]),  # should be a Quantity?
                                               passed=data["passed"],
                                               platform=json.dumps(data["platform"]))
        new_test_result.save()
        content = self.serializer.serialize(new_test_result)
        return HttpResponse(content, content_type="application/json; charset=utf-8", status=201)

    def get(self, request, *args, **kwargs):
        results = ValidationTestResult.objects.all()
        content = self.serializer.serialize(results)
        return HttpResponse(content, content_type="application/json; charset=utf-8", status=200)


class ScientificModelResource(View):
    serializer = ScientificModelSerializer

    def _get_model(self, model_id):
        try:
            model = ScientificModel.objects.get(pk=model_id)
        except ScientificModel.DoesNotExist:
            model = None
        return model

    def get(self, request, *args, **kwargs):
        """View a model"""
        model = self._get_model(kwargs["model_id"])
        if model is None:
            return HttpResponseNotFound("No such result")
        content = self.serializer.serialize(model)
        return HttpResponse(content, content_type="application/json; charset=utf-8", status=200)


class ScientificModelListResource(View):
    serializer = ScientificModelSerializer

    def post(self, request, *args, **kwargs):
         """Add a model"""
         # if not is_admin(request):
         #     return HttpResponseForbidden("You do not have permission to add a result.")
         form = ScientificModelForm(json.loads(request.body))
         if form.is_valid():
             model = form.save()
             content = self.serializer.serialize(model)
             return HttpResponse(content, content_type="application/json; charset=utf-8", status=201)
         else:
             print(form.data)
             return HttpResponseBadRequest(str(form.errors))  # todo: plain text

    def get(self, request, *args, **kwargs):
        models = ScientificModel.objects.all()
        content = self.serializer.serialize(models)
        return HttpResponse(content, content_type="application/json; charset=utf-8", status=200)



class SimpleModelListView(ListView):
    model = ScientificModel
    template_name = "simple_model_list.html"

    def get_queryset(self):
        filters = {}
        for key, value in self.request.GET.items():
            if key in VALID_MODEL_FILTER_NAMES:
                filters[key + "__icontains"] = value
        return ScientificModel.objects.filter(**filters)


class SimpleModelDetailView(DetailView):
    model = ScientificModel
    template_name = "simple_model_detail.html"


class SimpleResultListView(ListView):
    model = ValidationTestResult
    template_name = "simple_result_list.html"

    def get_queryset(self):
        filters = {}
        #for key, value in self.request.GET.items():
        #    if key in VALID_MODEL_FILTER_NAMES:
        #        filters[key + "__icontains"] = value
        return ValidationTestResult.objects.all()  #filter(**filters)


class SimpleResultDetailView(DetailView):
    model = ValidationTestResult
    template_name = "simple_result_detail.html"