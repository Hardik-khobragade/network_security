from dataclasses import dataclass

from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts:
    training_file_path: str
    testing_file_path: str
    
    
@dataclass
class DataValidationArtifacts:
    valid_status : bool
    valid_train_file_path : str
    valid_test_file_path : str
    invalid_train_file_path : str
    invalid_test_file_path : str
    drift_report_file_path : str
    
@dataclass
class DataTransformationArtifacts:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str