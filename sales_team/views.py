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
        try:
            sale = request.data
            val = collection.find_one({'ref':sale['ref']})
            if ('ref' in sale) and (not val):
                sale['status'] = 'pending'
                collection.insert_one(sale)
                return Response({'data':'recived'},status=201)
            elif ('ref' in sale) and val:
                collection.update_one({'ref':sale['ref']},{'$set':{'items':sale['items'],'package':sale['package']}})
                return Response({'data':'updated'},status=201)
            else:
                return Response({'error':'invalid order'},status=400)
        except:
            return Response({'error':'operation failed'},status=500)

@api_view(['POST'])
def package_cancel(request):
    collection = db['packages']
    try:
        purchase = dict(request.data)
        # val = collection.find_one({'ref':{'$in':purchase['ref']}})
        if ('ref' in purchase):
            collection.update_many({'ref':{'$in':purchase['ref']}},{'$set':{'status':'cancelled'}})
            return Response({'data':'cancelled'},status=201)
        else:
            return Response({'error':'invalid order'},status=400)
    except pymongo.errors.PyMongoError:
        return Response({'error':'error updating data'},status=400)
    
@api_view(['POST'])
def ship_cancel(request):
    collection = db['ships']
    try:
        purchase = dict(request.data)
        # val = collection.find({'ref':{'$in':purchase['ref']}})
        if ('ref' in purchase):
            collection.update_many({'ref':{'$in':purchase['ref']}},{'$set':{'status':'cancelled'}})
            return Response({'data':'cancelled'},status=201)
        else:
            return Response({'error':'invalid order'},status=400)
    except:
        return Response({'error':'error updating data'},status=400)

    
        
@api_view(['POST'])
def backend_ship_approve(request):
    collection = db['shipment']
    if request.method == "POST":
        sale = request.data
        val = collection.find_one({'ref':sale['ref']})
        if ('ref' in sale) and (not val):
                sale['status'] = 'pending'
                collection.insert_one(sale)
                return Response({'data':'recived'},status=201)
        elif ('ref' in sale) and val:
            collection.update_one({'ref':sale['ref']},{'$set':{'items':sale['items'],'package':sale['package']}})
            return Response({'data':'updated'},status=201)
        else:
            return Response({'invalid order'})
    
    
@api_view(['POST'])
def frontend_package_approve(request):
    collection = db['packages']
    sale = request.data
    data = (collection.find_one({'ref':sale['ref']}))
    if data: 
        if data['status'] == 'pending':
            url=env('BASE_URL')+'/sales/package_api/'
            try:
                res = requests.post(url,{'ref':sale['ref']})
                if res.status_code == 201:
                    res = collection.update_one({'ref':sale['ref']},{'$set':{
                        'status':'approved'
                    }})
                    return Response({'data':'approved successfully'},status=201)
                else:
                    return Response({'data':'Updation error'},status=403)
            except requests.exceptions.ConnectionError:
                return Response({'Operation failed'},status=500)
        else:
            return Response({'Already updated'},status=403)
    else:
        return Response({'invalid order'},status=404)

        
@api_view(['POST'])
def frontend_ship_approve(request):
    collection = db['shipment']
    sale = request.data
    data = (collection.find_one({'ref':sale['ref']}))
    if data: 
        if data['status'] != 'cancelled':
            url=env('BASE_URL')+'/sales/ships_api/'
            try:
                res =requests.post(url,{'ref':data['ref'], 'status':sale['status']})
                if res.status_code == 201:
                    collection.update_one({'ref':sale['ref']},{'$set':{
                        'status':sale['status_val']
                    }})
                    return Response({'data':dumps(data)},status=201)
                else:
                    return Response({'error':'Cant update data on server'},status=403)
                    
            except requests.ConnectionError:
                return Response({'Operation failed'},status=500)
            except pymongo.errors.InvalidOperation:
                return Response({'Operation failed'},status=501)
        else:
            return Response({'Already cancelled order!'},status=402)
    else:
        return Response({'invalid order or order cancelled'},status=402)


@api_view(['POST'])
def pay(request):
    collection = db['shipment']
    sale = request.data
    data = (collection.find_one({'ref':int(sale['ref'])}))
    if data: 
        if data['status'] != 'cancelled':
            url=env('BASE_URL')+'/sales/sales_api/'
            try:
                res =requests.post(url,{'ref':data['ref'], 'status':sale['status']})
                if res.status_code == 201:
                    collection.update_one({'ref':sale['ref']},{'$set':{
                        'status':sale['status_val']
                    }})
                    return Response({'data':dumps(data)},status=201)
                else:
                    return Response({'error':'Cant update data on server'},status=403)
                    
            except requests.ConnectionError:
                return Response({'Operation failed'},status=500)
            except pymongo.errors.InvalidOperation:
                return Response({'Operation failed'},status=501)
        else:
            return Response({'Already cancelled order!'},status=402)
    else:
        return Response({'invalid order or order cancelled'},status=400)


