import re
from collections import OrderedDict


class StringTableParser(object):
    """A String table parser provide facility to parse data
    in python dictionary.

    for example,
    below data is sotored in some file called data.txt:
    BLADE#  NAME  B0    B1
    1       LC01  25    27
    2       LC02  26    26

    parser = StringTableParser(data_file='data2.txt')
    parser.generate_column_table()
    print parser.parsed_data

    result:
    OrderedDict([
                ('blade', ['1', '2']),
                ('name', ['lc01', 'lc02']),
                ('b0', ['25', '26']),
                ('b1', ['27', '26'])
    ])

    parser.generate_row_table('name')
    print parser.parsed_data

    result:
    OrderedDict([
                ('lc01', OrderedDict([('blade', '1'),
                                      ('name', 'lc01'),
                                      ('b0', '25'),
                                      ('b1', '27')])),
                ('lc02', OrderedDict([('blade', '2'),
                                      ('name', 'lc02'),
                                      ('b0', '26'),
                                      ('b1', '26')]))
    ])


    see the difference between column based parsing and row based parsing
    """

    def __init__(self, data_file=None, data_list=None, headers_row=1):
        """param: data_file: location of the file which hold valid
                             string table
                  data_list: alternative to file, a list of lines of
                             string table
                  headers_row: integer that define how many rows in data
                               is for heading. defaul is 1.
        """
        self.data = None
        if data_file:
            with open(data_file, 'r') as f:
                self.data = f.readlines() or data_list

        if self.data is None:
            raise ValueError("Provide 'data_file' of 'data_list'")

        self.headers_row = headers_row
        self.parsed_data = OrderedDict()

    def _clean(self, string):
        """remove unwanted charector form string or replace with usabel"""
        return string.lower().replace('#', '').replace('(', '_').replace(
            ')', '')

    def _transform_dict(self, key):
        """allow to manupulate table based on assinged key"""
        new_dict = OrderedDict()
        for idx, v in enumerate(self.parsed_data[key]):
            new_dict[v] = row_data = OrderedDict()
            for k in self.parsed_data.keys():
                row_data[k] = self.parsed_data[k][idx]
        self.parsed_data = new_dict

    def generate_column_table(self):
        """This method is responsible for generating the python object
        this is untransformed data.

        table get generated in dictionary where table's header is key and value is
        list of column data
        """
        search = re.finditer(r'[\w#()]+', self.data[0])
        headers = []
        for tag in search:
            key = self._clean(tag.group())
            headers.append(key)

            self.parsed_data[key] = col_data = []
            for line in self.data[self.headers_row:]:
                val = re.match(r'[\w()-]+', line[tag.start():])
                if val is None:
                    val = 0
                else:
                    val = self._clean(val.group())

                col_data.append(val)

    def generate_row_table(self, datastore):
        """This method parse text table into row table in dictionary form.
        param: datastore: defines which column should be user as key and
                          values will be key, value pairs of other column"""
        self.generate_column_table()
        self._transform_dict(datastore)


parser = StringTableParser(data_file='data2.txt')
parser.generate_row_table('name')
print parser.parsed_data
