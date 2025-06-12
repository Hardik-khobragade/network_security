import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from network_security.constant.training_pipeline import SAVE_MODEL_DIR, MODEL_FILE_NAME

from network_security.logging import logging
from network_security.exception import NetworkSecurityException

class NetworkModel:
    def __init__(self,preprocessor,model):
        
        try:
            self.preprocessor=preprocessor
            self.model=model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def predict(self,x):
        try:
            x_transform=self.preprocessor.transform(x)
            y_hat=self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        