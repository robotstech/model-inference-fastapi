from examples.imagenet_classification_torch.model_service import ModelService


def test_predict():
    with open('n01443537_goldfish.jpeg', 'rb') as file:
        prediction = ModelService.predict(image_files=[file.read()])
        assert prediction[0]["class"].startswith("goldfish")
