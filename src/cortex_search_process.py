import os
import sys
import snowflake.connector
from tqdm.auto import tqdm
from dotenv import load_dotenv
from snowflake.snowpark.session import Session
from src.logger import logging
from src.exception import snowflakecortexerror
from src.entity.config_entity import SetUpConfig
from src.entity.artifacts_entity import  DataProcessingArtifact

load_dotenv()

class CortexSearchClass:
    def __init__(self,setupconfig : SetUpConfig, data_processing_artifact : DataProcessingArtifact):
        try:
            self.setupconfig = setupconfig
            self.data_processing_artifact = data_processing_artifact
        except Exception as e:
            raise snowflakecortexerror(e,sys) 

    def load_cortex_search(self) -> str:
        try:
            logging.info("Connecting to snowflake")
            self.connection_params = self.setupconfig.CONNECTION_PARAMS
            #print(f"CONNECTION { self.connection_params }")
            self.data_process_text = self.data_processing_artifact
            #print(f"data processing artifact { self.data_process_text} ")
            snowflake_connector = snowflake.connector.connect(**self.connection_params)
            logging.info("Connected to snowflake successuflly")
            cursor = snowflake_connector.cursor()
            logging.info("Creatng process table")
            cursor.execute("CREATE OR REPLACE TABLE streamlit_docs(doc_text VARCHAR)")
            logging.info("Created process table")
            logging.info("Insert the data into the table")
            for curr in tqdm(self.data_process_text):
                #logging.info(f"streamlit cursor CCCCC value is  {curr}")
                cursor.execute("INSERT INTO streamlit_docs VALUES (%s)", curr.text)
            logging.info("Inserted the data into the table")
            logging.info("Creating the cortex search service")
            cursor.execute("""
                           CREATE OR REPLACE CORTEX SEARCH SERVICE LLMOPS_DB.LLMOPS_SCHEMA.LLMOPS_CORTEX_SEARCH_SERVICE ON 
                           doc_text WAREHOUSE = LLMOPS_WH_M TARGET_LAG = '1 hour' AS 
                           ( SELECT doc_text FROM LLMOPS_DB.LLMOPS_SCHEMA.streamlit_docs);
                           """)
            logging.info("Created the cortex search service successfully")
            return None    

        except Exception as e:
            raise snowflakecortexerror(e,sys)



