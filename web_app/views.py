from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from web_app.models import ElectroCar, Person
from django.http import HttpResponse, JsonResponse
from web_app.serializers import CarSerializer


class Index(APIView):
    permission_classes = (IsAuthenticated,) 

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

def cars_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        cars = ElectroCar.objects.all()
        serializer = CarSerializer(cars, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CarSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def car_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = ElectroCar.objects.get(pk=pk)
    except ElectroCar.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CarSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CarSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
    
def person_list(request):
    if request.method == 'GET':
        persons = Person.objects.all()
        serializer = CarSerializer(persons, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CarSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    

    

