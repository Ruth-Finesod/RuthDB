import struct

from commands.base_command import BaseCommand


class Select(BaseCommand):

    def __init__(self, db_name, table_name):
        super().__init__(db_name)
        self.table_name = table_name

    def execute(self) -> list[list[str]]:
        """
        select from th DB the data of the table
        :return: list of the rows as list, first one is the columns names
        """
        columns, data = self.get_column_names()
        select_ls = [columns]
        while data:
            lengths = struct.unpack('H' * len(columns), data[:len(columns) * 2])
            data = data[len(columns) * 2:]
            values = data[:sum(lengths)].decode('utf-8')
            data = data[sum(lengths):]
            ls_values = []
            i = 0
            for l in lengths:
                ls_values.append(values[i: l + i])
                i += l
            select_ls.append(ls_values)
        return select_ls
