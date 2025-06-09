import yaml
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from network_security.logging import logging
from network_security.exception import NetworkSecurityException
import numpy as np
import pickle
import dill 

def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its contents as a dictionary.
    Raises NetworkSecurityException if any error occurs.
    """
    try:
        with open(file_path, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        logging.error(f"Error reading YAML file: {file_path} - {e}")
        raise NetworkSecurityException(e, sys)
    
    
def write_yaml_file(file_path: str, content: object , replace: bool = False) -> None:
    """
    Writes a dictionary to a YAML file.
    Raises NetworkSecurityException if any error occurs.
    """
    try:
        
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
                
        with open(file_path, 'w') as yaml_file:
            yaml.dump(content, yaml_file)
    except Exception as e:
        logging.error(f"Error writing YAML file: {file_path} - {e}")
        raise NetworkSecurityException(e, sys)
    
def save_numpy_array_data(file_path : str,array:np.array):
    try:
        dir_name=os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
    
def save_object(file_path: str, obj: object) -> None:
    """
    Saves a Python object to a file using dill.
    Raises NetworkSecurityException if any error occurs.
    """
    try:
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        logging.error(f"Error saving object to file: {file_path} - {e}")
        raise NetworkSecurityException(e, sys)
    
    