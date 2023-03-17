import json
import sys
from typing import Dict, List, Optional

import uvicorn
from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel

from model_inference_fastapi.model_service import ModelService

app = FastAPI()


class JsonData(BaseModel):
    data: List[Dict]

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


# Define the main route
@app.get('/')
def root_route():
    return {'error': 'Use GET /prediction instead of the root route!'}


# Define the /prediction route
@app.post('/predict/', response_model=List[Dict])
async def prediction_route(json_data: Optional[JsonData] = None, image_files: Optional[List[UploadFile]] = None):
    _files = []
    data = json_data.data or list()
    image_files = image_files or list()

    if not (image_files or data):
        raise HTTPException(status_code=400, detail=f'files and data can not be empty')

    try:
        for file in image_files:
            # Ensure that this is an image
            if file.content_type.startswith('image/') is False:
                raise HTTPException(status_code=400, detail=f'File \'{file.filename}\' is not an image.')

            # Read image contents
            contents = await file.read()
            _files.append(contents)

        if err := ModelService.validate(data=data, image_files=_files):
            raise HTTPException(status_code=400, detail=err)

        response = ModelService.predict(data=data, image_files=_files)
        return response

    except:
        e = sys.exc_info()[1]
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/ping")
async def ping():
    return "pong"

