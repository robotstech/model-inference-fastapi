from model_inference_fastapi.model_service import ModelService


def test_main():
    assert ModelService.validate() is None
    assert ModelService.predict()[0]["status"] == "Ready to Go!!!"
