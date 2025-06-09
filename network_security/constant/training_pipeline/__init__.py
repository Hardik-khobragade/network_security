import os 
import sys 
import pandas as pd 
import numpy as np

"""
defining comman constants variable for training pipeline
"""
TRAGET_COLUMN = "Results"
PIPELINE_NAME : str ='NetworkSecurity'
ARTIFACTS_DIR : str ='Artifacts'
FILE_NAME :str = 'phisingData.csv'
TRAIN_FILE_NAME : str='train.csv'
TEST_FILE_NAME: str='test.csv'

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


SCHEMA_FILE_PATH=os.path.join("data_schema",'schema.yaml')

DATA_VALIDATION_DIR_NAME : str = "data_validation"
DATA_VALIDATION_VALID_DIR : str = "validated"
DATA_VALIDATION_INVALID_DIR : str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR : str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME : str = "report.yaml"
