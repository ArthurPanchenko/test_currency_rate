import json
import time
import requests

from django.http import JsonResponse

from .models import Check


def get_current_currencies(request):
    last_check = Check.objects.first()
    if last_check and (time.time() - last_check.timestamp.timestamp()) < 10:
        return JsonResponse({'error': 'Checks are too often'})
                       
    response = requests.get('https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_eLOtDeG98fG4WliDOHqmHysU1sSHtz5AUfk656wp&currencies=RUB')
    
    if response.status_code == 200:
        data = response.json()['data']
        rub = data['RUB']

        Check.objects.create(
            value=rub,
        )
        last_checks = Check.objects.values()[:10]
        serialized_last_checks = [check for check in last_checks]
        context = {
            'rub': rub,
            'requests': serialized_last_checks
        }
    
        return JsonResponse(context)
    else:
        return JsonResponse({'error': 'Cant get exchange rate'})
