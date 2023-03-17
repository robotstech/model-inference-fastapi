from typing import Dict, List, Optional

import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

from model_inference_fastapi.model_service_base import ModelServiceBase
from model_inference_fastapi.utils import convert_image_file_to_numpy_image_array


# derived from https://keras.io/api/applications/
class ModelService(ModelServiceBase):
    __model = ResNet50(weights='imagenet')

    @staticmethod
    def validate(*, data: Optional[List[Dict]] = None, image_files: Optional[List[bytes]] = None):
        if len(image_files) != 1:
            return "There must be at least one image file in image_files"

    @staticmethod
    def predict(*, data: Optional[List[Dict]] = None, image_files: Optional[List[bytes]] = None) -> List[Dict]:
        x = convert_image_file_to_numpy_image_array(image_files[0])

        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        predictions = ModelService.__model.predict(x)

        # decode the results into a list of tuples (class, description, probability)
        # (one such list for each sample in the batch)
        print('Predicted:', decode_predictions(predictions, top=3)[0])

        # Predicted: [(u'n02504013', u'Indian_elephant', 0.82658225), (u'n01871265', u'tusker', 0.1122357),
        # (u'n02504458', u'African_elephant', 0.061040461)]
        return [{"predictions": decode_predictions(predictions, top=3)[0]}]
