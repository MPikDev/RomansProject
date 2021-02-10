from django.shortcuts import render
from .models import CompanyInfo
# Create your views here.

def home(request):
    company_infos = CompanyInfo.objects.all()
    data = {
        'company_infos':company_infos,
    }
    return render(request, 'home.html', data)
