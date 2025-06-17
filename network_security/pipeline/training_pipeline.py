import os,sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from network_security.logging import logging
from network_security.exception import NetworkSecurityException
from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_training import ModelTrainer
from network_security.entity.config_entity import TrainingPipelineConfig
from network_security.constant.training_pipeline import TRAINING_BUCKET_NANE
from network_security.cloud.s3_syncer import S3Sync


from network_security.entity.config_entity import(
    ModelTraninerConfig,
    DataTransformationConfig,
    DataIngestionConfig,
    DataValidationConfig
)

from network_security.entity.artifact_entity import (
    DataIngestionArtifacts,
    DataTransformationArtifacts,
    DataValidationArtifacts,
    ModelTraningArtifacts
)



class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()
        self.s3_sync = S3Sync()
        
        
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Start data Ingestion")
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifacts):
        try:
            data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation=DataValidation(data_ingestion_artifacts=data_ingestion_artifact,data_validation_config=data_validation_config)
            logging.info("Initiate the data Validation")
            data_validation_artifact=data_validation.initiate_data_validation()
            logging.info("Data Validation Completed")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifacts):
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Data Transformation Started")
            data_transformation = DataTransformation(data_validation_artifacts=data_validation_artifact,
            data_transformation_config=data_transformation_config)
           
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"Data Transformation complete with artifact :{data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifacts)->ModelTraningArtifacts:
        try:
            self.model_trainer_config: ModelTraninerConfig = ModelTraninerConfig(
                training_pipeline_config=self.training_pipeline_config
            )
            logging.info("Model training initiated")
            model_trainer = ModelTrainer(
                data_transformation_artifacts=data_transformation_artifact,
                model_trainer_config=self.model_trainer_config,
            )

            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info("Model Training completed")
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    ## local artifact is going to s3 bucket    
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NANE}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.artifact_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    ## local final model is going to s3 bucket 
        
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NANE}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.model_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)     
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact)
            model_traning_artifacts=self.start_model_trainer(data_transformation_artifact)
            
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
                       
            return model_traning_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    