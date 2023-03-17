from examples.imagenet_classification.model_service import ModelService


def test_predict():
    with open('/path/to/image.jpg', 'rb') as file:
        prediction = ModelService.predict(image_files=[file.read()])
        assert prediction[0]["class"] == "dog"
