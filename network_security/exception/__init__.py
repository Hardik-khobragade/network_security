import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from network_security.logging import logging

class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message=error_message
        _,_,exc_tb=error_details.exc_info()
        
        self.lineno=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename
        
    def __str__(self):
        return "Error occured in python file no.[{0}] in script [{1}] says that [{2}]".format(
            self.lineno,self.file_name, str(self.error_message)
        )
        
if __name__=="__main__":
    try:
        logging.info("Exception block triggered")
        a=1/0
        print('1 divide by 0 is not possible')
    except Exception as e:
        raise NetworkSecurityException(e,sys)
        
        