import json
import pandas as pd
from scipy import stats
from datetime import datetime, date
from django.http import JsonResponse
from .contract import operation
from django.http import HttpResponse


def predict(request):
    get_year = request.GET.get('year')
    get_district = request.GET.get('dict')
    print(get_year, get_district)
    date_now = datetime.today().strftime('%Y')
    data = pd.read_csv('Dataset.csv')

    year = []
    district = []
    litracy = []
    emp = []
    error = []
    for i in range(len(data)):

        if data.iloc[i]['DISTRACTS'] == get_district:
            # print(int(date_now) - int(data.iloc[i]['Years']))
            year.append(int(date_now) - int(data.iloc[i]['YEARS']))
            district.append(data.iloc[i]['DISTRACTS'])
            litracy.append(data.iloc[i]['LITERARCY'])
            emp.append(data.iloc[i]['EMPLOYMENT'])

    x = year
    y = litracy
    z = emp

    no_of_y = int(get_year) - int(date_now)

    get_value = no_of_y

    slope, intercept, r, p, std_err = stats.linregress(x, y)

    lit_rate = slope * get_value + intercept
    emp_rate = find_emp(x, z, get_value)
    context = {"literacy": lit_rate, "employment": emp_rate}

    return JsonResponse(context)


def find_emp(x, z, value):
    slope, intercept, r, p, std_err = stats.linregress(x, z)
    return slope * value + intercept


def deploy(request):
    objDep = operation("0x188F6F7C2F5E4b853950426d9D9D129dCF86C22c",
                       "contractfile/sol2.sol", "sol2.sol", "HTTP://127.0.0.1:7545", "property")
    contaddress = objDep.deploy()

    return HttpResponse(contaddress)


def uploadProperty(request):
    objDep = operation("0x188F6F7C2F5E4b853950426d9D9D129dCF86C22c",
                       "contractfile/sol2.sol", "sol2.sol", "HTTP://127.0.0.1:7545", "property")

    contaddress = "0x8211A8fea8e677c9e28995222B4edb2d2c940bE2"
    privatkey = "c80c08f9c24b201ff48ec3c0f872d8921821176fa0987bdd2f009235d8b82388"
    newowneraddress = "0x278c7FCE6F142E3cA0DD61ce8D757ecd459De068"
    landid = 90
    landaddress = "bhara kahu isb"
    try:
        result = objDep.uploadProperty(
            contaddress, privatkey, landid, newowneraddress, landaddress)
    except Exception as e:
        result = e

    return HttpResponse(result)


def propertyDetail(request):
    objDep = operation("0x188F6F7C2F5E4b853950426d9D9D129dCF86C22c",
                       "contractfile/sol2.sol", "sol2.so0x8211A8fea8e677c9e28995222B4edb2d2c940bE20x8211A8fea8e677c9e28995222B4edb2d2c940bE2l", "HTTP://127.0.0.1:7545", "property")
    contaddress = "0x8211A8fea8e677c9e28995222B4edb2d2c940bE2"
    landid = 90

    value=objDep.getPropertyDetail(contaddress,landid)
    return HttpResponse(value)



def transferProperty(request):
    objDep = operation("0x278c7FCE6F142E3cA0DD61ce8D757ecd459De068",
                       "contractfile/sol2.sol", "sol2.sol", "HTTP://127.0.0.1:7545", "property")

    contaddress = "0x8211A8fea8e677c9e28995222B4edb2d2c940bE2"
    privatkey = "f0a6a8fbcfe1e200ef47ac16b6d50517efafe5f8aadaae31372b4d60c2dcd9af"
    newowneraddress = "0x3090b9fE3C0E0b364fcAf8B6B5C67c61dbb44110"
    landid = 90
 
    try:
        result = objDep.transfer(
            contaddress, privatkey, landid, newowneraddress)
    except Exception as e:
        result = e

    return HttpResponse(result)