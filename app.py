import sys
import traceback
from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime
from loguru import logger

import model_adapter


logger.remove()  # Removes default handler
logger.add(f"app.log",
           format="<white>{time:YYYY-M-D HH:mm:ss:SS}</white> "
           "<green>{module}:{function}:{line}</green> "
           "<level>{message}</level>")
logger.add(
    sys.stderr, colorize=True, backtrace=True, diagnose=True,
    format="<white>{time:YYYY-M-D HH:mm:ss:SS}</white> "
           "<green>{module}:{function}:{line}</green> "
           "<level>{message}</level>")


class RequestModel(BaseModel):
    # TODO: Add features, add validation
    pass


app = FastAPI()

fe = model_adapter.FeatureExtractor()
sklearn_adapter = model_adapter.SklearnAdapter(
    model_fpath="model/model.pkl",
    label_encoder_path="model/type_label_encoder.pkl"
    )
xgboost_adapter = model_adapter.XgBoostAdapter()


@app.post("/predict")
def predict(wav_file_request: RequestModel, request: Request):
    ip = request.client.host  # Change to 'X-forwarded-from" if using NGINX
    logger.info(f"Request from {ip}")

    try:
        logger.debug("Request file format: {}".format(wav_file_request.file_format))
        now = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        features = fe.extract_features(fpath=fpath)
        return {"response": xgboost_adapter.predict(features)}

    except BaseException as e:
        logger.opt(exception=True).debug("Exception: ".format(e))
        return {"Exception: ": traceback.print_exc()}