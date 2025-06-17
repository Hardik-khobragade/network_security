import os,sys
import certifi
import pymongo
import joblib
ca=certifi.where()

from dotenv import load_dotenv

MONGODB_URL=os.getenv('MongoDB_url')

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from network_security.exception import NetworkSecurityException
from network_security.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,Request,File,UploadFile
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from network_security.utils.main_utils.utils import load_object
from network_security.utils.ml_utils.model.estimator import NetworkModel
from network_security.constant.training_pipeline import DATA_INGESTION_COLLECTOR_NAME,DATA_INGESTION_DATABASE_NAME
from uvicorn import run as app_run


client=pymongo.MongoClient(MONGODB_URL,tlsCAFile=ca)
database=client[DATA_INGESTION_DATABASE_NAME]
collector=client[DATA_INGESTION_COLLECTOR_NAME]

from fastapi.staticfiles import StaticFiles
app=FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
origin=["*"]

from fastapi.templating import Jinja2Templates
templates=Jinja2Templates(directory="./templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    
@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
@app.post("/predict")
async def predict_route(request: Request,file: UploadFile = File(...)):
    try:
        df=pd.read_csv(file.file)
        
        preprocesor = joblib.load("final_model/preprocessor.pkl")
        #preprocesor=load_object("final_model//preprocessor.pkl")
        final_model=joblib.load("final_model//model.pkl")
        
        
        network_model = NetworkModel(preprocessor=preprocesor,model=final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
       
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
      
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    except Exception as e:
            raise NetworkSecurityException(e,sys)

    
if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)
    
    