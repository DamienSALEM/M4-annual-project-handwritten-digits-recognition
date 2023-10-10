from rest_framework.decorators import api_view
from rest_framework.response import Response
import pymongo
from django.conf import settings
from utils import transform_image_png_to_pixels

my_client = pymongo.MongoClient(settings.DB_NAME)

db_name = my_client['final_project']
collection_name = db_name['interrogate']


@api_view(['POST'])
def interrogate(request):
    image_pixel = transform_image_png_to_pixels(request.data['image'])
    print(image_pixel)
    try:
        collection_name.insert_one(request.data)
        return Response({'status': 200, 'message': 'Interrogation réussie'})
    except:
        return Response({'status': 404, 'message': 'Interrogation échouée'})
