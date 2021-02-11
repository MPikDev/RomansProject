from copy import deepcopy

from django.shortcuts import render
from .models import CompanyInfo, STATES_TUPLE, SCHEDULING_OPTIONS, LOAD_TYPE_OPTIONS,CompanyInfoEntry


# Create your views here.

def home(request):
    company_infos = CompanyInfo.objects.all()
    data = {
        'company_infos': company_infos,
    }
    return render(request, 'home.html', data)


def add_company_info(request):



    new_company = dict(
        company_name= request.POST['company_name'],
        # open_time= request.POST['open_time'],
        # close_time= request.POST['close_time'],
        address= request.POST['address'],
        state= request.POST['states_dropdown'],
        city= request.POST['company_city'],

        overnight_parking= request.POST.get('overnight_parking', False),
        lumper= request.POST.get('lumper', False),
        facilities= request.POST.get('facilities', False),
        scheduling= request.POST['schedule_dropdown'],
        load_type= request.POST['load_dropdown'],
    )

    if request.POST['company_zip_code'] == '':
        new_company['zip_code'] = None
    else:
        new_company['zip_code'] = int(float(request.POST['company_zip_code']))

    if request.POST['wait_time'] == '':
        new_company['wait_time'] = None
    else:
        new_company['wait_time'] = int(float(request.POST['wait_time']))

    if request.POST['load_time'] == '':
        new_company['load_time'] = None
    else:
        new_company['load_time'] = int(float(request.POST['load_time']))

    CompanyInfoEntry.objects.create(**new_company)
    add_to_web = new_company
    add_to_web['average_wait'] = add_to_web['wait_time']
    del add_to_web['wait_time']
    add_to_web['average_load'] = add_to_web['load_time']
    del add_to_web['load_time']
    CompanyInfo.objects.create(**add_to_web)
    return home(request)


def add_company_form(request):
    data = dict(
        states=STATES_TUPLE,
        schedule_options=SCHEDULING_OPTIONS,
        load_options=LOAD_TYPE_OPTIONS
    )
    return render(request, 'new_company_form.html', data)
