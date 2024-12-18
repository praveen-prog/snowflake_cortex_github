import os
import sys
from src.logger import logging
from src.exception import snowflakecortexerror
from src.entity.config_entity import (SetUpConfig)
from src.entity.artifacts_entity import (DataIngestionArtifact,DataProcessingArtifact)
from src.data_ingestion import DataIngestionClass
from src.data_processing import DataProcessingClass
from src.cortex_search_process import CortexSearchClass
from src.cortex_search_retriever import CortexSearchRetriever
from snowflake.snowpark.session import Session

class TrainingPipeline:
    def __init__(self,setupconfig : SetUpConfig =SetUpConfig()):
        self.setupconfig = setupconfig
        self.connection_params = self.setupconfig.CONNECTION_PARAMS
        self.snowpark_session = Session.builder.configs(self.connection_params).create()
        #self.config_entity = SetUpConfig()
        #self.data_ingestion = DataIngestionClass()
        pass
        

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Entered start_data_ingestion method of TrainingPipeline class")
            data_ingestion = DataIngestionClass()
            data_ingestion_artifact = data_ingestion.content_creation()
            logging.info(f"Got the data ingestion artifacts :  {data_ingestion_artifact}")
            logging.info("Exited start_data_ingestion method of TrainingPipeline class")    
            return data_ingestion_artifact
        except Exception as e:
            raise snowflakecortexerror(e,sys)   
          
    def start_data_processing(self,data_ingestion_artifact : DataIngestionArtifact) -> None:
        try:
            logging.info("Entered start_data_processing method of TrainingPipeline class")
            data_processing = DataProcessingClass(data_ingestion_artifact)
            data_processing_artifact = data_processing.semantic_splitting()
            logging.info(f"Data processing artifact is {data_processing_artifact}")
            logging.info("Exited start_data_processing method of TrainingPipeline class")    
            return data_processing_artifact
        except Exception as e:
            raise snowflakecortexerror(e,sys)  
                 
    def start_cortex_search_process(self, setupconfig : SetUpConfig ,data_processing_artifact : DataProcessingArtifact) -> None:    
        try:
            logging.info("Entering load cortex search method of CortexSearch class")
            cortex_search_class = CortexSearchClass(setupconfig=setupconfig,data_processing_artifact=data_processing_artifact)
            cortex_search_class_artifact = cortex_search_class.load_cortex_search()
            logging.info("Exiting load cortex search method of CortexSearch class")

            return cortex_search_class_artifact
        except Exception as e:
            raise snowflakecortexerror(e,sys) 

    def start_cortex_search_retriever(self,query) -> None:
        try:
            snowpark_session = self.snowpark_session
            logging.info("Entering retrieve method of CortexSearchRetriever class")
            cortex_retriever_class = CortexSearchRetriever(session=snowpark_session, limit_to_retrieve= 4)
            cortex_retriever_class_artifact = cortex_retriever_class.tru_lens_integ(query=query)
            logging.info(f"Response is {cortex_retriever_class_artifact}")
            print(f"Response is {cortex_retriever_class_artifact}")
            logging.info("Exiting retrieve method of CortexSearchRetriever class")
            logging.info("Exited start_cortex_search_process method of TrainingPipeline class")
            return cortex_retriever_class_artifact            
        except Exception as e:
            raise snowflakecortexerror(e,sys)     



###################################################################################
    def run_pipeline(self ,query,run_only_search_retriever : bool) -> None:
        try:
            if run_only_search_retriever:
                cortex_search_retriever_artifact = self.start_cortex_search_retriever(query =query)
                return cortex_search_retriever_artifact

            else:
                data_ingestion_artifact = self.start_data_ingestion()
                data_processing_artifact = self.start_data_processing(data_ingestion_artifact)
                cortex_serach_process_artifact = self.start_cortex_search_process(setupconfig=SetUpConfig,data_processing_artifact=data_processing_artifact)
                cortex_search_retriever_artifact = self.start_cortex_search_retriever(query =query)
                return cortex_search_retriever_artifact
        except Exception as e:
            raise snowflakecortexerror(e,sys)  

#obj =  TrainingPipeline()

#obj.run_pipeline()
