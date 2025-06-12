import os,sys
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from network_security.entity.artifact_entity import ClassificationMetrixArticfacts
from network_security.exception import NetworkSecurityException
from sklearn.metrics import f1_score,precision_score,recall_score

def get_classififcation_score(y_test,y_pred)->ClassificationMetrixArticfacts:
    try:
        if not set(np.unique(y_pred)).issubset({0, 1}):
            y_pred = (np.array(y_pred) >= 0.5).astype(int)
        
        model_f1_score=f1_score(y_test,y_pred)
        model_precision_score=precision_score(y_test,y_pred)
        model_recall_score=recall_score(y_test,y_pred)
        
        classification_metrics=ClassificationMetrixArticfacts(
            f1_score=model_f1_score,
            precision_score=model_precision_score,
            recall_score=model_recall_score
        )
        return classification_metrics
    except Exception as e :
        raise NetworkSecurityException(e,sys)