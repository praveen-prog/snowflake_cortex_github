import os
import sys
import re
import nest_asyncio
from llama_index.readers.github import GithubRepositoryReader, GithubClient
from src.logger import logging
from dotenv import load_dotenv
from src.exception import snowflakecortexerror
from src.entity.config_entity import SetUpConfig
from src.entity.artifacts_entity import DataIngestionArtifact
import requests

load_dotenv()
nest_asyncio.apply()


logging.info("Entered into GitHub Connection")

class DataIngestionClass:
    def __init__(self):
        pass
    def connect_github(self,setupconfig : SetUpConfig = SetUpConfig()) -> list:
        try:
            self.setupconfig = setupconfig
            logging.info("Fetching github token")  
            print("Fetching token")  
            self.github_token = setupconfig.GITHUB_TOKEN
            self.github_repo_link = setupconfig.GITHUB_REPO_LINK
            self.github_owner = setupconfig.GITHUB_OWNER
            self.github_repo_name = setupconfig.GITHUB_REPO_NAME
            self.github_repo_branch = setupconfig.GITHUB_REPO_BRANCH
            self.github_filter_directories = setupconfig.GITHUB_FILTER_DIRECTORIES
            self.github_filter_extensions = setupconfig.GITHUB_FILTER_EXTENSIONS
            # Replace <your_github_token> with your token
            headers = {"Authorization": self.github_token }
            logging.info("GitHub token fetched successfully")
            response = requests.get(self.github_repo_link , headers=headers)
            if response.status_code == 200:
                logging.info(f"Branch data: {response.json()}")                
            else:
                logging.info(f"Error: {response.status_code}, {response.json()}")

            github_client = GithubClient(github_token=self.github_token, verbose=False)
            logging.info(f"Connected to GitHub Client : {github_client}")

            reader = GithubRepositoryReader(
                github_client=github_client,
                owner=self.github_owner,
                repo=self.github_repo_name,
                use_parser=False,
                verbose=False,
                filter_directories=(
                self.github_filter_directories,GithubRepositoryReader.FilterType.INCLUDE,
                                    ),
                filter_file_extensions=(
                    self.github_filter_extensions,GithubRepositoryReader.FilterType.INCLUDE,
                                        )
                )
            logging.info(f"GitHub Reader is : {reader}")
            documents = reader.load_data(branch=self.github_repo_branch)
            logging.info(f"Github documents read completed {self.github_repo_branch}")
            logging.info(f"type of documents AAAAA: {type(documents)}")

            return documents

        except Exception as e:
            raise snowflakecortexerror(e,sys)  
        
    def clean_up_text(self,content: str) -> str:
        try:
            """
            Remove unwanted characters and patterns in text input.

            :param content: Text input.

            :return: Cleaned version of original text input.
            """

            # Fix hyphenated words broken by newline
            content = re.sub(r"(\w+)-\n(\w+)", r"\1\2", content)

            unwanted_patterns = ["---\nvisible: false", "---", "#", "slug:"]
            for pattern in unwanted_patterns:
                content = re.sub(pattern, "", content)

            # Remove all slugs starting with a \ and stopping at the first space
            content = re.sub(r"\\slug: [^\s]*", "", content)

            # normalize whitespace
            content = re.sub(r"\s+", " ", content)
            return content
        except Exception as e:
            raise snowflakecortexerror(e,sys)   
    
    def content_creation(self) -> DataIngestionArtifact:
        try:
            logging.info("Entered content_creation method of DataIngestion Class")
            documents : list = self.connect_github()
            cleaned_documents = []

            for d in documents:
                #logging.info(f"Extracted Text value is BBBBBB: {d}")
                cleaned_text = self.clean_up_text(d.text)
                d.text = cleaned_text
                cleaned_documents.append(d)   
            logging.info("Exited content_creation method of DataIngestion Class")
            return cleaned_documents 
        except Exception as e:
            raise snowflakecortexerror(e,sys)       


#obj =  DataIngestionClass()
#obj.clean_up_text()
