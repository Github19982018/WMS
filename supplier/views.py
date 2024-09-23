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
collection = db['supplier']


@api_view(['POST'])
def backend(request):
    if request.method == "POST":
        purchase = request.data
        if ('ref' in purchase) and (not collection.find_one({'ref':purchase['ref']})):
            purchase['status'] = 'pending'
            collection.insert_one(purchase)
            return Response({'success'})
        else:
            return Response({'invalid data'})
    
    
@api_view(['POST'])
def frontend(request):
    if request.method == "POST":
        purchase = request.data
        data = (collection.find_one({'ref':purchase['ref']}))
        if data:
            url=env('BASE_URL')+'/purchase_api'
            try:
                requests.post(url,{'ref':data.ref,'status':purchase.status})
                collection.update_one({'ref':purchase['ref']},{'$set':{
                    'status':purchase.status_val
                }})
                return Response({'success'})
            except:
                return Response({'Operation failed'})
        else:
            return Response({'invalid data'})