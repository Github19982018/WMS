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
    
@api_view(['POST'])
def approve(request):
    try:
        purchase = dict(request.data)
        val = collection.find_one({'ref':purchase['ref']})
        if ('ref' in purchase) and (not val):
            purchase['status'] = 'pending'
            collection.insert_one(purchase)
            return Response({'data':'success'},status=201)
        elif ('ref' in purchase) and val:
            collection.update_one({'ref':purchase['ref']},{'$set':{'items':purchase['items'], 'purchase':purchase['purchase']}})
            return Response({'data':'success'},status=201)
        else:
            return Response({'invalid order'},status=400)
    except pymongo.errors.InvalidOperation:
        return Response({'error':'error updating data'},status=400)


@api_view(['POST'])
def front_approve(request):
    if request.method == "POST":
        purchase = request.data
        data = (collection.find_one({'ref':purchase['ref']}))
        if data and data['status'] == 'pending':
            url=env('BASE_URL')+'/purchases/purchase/'
            try:
                response = requests.post(url,{'ref':data['ref']})
                if response.status_code == 201:
                    collection.update_one({'ref':purchase['ref']},{'$set':{
                        'status':'approved'
                }})
                    return Response({'data':'updated'},status=201)
                else:
                    return Response({'error':'cant send or update the data on server'},status=400)
            except pymongo.errors.InvalidOperation as message:
                return Response(data=message,status=400)
            except requests.exceptions.ConnectionError:
                return Response({'error':'database Operation failed'},status=501)
            except requests.exceptions.Timeout:
                return Response({'error':'database Operation failed'},status=501)
        else:
            return Response({'error':'invalid order or already updated'},status=404)


