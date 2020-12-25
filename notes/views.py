from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Note
from .serializers import NoteSerializer


@api_view(['GET'])
def note_api_overview(request):
    api_urls = {
        'List': '/note/',
        'Detail': '/note/<int:pk>',
        'Create': '/note-create/',
        'Update': '/note-update/',
        'Delete': '/note-delete/',
    }
    return Response(api_urls)


@api_view(['GET'])
def note_list(request):
    notes = Note.objects.all().order_by('-timestamp')
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def note_detail(request, pk):
    try:
        note = Note.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response('Invalid note ID.', status=status.HTTP_404_NOT_FOUND)
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def note_create(request):
    serializer = NoteSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def note_update(request, pk):
    try:
        note = Note.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response('Invalid note ID.', status=status.HTTP_404_NOT_FOUND)

    serializer = NoteSerializer(instance=note, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def note_delete(request, pk):
    try:
        note = Note.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response('Invalid note ID.', status=status.HTTP_404_NOT_FOUND)

    note.delete()
    return Response('Note deleted.')
