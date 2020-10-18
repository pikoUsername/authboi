from src.utils.db_api.basestorage import BaseStorage

from dataclasses import dataclass
from typing import List

@dataclass()
class PostgresConn(BaseStorage):
    pass