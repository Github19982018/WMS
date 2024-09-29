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
        val = collection.find_one({'ref':purchase['ref']})
        if ('ref' in purchase):
            if val:
                collection.update_one({'ref':purchase['ref']},{'$set':{'items':purchase['items'],'package':purchase['package']}})
                return Response({'data':'order updated'},status=201)
            else:
                purchase['status'] = 'pending'
                collection.insert_one(purchase)
                return Response({'data':'order received'},status=201)
        else:
            return Response({'error':'invalid order'},status=400)
    except:
            return Response({'error':'updation failed'},status=400)
        
    
    
@api_view(['POST'])
def frontend(request):
    try:
        purchase = request.data
        data = dict(collection.find_one({'ref':purchase['ref']}))
        if data: 
            if data['status'] != 'cancelled':
                if purchase['status'] in [7,8,9]:
                    url=env('BASE_URL')+'/purchases/supplier/recieve/'
                    status = purchase['status']-6
                else:
                    url=env('BASE_URL')+'/purchases/supplier/'
                    status = purchase['status']
                response = requests.post(url,{'ref':data['ref'],'status':status,'status_val':purchase['status_val']})
                collection.update_one({'ref':purchase['ref']},{'$set':{
                    'status':purchase['status_val']
                }})
                if response.status_code == 201:
                    return Response({'data':'order updated'},status=201)
                else:
                    return Response({'error':'cant update the data'},status=400)                    
            else:
                return Response(data={'error':'already cancelled order!'},status=404)
        else:
            return Response(data={'error':'invalid order'},status=404)
    except requests.ConnectionError:
        return Response(data={'error':'Operation failed'},status=401)
    except pymongo.errors.OperationFailure:
        return Response(data={'error':'Operation failed'},status=402)
        
@api_view(['POST'])
def cancel(request):
    try:
        purchase = dict(request.data)
        val = collection.find_one({'ref':purchase['ref']})
        if ('ref' in purchase) and val:
            collection.update_one({'ref':purchase['ref']},{'$set':{'status':'cancelled'}})
            return Response({'data':'success'},status=201)
        else:
            return Response({'invalid order'},status=400)
    except:
        return Response({'error':'error updating data'},status=400)