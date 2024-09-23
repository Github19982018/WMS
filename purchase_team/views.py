from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pymongo
import requests
import environ 
from bson.json_util import dumps

env = environ.Env()
environ.Env.read_env()

client = pymongo.MongoClient()
db = client.test_database
collection = db['purchase']


# Create your views here.
@api_view(['GET'])
def purchases(request):
    data = collection.find({})
    return Response(dumps(data))

@api_view(['GET'])
def purchase(request,id):
    data = collection.find({'ref':id})
    return Response(dumps(data))

@api_view(['POST'])
def approve(request):
    if request.method == "POST":
        test1 = request.data
        if ('ref' in test1) and (not collection.find_one({'ref':test1['ref']})):
            test1['status'] = 'pending'
            collection.insert_one(test1)
            return Response({'success'})
        else:
            return Response({'invalid data'})


@api_view(['POST'])
def front_approve(request):
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


