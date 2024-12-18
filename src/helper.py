import os
import sys
from logger import logging
from dotenv import load_dotenv
from exception import snowflakecortexerror
from entity.config_entity import SetUpConfig
from snowflake.snowpark.session import Session
from snowflake.cortex import Complete

load_dotenv()

logging.info("Welcome to cortex app")

class SnowflakeConnectClass:
    def __init__(self):
        pass
    
    def connect_snowflake_session(self,setupconfig :  SetUpConfig = SetUpConfig()):
        try:
            self.setupconfig = setupconfig
            self.snowflake_account = self.setupconfig.SNOWFLAKE_ACCOUNT
            self.model_name = self.setupconfig.MODEL_NAME
            logging.info(f"Snowflake Account is {self.snowflake_account }")
            self.connection_params = self.setupconfig.CONNECTION_PARAMS
            logging.info(f"Connection details {self.connection_params}")
            snowpark_session = Session.builder.configs(self.connection_params).create()
            logging.info(f"Connected to snowpark session : {snowpark_session}")
            model_eval = Complete(self.model_name, "how do snowflakes get their unique patterns?")
            logging.info(f"Model testing is {model_eval}")
        except Exception as e:
            raise snowflakecortexerror(e,sys)  


obj = SnowflakeConnectClass()
obj.connect_snowflake_session()

