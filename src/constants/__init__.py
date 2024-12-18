import os
from datetime import date
from dotenv import load_dotenv
from src.exception import snowflakecortexerror
from typing import ClassVar
load_dotenv()


MODEL_NAME : str = "mistral-large2"
os.chdir("../../")
SNOWFLAKE_ACCOUNT : str =   os.environ.get("SNOWFLAKE_ACCOUNT")
CONNECTION_PARAMS : ClassVar[dict[str]] = {
  "account":  os.environ.get("SNOWFLAKE_ACCOUNT"),
  "user": os.environ.get("SNOWFLAKE_USER"),
  "password": os.environ.get("SNOWFLAKE_USER_PASSWORD"),
  "role": os.environ.get("SNOWFLAKE_ROLE"),
  "database": os.environ.get("SNOWFLAKE_DATABASE"),
  "schema": os.environ.get("SNOWFLAKE_SCHEMA"),
  "warehouse": os.environ.get("SNOWFLAKE_WAREHOUSE")
}
GITHUB_TOKEN : str = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO_LINK : str = "https://api.github.com/repos/praveen-prog/docs/branches/main"
GITHUB_OWNER : str = "praveen-prog"
GITHUB_REPO_NAME: str = "docs"
GITHUB_REPO_BRANCH: str = "main"
GITHUB_FILTER_DIRECTORIES : ClassVar[list[str]] = ["content"]
GITHUB_FILTER_EXTENSIONS : ClassVar[list[str]] = [".md"]