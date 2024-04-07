# csrf_view.py

from django.http import JsonResponse
from notification.csrf import get_csrf_token  # Import the function to obtain CSRF token

def get_csrf_token_view(request):
    csrf_token = get_csrf_token(request)  # Obtain the CSRF token
    return JsonResponse({'csrf_token': csrf_token})
