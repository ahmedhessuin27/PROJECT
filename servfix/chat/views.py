from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Message
from .serializers import MessageSerializer

@api_view(['GET', 'POST'])
def message_list(request):
    if request.method == 'GET':
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import status
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer

@api_view(['DELETE'])
def message_delete(request, pk):
    try:
        message = Message.objects.get(pk=pk)
    except Message.DoesNotExist:
        return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

    message.delete()
    return Response({'success': 'Message deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


