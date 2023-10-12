from rest_framework.decorators import api_view
from rest_framework.response import Response
import pymongo
from django.conf import settings
from utils import transform_image_png_to_pixels
from tensorflow.keras.models import load_model
import numpy as np

model = load_model('../../IA/models/cnn_model.h5')

my_client = pymongo.MongoClient(settings.DB_NAME)

db_name = my_client['final_project']
collection_name = db_name['interrogate']


@api_view(['POST'])
def interrogate(request):
    image_pixel = transform_image_png_to_pixels(request.data['image'])
    result = model.predict(image_pixel)
    predicted_classes = np.argmax(result, axis=1)
    predicted_probability = result[0][int(predicted_classes[0])] * 100
    try:
        collection_name.insert_one({'predicted_result': int(predicted_classes[0]), 'image': request.data['image']})
        return Response({'status': 200, 'message': 'Interrogation réussie', 'predictedClasses': predicted_classes[0], 'predictedProbability': predicted_probability})
    except:
        return Response({'status': 404, 'message': 'Interrogation échouée'})
