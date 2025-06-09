import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from network_security.exception import NetworkSecurityException
from network_security.logging import logging
from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_transformation import DataTransformation
from network_security.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from network_security.entity.config_entity import TrainingPipelineConfig
from network_security.entity.artifact_entity import DataIngestionArtifacts
from network_security.components.data_validation import DataValidation



if __name__=='__main__':
    try:
        training_pipeline_config=TrainingPipelineConfig()
        data_ingestion_config=DataIngestionConfig(training_pipeline_config) 
        data_ingestion=DataIngestion(data_ingestion_config)
        logging.info("Initiate the data ingestion")   
        data_ingestion_artifacts=data_ingestion.initiate_data_ingestion()
        
       
        
        # print(data_ingestion_artifacts)
        # logging.info("data ingestion completed")
        # datavalidationconfig=DataValidationConfig(training_pipeline_config=training_pipeline_config)
        # data_validation=DataValidation(data_ingestion_artifacts=datavalidationconfig,data_validation_config=datavalidationconfig)
        # logging.info("Initiate data validation")
        # data_validation.initiate_data_validation()
        # logging.info("Data validation complete")
        
        data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifacts)
        logging.info("data ingestion completed")
        datavalidationconfig = DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(
            data_ingestion_artifacts=data_ingestion_artifacts,  
            data_validation_config=datavalidationconfig)
        logging.info("Initiate data validation")
        data_validation_artifacts=data_validation.initiate_data_validation()
        logging.info("Data validation complete")
        
        logging.info("Data transformation initiate")
        data_transformation_config=DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation_artifact=DataTransformation(data_validation_artifacts,data_transformation_config)
        print(data_transformation_artifact)
        logging.info("Data tranformation complete")
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)






