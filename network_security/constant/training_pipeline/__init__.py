import os 
import sys 
import pandas as pd 
import numpy as np

"""
defining comman constants variable for training pipeline
"""
TRAGET_COLUMN = "Result"
PIPELINE_NAME : str ='NetworkSecurity'
ARTIFACTS_DIR : str ='Artifacts'
FILE_NAME :str = 'phisingData.csv'
TRAIN_FILE_NAME : str='train.csv'
TEST_FILE_NAME: str='test.csv'


SCHEMA_FILE_PATH=os.path.join("data_schema",'schema.yaml')
SAVE_MODEL_DIR=os.path.join('save_model')
MODEL_FILE_NAME : str ="model.pkl"

""" 
Data Ingestion related constants 
"""


DATA_INGESTION_COLLECTOR_NAME: str ="NetworkData"
DATA_INGESTION_DATABASE_NAME: str = "hardikkhobragade78"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR : str =" ingestion"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2



"""
Data Validation related constant 
"""




DATA_VALIDATION_DIR_NAME : str = "data_validation"
DATA_VALIDATION_VALID_DIR : str = "validated"
DATA_VALIDATION_INVALID_DIR : str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR : str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME : str = "report.yaml"

PREPROCESSING_OBJECT_FILE_NAME : str ="preprocessor.pkl"
"""
Data Transformation related constants 

"""

DATA_TRANSFORMATION_DIR_NAME : str ='data_transformation'
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR : str ='transformed'
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR : str ='transformed_object'

DATA_TRANSFORMATION_IMPUTE_PARAMS : dict ={
    
    "missing_values":np.nan,
    "n_neighbors":3,
    "weights":"uniform",
}

"""
Model traning related constant variables
"""

MODEL_TRAINING_DIR_NAME : str ="model_trainer"
MODEL_TRAINING_TRAIN_MODEL_DIR: str ="trained_model"

MODEL_TRAINING_TRAIN_MODEL_NAME: str = "model.pkl"
MODEL_TRAINING_EXPECTED_SCORE: float = 0.6
MODEL_TRAINING_OVERFITTING_UNDERFITTING_THERSHOLD: float  = 0.05


TRAINING_BUCKET_NANE: str = 'network-security144'