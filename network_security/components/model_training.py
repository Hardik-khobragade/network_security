import os
import sys 
import mlflow
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from network_security.exception import NetworkSecurityException
from network_security.logging import logging


from network_security.utils.main_utils.utils import save_object,load_object,load_numpy_array_data
from network_security.utils.ml_utils.metric.classification_metric import get_classififcation_score

from network_security.entity.config_entity import ModelTraninerConfig
from network_security.entity.artifact_entity import DataTransformationArtifacts,ModelTraningArtifacts
from network_security.utils.main_utils.utils import evaluate_model
from network_security.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)




class ModelTraner:
    def __init__(self, model_trainer_config:ModelTraninerConfig ,data_transformation_artifacts:DataTransformationArtifacts):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifacts=data_transformation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def track_mlflow(self,best_model,classification_metrics):
        with mlflow.start_run():
            f1_score=classification_metrics.f1_score
            precision_score=classification_metrics.precision_score
            recall_score=classification_metrics.recall_score

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision_score", precision_score)
            mlflow.log_metric("recall_score", recall_score)
        
            mlflow.sklearn.log_model(best_model,'model')
            
            
    def train_model(self, X_train, y_train,X_test,y_test):
        try:
            model = {
                "LinearRegression": LinearRegression(),
                "DecisionTreeClassifier": DecisionTreeClassifier(),
                "KNeighborsClassifier": KNeighborsClassifier(),
                "AdaBoostClassifier": AdaBoostClassifier(),
                "GradientBoostingClassifier": GradientBoostingClassifier(),
                "RandomForestClassifier": RandomForestClassifier()
            }
            
            params = {
                "LinearRegression": {},
                "DecisionTreeClassifier": {
                "criterion": ["gini", "entropy"],
                # "max_depth": [None, 10, 20, 30],
                # "min_samples_split": [2, 5, 10]
                },
                "KNeighborsClassifier": {
                "n_neighbors": [3, 5, 7],
                # "weights": ["uniform", "distance"],
                # "algorithm": ["auto", "ball_tree", "kd_tree", "brute"]
                },
                "AdaBoostClassifier": {
                "n_estimators": [50, 100, 200],
                "learning_rate": [0.01, 0.1, 1.0]
                },
                "GradientBoostingClassifier": {
                # "n_estimators": [100, 150, 200],
                "learning_rate": [0.01, 0.1, 0.2],
                # "max_depth": [3, 5, 7]
                },
                "RandomForestClassifier": {
                "n_estimators": [100, 200, 300],
                "criterion": ["gini", "entropy"],
                "max_depth": [None, 10, 20, 30]
                }
            }
            
            model_report:dict=evaluate_model(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=model,params=params)
            
            best_model_score= max(sorted(model_report.values()))
            
            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            
            best_model=model[best_model_name]
            y_train_pred=best_model.predict(X_train)
            y_test_pred=best_model.predict(X_test)
            
            classification_test_metric=get_classififcation_score(y_test=y_test,y_pred=y_test_pred)
            classification_train_metric=get_classififcation_score(y_test=y_train,y_pred=y_train_pred)
            
            
            #Track experiment with mlflow
            self.track_mlflow(best_model,classification_train_metric)
            self.track_mlflow(best_model,classification_test_metric)
            
            processor=load_object(file_path=self.data_transformation_artifacts.transformed_object_file_path)
            
            model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
            
            os.makedirs(model_dir_path,exist_ok=True)
            
            Network_model=NetworkModel(preprocessor=processor,model=best_model)
            save_object(self.model_trainer_config.trained_model_file_path,obj=Network_model)
            
            model_trainner_artifact=ModelTraningArtifacts(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                                          train_metrics_artifact=classification_train_metric,
                                                          test_metrics_artifact=classification_test_metric)
            logging.info(f"Model Trainer artifacts {model_trainner_artifact}")
            logging.info(f'best model: {best_model_name} and score {best_model_score}')
            
            return model_trainner_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
        
    def initiate_model_trainer(self)->ModelTraningArtifacts:
        try:
            train_file_path=self.data_transformation_artifacts.transformed_train_file_path
            test_file_path=self.data_transformation_artifacts.transformed_test_file_path
            
            #loading train and test array
            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)
            
            
            X_train,y_train,X_test,y_test=(
                
            train_arr[:,:-1],
            train_arr[:,-1],
            test_arr[:,:-1],
            test_arr[:,-1]
            )
            model_trainer_artifact=self.train_model(X_train,y_train,X_test,y_test)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        
        