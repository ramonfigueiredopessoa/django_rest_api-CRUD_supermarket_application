from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Item
from api.serializers import ItemSerializer


def index(request):
    return HttpResponse("<h1>Django REST API: Supermarket application CRUD</h1>"
                        "<p><a href='http://127.0.0.1:8000/admin'>Admin page</a></p>"
                        "<p><a href='http://127.0.0.1:8000/api'>API</a></p>"
                        "<ol>"
                            "<li><a href='http://127.0.0.1:8000/api/create/'>Create item</a></li>"
                            "<li><a href='http://127.0.0.1:8000/api/all/'>View items</a></li>"
                            "<li>Search items</li>"
                            "<ul>"
                                "<li>Search by item name: GET http://127.0.0.1:8000/api/all/?name=item_name"
                                "<li>Search by category: GET http://127.0.0.1:8000/api/all/?category=category_name"
                                "<li>Search by subcategory: GET http://127.0.0.1:8000/api/all/?subcategory=category_name"
                            "</ul>"
                            "<li>Update item</li>"
                            "<ul>"
                                "<li>PUT http://127.0.0.1:8000/api/update/pk/</li>"
                            "</ul>"
                            "<li>Delete item:</li>"
                            "<ul>"
                                "<li>DELETE http://127.0.0.1:8000/api/delete/pk/</li>"
                            "</ul>"
                        "</ol>")

@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'All items': '/all',
        'Search by item name': '/?name=item_name',
        'Search by category': '/?category=category_name',
        'Search by subcategory': '/?subcategory=category_name',
        'Add': '/create/',
        'Update': '/update/pk/',
        'Delete': '/delete/pk/'
    }

    return Response(api_urls)


@api_view(['POST'])
def add_item(request):
    item = ItemSerializer(data=request.data)

    # validating for already existing data
    if Item.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if item.is_valid():
        item.save()
        return Response(item.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def view_items(request):
    # checking for the parameters from the URL
    if request.query_params:
        items = Item.objects.filter(**request.query_params.dict())
    else:
        items = Item.objects.all()

    # if there is something in items else raise error
    if items:
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_item(request, pk):
    item = Item.objects.get(pk=pk)
    data = ItemSerializer(instance=item, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return Response(status=status.HTTP_202_ACCEPTED)
