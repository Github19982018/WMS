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
collection = db['supplier']

@api_view(['GET'])
def purchases(request):
    data = collection.find()
    return Response(dumps(data))

@api_view(['GET'])
def purchase(request,id):
    data = collection.find({'ref':id})
    return Response(dumps(data))


@api_view(['POST'])
def backend(request):
    if request.method == "POST":
        purchase = dict(request.data)
        if ('ref' in purchase) and (not collection.find_one({'ref':purchase['ref']})):
            purchase['status'] = 'pending'
            collection.insert_one(purchase)
            return Response({'success'},status=201)
        else:
            return Response({'invalid data'},status=400)
    
    
@api_view(['POST'])
def frontend(request):
    if request.method == "POST":
        purchase = request.data
        data = (collection.find_one({'ref':purchase['ref']}))
        if data:
            url=env('BASE_URL')+'/purchase_api/'
            try:
                response = requests.post(url,{'ref':data.ref,'status':purchase.status})
                if response.status_code == 201:
                    collection.update_one({'ref':purchase['ref']},{'$set':{
                        'status':purchase.status_val
                    }})
                    return Response({'success'},status=201)
                else:
                    return Response({'error':'cant update the data'},status=400)                    
            except:
                return Response({'Operation failed'},status=404)
        else:
            return Response({'invalid data'},status=404)