# csrf.py

from django.middleware.csrf import get_token

def get_csrf_token(request):
    csrf_token = get_token(request)
    return csrf_token
