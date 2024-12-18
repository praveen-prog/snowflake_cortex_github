from dataclasses import dataclass
from typing import ClassVar
from src.constants import *

@dataclass
class DataIngestionArtifact:
    DATA_CLEAN_UP_TXT : ClassVar[list[str]]

@dataclass
class DataProcessingArtifact:
    DATA_PROCESS_TXT : ClassVar[list[str]]
