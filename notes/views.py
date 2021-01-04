from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Note
from .serializers import NoteSerializer
from constants import AuthConstants


@api_view(['GET'])
def note_api_overview(request):
    api_urls = {
        'List': '/note/',
        'Detail': '/note/<int:pk>',
        'Create': '/note-create/',
        'Update': '/note-update/<int:pk>',
        'Delete': '/note-delete/<int:pk>',
    }
    return Response(api_urls)


@api_view(['GET'])
def note_list(request):
    if request.user.is_authenticated:
        notes = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    err_res = {
        'code': AuthConstants.TOKEN_MISSING,
        'detail': 'No token was provided.'
    }
    return Response(err_res, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def note_detail(request, pk):
    if request.user.is_authenticated:
        try:
            note = Note.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response('Invalid note ID.', status=status.HTTP_404_NOT_FOUND)

        if note.user.id != request.user.id:
            return Response('You can\'t access this note.', status=status.HTTP_401_UNAUTHORIZED)

        serializer = NoteSerializer(note, many=False)
        return Response(serializer.data)

    return Response('You must be logged in.', status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def note_create(request):
    if request.user.is_authenticated:
        request.data['user'] = request.user.id
        serializer = NoteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response('You must be logged in.', status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
def note_update(request, pk):
    if request.user.is_authenticated:
        try:
            note = Note.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response('Invalid note ID.', status=status.HTTP_404_NOT_FOUND)

        if note.user.id != request.user.id:
            return Response('You can\'t access this note.', status=status.HTTP_401_UNAUTHORIZED)

        request.data['user'] = request.user.id
        serializer = NoteSerializer(instance=note, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response('You must be logged in.', status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
def note_delete(request, pk):
    if request.user.is_authenticated:
        try:
            note = Note.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response('Invalid note ID.', status=status.HTTP_404_NOT_FOUND)

        if note.user.id != request.user.id:
            return Response('You can\'t access this note.', status=status.HTTP_401_UNAUTHORIZED)

        note.delete()
        return Response('Note deleted.')

    return Response('You must be logged in.', status=status.HTTP_401_UNAUTHORIZED)
