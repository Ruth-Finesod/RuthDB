from commands.base_command import BaseCommand
from exceptions import *


class Create(BaseCommand):
    def __init__(self, db_name: str, data: str):
        super().__init__(db_name)
        self.table_name = data[0]
        self.columns = data[1]

    def execute(self):
        """
        create table in DB, by creating txt file with columns names
        """
        if self.is_table_exist():
            raise TableAlreadyExistsError(self.table_name)
        with open(f'{self.db_name}/{self.table_name}.txt', 'w') as f:
            f.write(f'{self.columns})')
