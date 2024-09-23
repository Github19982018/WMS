from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pymongo
import requests
import environ

env = environ.Env()
environ.Env.read_env()

client = pymongo.MongoClient()
db = client.test_database


# Create your views here.
@api_view(['GET'])
def packages(request):
    collection = db['packages']
    data = collection.find({'status':'pending'})
    return Response(data)

@api_view(['GET'])
def ships(request):
    collection = db['ships']
    data = collection.find({'status':'pending'})
    return Response(data)

@api_view(['GET'])
def package(request,id):
    collection = db['packages']
    data = collection.find_one({'_id':id})
    return Response(data)

@api_view(['GET'])
def ship(request,id):
    collection = db['ships']
    data = collection.find_one({'_id':id})
    return Response(data)
        
        
@api_view(['POST'])
def backend_package_approve(request):
    collection = db['packages']
    if request.method == "POST":
        sale = request.data
        if ('ref' in sale) and (not collection.find_one({'ref':sale['ref']})):
            sale['status'] = 'pending'
            collection.insert_one(sale)
            return Response({'success'})
        else:
            return Response({'invalid data'})

    
        
@api_view(['POST'])
def backend_ship_approve(request):
    collection = db['shipment']
    if request.method == "POST":
        sale = request.data
        if ('ref' in sale) and (not collection.find_one({'ref':sale['ref']})):
            sale['status'] = 'pending'
            collection.insert_one(sale)
            return Response({'success'})
        else:
            return Response({'invalid data'})
    
    
@api_view(['POST'])
def frontend_package_approve(request):
    collection = db['packages']
    if request.method == "POST":
        sale = request.data
        data = (collection.find_one({'ref':sale['ref']}))
        if data:
            url=env('BASE_URL')+'/sales/package_api'
            try:
                requests.post(url,{'ref':data.ref})
                collection.update_one({'ref':sale['ref']},{'$set':{
                    'status':'approved'
                }})
                return Response({'success'})
            except:
                return Response({'Operation failed'})
        else:
            return Response({'invalid data'})

        
@api_view(['POST'])
def frontend_ship_approve(request):
    collection = db['shipment']
    if request.method == "POST":
        sale = request.data
        data = (collection.find_one({'ref':sale['ref']}))
        if data:
            url=env('BASE_URL')+'/sales/ships_api'
            try:
                requests.post(url,{'ref':data.ref, 'status':sale.status})
                collection.update_one({'ref':sale['ref']},{'$set':{
                    'status':sale.status_val
                }})
                return Response({'success'})
            except:
                return Response({'Operation failed'})
        else:
            return Response({'invalid data'})




