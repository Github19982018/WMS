from django.shortcuts import render,HttpResponse
import pymongo.errors
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pymongo
import requests
from bson.json_util import dumps
import environ

env = environ.Env()
environ.Env.read_env()

client = pymongo.MongoClient()
db = client.wms


# Create your views here.
@api_view(['GET'])
def packages(request):
    collection = db['packages']
    data = collection.find({'status':'pending'})
    return Response(dumps(data))

@api_view(['GET'])
def ships(request):
    collection = db['shipment']
    data = collection.find()
    return Response(dumps(data))

@api_view(['GET'])
def package(request,id):
    collection = db['packages']
    data = collection.find_one({'ref':id})
    return Response(dumps(data))

@api_view(['GET'])
def ship(request,id):
    collection = db['ships']
    data = collection.find_one({'ref':id})
    return Response(dumps(data))
        
        
@api_view(['POST'])
def backend_package_approve(request):
    collection = db['packages']
    if request.method == "POST":
        sale = request.data
        val = collection.find_one({'ref':sale['ref']})
        if ('ref' in sale) and (not val):
            sale['status'] = 'pending'
            collection.insert_one(sale)
            return Response({'success'})
        elif ('ref' in sale) and val:
            collection.update_one({'ref':sale['ref']},{'$set':{'items':sale['items'],'package':sale['package']}})
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
            url=env('BASE_URL')+'/sales/package_api/'
            try:
                res = requests.post(url,{'ref':sale['ref']})
                print(res)
                if res.status_code == 201:
                    res = collection.update_one({'ref':sale['ref']},{'$set':{
                        'status':'approved'
                    }})
                    return Response({'data':'approved successfully'},status=201)
            except requests.exceptions.ConnectionError:
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
            url=env('BASE_URL')+'/sales/ships_api/'
            try:
                res =requests.post(url,{'ref':data['ref'], 'status':sale['status']})
                if res.status_code == 201:
                    collection.update_one({'ref':sale['ref']},{'$set':{
                        'status':sale['status_val']
                    }})
                    return Response({'data':dumps(data)},status=201)
                else:
                    return Response({'error':'Cant update data'},status=403)
                    
            except requests.ConnectionError:
                return Response({'Operation failed'},status=500)
            except pymongo.errors.InvalidOperation:
                return Response({'Operation failed'},status=501)
        else:
            return Response({'invalid data'},status=402)




