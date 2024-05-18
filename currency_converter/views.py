from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests


# Получение всех вариантов валют из стороннего API
@api_view(['GET'])
def get_currency_options(request):
    api_url = "https://api.coingate.com/api/v2/currencies" # URL стороннего API
    response = requests.get(api_url)

    if response.status_code == 200:
        currencies = response.json() 
        # Получаем название и короткое обозначение для фиатных валют (т.е. не включаем криптовалюту)
        fiat_currencies = [{"symbol": currency["symbol"], "title": currency["title"]} for currency in currencies if currency["kind"] == "fiat"]
        return Response(fiat_currencies)  
    else:
        return Response([]) # Пустой массив, если нет доступа к стороннему серверу
    

# Главная страница
def index(request):
    currencies_response = get_currency_options(request) 

    if currencies_response.status_code == 200:
        currencies = currencies_response.data
    else:
        currencies = []

    return render(request, 'index.html', {'currencies': currencies})


# Конвертация валюты
@api_view(['GET'])
def convert(request):
    # Получение данных из формы
    from_currency = request.GET.get('from')
    to_currency = request.GET.get('to')
    value = request.GET.get('value').replace(',', '.')

    api_url = f'https://api.coingate.com/v2/rates/merchant/{from_currency}/{to_currency}' # URL стороннего API

    response = requests.get(api_url)
    rate = float(response.json())
    result = rate * float(value)
    result = round(result, 10)

    return JsonResponse({'result': result})