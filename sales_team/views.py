from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pymongo

client = pymongo.MongoClient()
db = client.test_database
collection = db['sales']


# Create your views here.
@api_view(['GET','POST'])
def approve(request):
    if request.method == "POST":
        sale = request.data
        if ('ref' in sale) and (not collection.find_one({'ref':sale['ref']})):
            sale['status'] = 'pending'
            collection.insert_one(sale)
            return Response({'success'})
        else:
            return Response({'invalid data'})
    else:
        
        return Response('get out')



# test1 = {
#     'name':'gemini',
#     'type': 'ai'
# }

# collection.insert_one(test1)

