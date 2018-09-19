import os
from io import StringIO

import json
import requests
import urllib3
import collections
urllib3.disable_warnings()

from django.shortcuts import render, HttpResponse
from django.http import StreamingHttpResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.core.files import File
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import DeleteView, CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from django.db.models import Q

from django.shortcuts import get_object_or_404

from mainapp.models import Units, Companys, Address, Classifier


def add_data_classifier(type_text, obj):
    if obj[type_text] is None:
        return None

    tup = Classifier.type_choices
    result = list(filter(lambda x: x[1] == type_text, tup))
    if result:
        typeof = result[0][0]
    else:
        typeof = None
    try:
        obj_Classifier = Classifier.objects.get(
            name=obj[type_text], typeof=typeof)
    except ObjectDoesNotExist:
        obj_Classifier = Classifier(name=obj[type_text], typeof=typeof)
        obj_Classifier.save()
    obj[type_text] = obj_Classifier


def check_data(name, obj, return_dict, default=None):
    data = obj.get(name, None)
    if data:
        return_dict[name] = data
    else:
        return_dict[name] = default
    return return_dict


def add_row_to_db(row):
    unit_dict = dict()
    company_dict = dict()
    addres_dict = dict()

    unit_dict = check_data('name', row, unit_dict, 'none_name')
    unit_dict = check_data('username', row, unit_dict, 'none_username')
    unit_dict = check_data('email', row, unit_dict)
    unit_dict = check_data('phone', row, unit_dict)
    unit_dict = check_data('website', row, unit_dict)
    unit_dict['on_load'] = True
    obj_Units, created_Units = Units.objects.filter(
        name=unit_dict['name'], username=unit_dict['username'], on_load=True).get_or_create(
        **unit_dict)

    company = row.get('company', None)
    if company:
        company_dict = check_data(
            'name',
            company,
            company_dict,
            'none_company_name')
        company_dict['on_load'] = True
        obj_Companys, created_Companys = Companys.objects.filter(
            name=company_dict['name'], on_load=True).get_or_create(**company_dict)

    address = row.get('address', None)
    if address:
        addres_dict = check_data('zipcode', address, addres_dict)
        add_data_classifier('zipcode', addres_dict)

        addres_dict = check_data('suite', address, addres_dict)
        add_data_classifier('suite', addres_dict)

        addres_dict = check_data('city', address, addres_dict)
        add_data_classifier('city', addres_dict)

        addres_dict = check_data('street', address, addres_dict)
        add_data_classifier('street', addres_dict)

        geo = address.get('geo', None)
        if geo:
            addres_dict = check_data('lat', geo, addres_dict)
            addres_dict = check_data('lng', geo, addres_dict)

        addres_dict['region'] = None

        field_list = [
            addres_dict['zipcode'],
            addres_dict['region'],
            addres_dict['city'],
            addres_dict['street'],
            addres_dict['suite']]
        field_list = [i.name if i is not None else '' for i in field_list]
        full_name = ' '.join(field_list)

        obj_Address, created_Address = Address.objects.filter(
            full_name=full_name).get_or_create(**addres_dict)
        obj_Units.address = obj_Address
        obj_Units.company = obj_Companys
        obj_Units.save()


class BaseView(ListView):

    def get_queryset(self):
        self.page = self.request.GET.get('page', None)
        search = self.request.GET.get('search', None)
        name__regex = r'^.*{}.*$'.format(search)

        if search:
            result_query = self.model.objects.all()
        else:
            result_query = self.model.objects.all()
        return result_query

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        #page = self.request.GET.get('page', None)
        #search = self.request.GET.get('search', None)

        #name__regex = r'^.*{}.*$'.format(search)

        # if search:
        #    result_query = self.model.objects.all()
        #    #result_query = self.model.objects.filter(
        #    #    Q(
        #    #        name__regex=name__regex) | Q(
        #    #        company__name__regex=name__regex) | Q(
        #    #        email__regex=name__regex) | Q(
        #    #        phone__regex=name__regex) | Q(
        #    #            interests__regex=name__regex))
        # else:
        #    result_query = self.model.objects.all()
        paginator = Paginator(self.get_queryset(), self.paginate_by)

        try:
            result_query = paginator.page(self.page)
        except PageNotAnInteger:
            result_query = paginator.page(1)
        except EmptyPage:
            result_query = paginator.page(paginator.num_pages)

        context['result_query'] = result_query
        context['col_names'] = self.model.get_field_names_gen()
        return context


def main(request):
    return render(request, 'mainapp/index.html')


class Units_List(BaseView, ListView):

    model = Units
    template_name = 'mainapp/lists.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_pref'] = '/units/'
        context['model'] = 'units'
        return context


class Companys_List(BaseView, ListView):

    model = Companys
    template_name = 'mainapp/lists.html'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['col_names'] = self.model.get_field_names_gen()
        context['url_pref'] = '/companys/'
        context['model'] = 'companys'
        return context


def load_data(request):
    resp = requests.get(
        'https://jsonplaceholder.typicode.com/users',
        verify=False)
    if resp.status_code != 200:
        return HttpResponse('status code error: code is not 200')
    try:
        data = resp.json()
    except ValueError:
        return HttpResponse('No JSON object could be decoded')
    if not isinstance(data, collections.Iterable):
        return HttpResponse('No JSON object could be decoded')
    for row in data:
        add_row_to_db(row)

    return render(request, 'mainapp/index.html')


def clear_data(request):
    return render(request, 'mainapp/index.html')
