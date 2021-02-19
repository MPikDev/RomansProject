from copy import deepcopy
from statistics import mean
from django.shortcuts import render
from .models import CompanyInfo, STATES_TUPLE, SCHEDULING_OPTIONS, LOAD_TYPE_OPTIONS,CompanyInfoEntry
from django.shortcuts import redirect


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
        open_time= request.POST['company_opening_time'],
        close_time= request.POST['company_closing_time'],
        address= request.POST['address'],
        phone= request.POST['company_phone'],
        website_link= request.POST['company_website_link'],
        state= request.POST['states_dropdown'],
        city= request.POST['company_city'],

        overnight_parking= request.POST.get('overnight_parking', False),
        lumper= request.POST.get('lumper', False),
        facilities= request.POST.get('facilities', False),
        scheduling= request.POST['schedule_dropdown'],
        load_type= request.POST['load_dropdown'],
    )
    # import pdb
    # pdb.set_trace()
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

    company_entry = CompanyInfoEntry.objects.create(**new_company)
    add_to_web = new_company
    add_to_web['average_wait'] = add_to_web['wait_time']
    del add_to_web['wait_time']
    add_to_web['average_load'] = add_to_web['load_time']
    del add_to_web['load_time']
    company_info = CompanyInfo.objects.create(**add_to_web)

    company_entry.company_info = company_info
    company_entry.save()

    return redirect('/home')


def add_company_form(request):
    data = dict(
        states=STATES_TUPLE,
        schedule_options=SCHEDULING_OPTIONS,
        load_options=LOAD_TYPE_OPTIONS,
        post_url='save_new_company',
        title='Add New Company Info',
        header='Add New Company Info',
    )
    return render(request, 'new_company_form.html', data)


def edit_company_form(request, **kwargs):
    print("", kwargs['pk'])
    company_pk =  kwargs['pk']
    company = CompanyInfo.objects.get(pk=company_pk)

    data = dict(
        post_url=f'save_edit_company/{company_pk}/',
        title='Edit Company Info',
        header=f'Edit Company Info for {company.company_name}',

        states=STATES_TUPLE,
        schedule_options=SCHEDULING_OPTIONS,
        load_options=LOAD_TYPE_OPTIONS,

        company_name= company.company_name,
        open_time= company.open_time.strftime("%I:%M"),
        close_time= company.close_time.strftime("%I:%M"),

        address= company.address,
        phone= company.phone,
        website_link= company.website_link,
        state= company.state,
        city= company.city,
        zip_code=company.zip_code,
        overnight_parking= company.overnight_parking,
        lumper= company.lumper,
        facilities= company.facilities,
        scheduling= company.scheduling,
        load_type= company.load_type,
    )
    return render(request, 'new_company_form.html', data)


def save_edit_company(request, **kwargs):
    print("", kwargs['pk'])
    company_pk =  kwargs['pk']
    company_info = CompanyInfo.objects.get(pk=company_pk)

    new_company = dict(
        company_info=company_info,
        company_name=request.POST['company_name'],
        open_time=request.POST['company_opening_time'],
        close_time=request.POST['company_closing_time'],
        address=request.POST['address'],
        phone=request.POST['company_phone'],
        website_link=request.POST['company_website_link'],
        state=request.POST['states_dropdown'],
        city=request.POST['company_city'],

        overnight_parking=request.POST.get('overnight_parking', False),
        lumper=request.POST.get('lumper', False),
        facilities=request.POST.get('facilities', False),
        scheduling=request.POST['schedule_dropdown'],
        load_type=request.POST['load_dropdown'],
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

    company_entry = CompanyInfoEntry.objects.create(**new_company)
    add_to_web = new_company

    wait_time_list = CompanyInfoEntry.objects.filter(company_info=company_info).exclude(wait_time=None).values_list('wait_time', flat=True)
    load_time_list = CompanyInfoEntry.objects.filter(company_info=company_info).exclude(load_time=None).values_list('load_time', flat=True)
    if len(wait_time_list) > 0:
        add_to_web['average_wait'] = mean(wait_time_list)
        add_to_web['max_wait'] = max(wait_time_list)
        add_to_web['min_wait'] = min(wait_time_list)
        add_to_web['n_of_wait'] = len(wait_time_list)
    if len(load_time_list) > 0:
        add_to_web['average_load'] = mean(load_time_list)
        add_to_web['max_load'] = max(load_time_list)
        add_to_web['min_load'] = min(load_time_list)
        add_to_web['n_of_load'] = len(load_time_list)

    del add_to_web['wait_time']
    del add_to_web['load_time']
    del add_to_web['company_info']
    CompanyInfo.objects.filter(pk=company_pk).update(**add_to_web)
    return redirect('/home')
