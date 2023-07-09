from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])  # @ is a decorators
def getRoute(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    return Response(routes)  # safe = False because safe means response data should be Json objects, then when safe set to False response data can contains python objects / non Json objects and Turn into data list

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)  #gunakan .data agar ListSerializer menjadi Json Serialize or Json object

@api_view(['GET'])
def getRoom(request, pk):
    rooms = Room.objects.get(id=pk)
    serializer = RoomSerializer(rooms, many=False)
    return Response(serializer.data)  #gunakan .data agar ListSerializer menjadi Json Serialize or Json object