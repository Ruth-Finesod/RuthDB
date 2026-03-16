import abc
import os
from glob import glob
from typing import List

from exceptions import NoSuchTableError


class BaseCommand:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.table_name = ""

    @abc.abstractmethod
    def execute(self):
        pass

    def is_table_exist(self) -> bool:
        return self.table_name + '.txt' in [os.path.basename(f) for f in glob(f'{self.db_name}/*')]

    def read_data(self) -> bytes:
        if self.is_table_exist():
            with open(f'{self.db_name}/{self.table_name}.txt', 'rb') as f:
                return f.read()
        else:
            raise NoSuchTableError(self.table_name)

    def get_column_names(self) -> tuple[List[str], bytes]:
        data = self.read_data()
        columns = data.split(b')')[0]
        data = data[len(columns) + 1:]
        columns = [value.decode('utf-8').strip(' ').lower() for value in columns.split(b',')]
        return columns, data
