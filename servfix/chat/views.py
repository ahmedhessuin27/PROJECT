from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import ChatRequest, Notification
from django.contrib.auth.models import User

def send_chat_request(request, receiver_id):
    sender = request.user
    receiver = get_object_or_404(User, pk=receiver_id)
    if ChatRequest.objects.filter(sender=sender, receiver=receiver).exists():
        return JsonResponse({'message': 'You have already sent a request to this user.'}, status=400)
    else:
        ChatRequest.objects.create(sender=sender, receiver=receiver)
        Notification.objects.create(user=receiver, message=f'You have a new chat request from {sender.username}.')
        return JsonResponse({'message': 'Chat request sent successfully.'})

def accept_chat_request(request, request_id):
    chat_request = get_object_or_404(ChatRequest, pk=request_id)
    if chat_request.receiver == request.user:
        chat_request.service_provider_accepted = True
        chat_request.save()
        Notification.objects.create(user=chat_request.sender, message=f'{request.user.username} accepted your chat request.')
        return JsonResponse({'message': 'Chat request accepted.'})
    else:
        return JsonResponse({'message': 'You are not authorized to accept this chat request.'}, status=403)

