import os
from src.constants import *
from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar


TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

@dataclass
class SetUpConfig:
    MODEL_NAME :  str = MODEL_NAME
    SNOWFLAKE_ACCOUNT : str = SNOWFLAKE_ACCOUNT
    CONNECTION_PARAMS : ClassVar[dict[str]] = CONNECTION_PARAMS
    GITHUB_TOKEN : str = GITHUB_TOKEN
    GITHUB_REPO_LINK : str  = GITHUB_REPO_LINK
    GITHUB_OWNER : str = GITHUB_OWNER
    GITHUB_REPO_NAME: str = GITHUB_REPO_NAME
    GITHUB_REPO_BRANCH : str = GITHUB_REPO_BRANCH
    GITHUB_FILTER_DIRECTORIES : ClassVar[list[str]] = GITHUB_FILTER_DIRECTORIES
    GITHUB_FILTER_EXTENSIONS : ClassVar[list[str]] = GITHUB_FILTER_EXTENSIONS
    

    
