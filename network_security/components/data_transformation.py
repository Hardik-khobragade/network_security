import sys,os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from network_security.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTE_PARAMS,TRAGET_COLUMN
from network_security.entity.artifact_entity import DataValidationArtifacts,DataTransformationArtifacts
from network_security.entity.config_entity import DataTransformationConfig
from network_security.exception import NetworkSecurityException
from network_security.logging import logging
from network_security.utils.main_utils.utils import save_numpy_array_data,save_object


class DataTransformation:
    def __init__(self,data_validation_artifacts:DataValidationArtifacts,
                 data_transformation_config:DataTransformationConfig):
        
        try:
            self.data_validation_artifacts=data_validation_artifacts
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)    
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    @classmethod
    def get_tranformation_obj(cls)->Pipeline:
        logging.info(
            "Entered get_data_trnasformer_object method of Trnasformation class"
        )
        try:
           imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTE_PARAMS)
           logging.info(
                f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTE_PARAMS}"
            )
           processor:Pipeline=Pipeline([("imputer",imputer)])
           return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
    def initiate_data_transformation(self)-> DataTransformationArtifacts:
        logging.info('Entereed the data transformation class')
        try:
            logging.info('Started data Transformation')
            train_df=DataTransformation.read_data(self.data_validation_artifacts.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifacts.valid_test_file_path)
            
            ##training dataframe
            input_feature_train_df=train_df.drop(columns=[TRAGET_COLUMN],axis=1)
            target_feature_train_df= train_df[TRAGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)
            
            
            ##testing dataframe
            input_feature_test_df=test_df.drop(columns=[TRAGET_COLUMN],axis=1)
            target_feature_test_df= test_df[TRAGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1,0)
            
            preprocessor=self.get_tranformation_obj()
            
            preprocessor_obj=preprocessor.fit(input_feature_train_df)
            transformed_train_input_feature=preprocessor_obj.transform(input_feature_train_df)
            transformed_test_input_feature=preprocessor_obj.transform(input_feature_test_df)
            
            train_arr=np.c_[transformed_train_input_feature,np.array(target_feature_train_df)]
            test_arr=np.c_[transformed_test_input_feature,np.array(target_feature_test_df)]
            
            #save array
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_obj)
            
            
            data_transformed_artifact=DataTransformationArtifacts(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )

            return data_transformed_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
        