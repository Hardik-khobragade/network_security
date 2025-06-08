import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from network_security.exception import NetworkSecurityException
from network_security.logging import logging
from network_security.components.data_ingestion import DataIngestion
from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.config_entity import TrainingPipelineConfig
from network_security.entity.artifact_entity import DataIngestionArtifacts




if __name__=='__main__':
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig) 
        dataingestion=DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")   
        
        dataingestionartifacts=dataingestion.initiate_data_ingestion()
        

        print(dataingestionartifacts)
        
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)






