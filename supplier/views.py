import pymongo.errors
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pymongo
import requests
import environ
from bson.json_util import dumps

env = environ.Env()
environ.Env.read_env()

client = pymongo.MongoClient()
db = client.wms
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
    try:
        purchase = dict(request.data)
        if ('ref' in purchase) and (not collection.find_one({'ref':purchase['ref']})):
            purchase['status'] = 'pending'
            collection.insert_one(purchase)
            return Response({'data':'success'},status=201)
        else:
            return Response({'error':'invalid data'},status=400)
    except:
            return Response({'error':'failed'},status=400)
        
    
    
@api_view(['POST'])
def frontend(request):
    if request.method == "POST":
        purchase = request.data
        data = dict(collection.find_one({'ref':purchase['ref']}))
        if data:
            url=env('BASE_URL')+'/purchases/supplier/'
            try:
                response = requests.post(url,{'ref':data['ref'],'status':purchase['status'],'status_val':purchase['status_val']})
                collection.update_one({'ref':purchase['ref']},{'$set':{
                    'status':purchase['status_val']
                }})
                if response.status_code == 201:
                    return Response({'data':'order updated'},status=201)
                else:
                    return Response({'error':'cant update the data'},status=400)                    
            except requests.ConnectionError:
                return Response(data={'error':'Operation failed'},status=401)
            except pymongo.errors.OperationFailure:
                return Response(data={'error':'Operation failed'},status=402)
        else:
            return Response(data={'error':'invalid data'},status=404)