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
def approve(request):
    try:
        if request.method == "POST":
            purch = dict(request.data)
            if ('ref' in purch) and (not collection.find_one({'ref':purch['ref']})):
                purch['status'] = 'pending'
                collection.insert_one(purch)
                return Response({'success'},status=201)
            else:
                return Response({'invalid data'},status=400)
    except:
        return Response({'error':'error updating data'},status=400)


@api_view(['POST'])
def front_approve(request):
    if request.method == "POST":
        purchase = request.data
        data = (collection.find_one({'ref':purchase['ref']}))
        if data:
            url=env('BASE_URL')+'/purchases/purchase/'
            try:
                response = requests.post(url,{'ref':data['ref']})
                if response.status_code == 201:
                    res = collection.update_one({'ref':purchase['ref']},{'$set':{
                        'status':'approved'
                }})
                    return Response({'data':dumps(res)},status=201)
                else:
                    return Response({'error':'cant update the data'},status=400)
            except pymongo.errors as message:
                return Response(data=message,status=400)
            except requests.exceptions:
                return Response({'error':'Operation failed'},status=404)
        else:
            return Response({'error':'invalid data'},status=404)


