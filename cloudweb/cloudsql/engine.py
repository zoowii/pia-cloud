# coding: utf8
# 暂时只支持create, insert, select语句
# TODO: 使用ply解析并预编译，以及参数化SQL
from __future__ import print_function, unicode_literals
from core.util import mongo_util
import re
from bson import ObjectId

mongo = mongo_util.get_mongo_db()


class Session(object):
    def __init__(self):
        self.current_database = None

    def change_db(self, db):
        if isinstance(db, str):
            db = Database(db)
        self.current_database = db

    def get_db_name(self):
        if self.current_database is None:
            return None
        else:
            return self.current_database.name


class Database(object):
    """
    demo使用mongodb作为存储后端，
    所有datastore数据库都放到一个mongodb database中
    命名方式：
    数据库名@表名
    """

    def __init__(self, db_name):
        self.name = db_name
        self.db = mongo

    def get_table(self, name):
        return Table(self, name)


class Table(object):
    def __init__(self, database, name):
        self.name = name
        self.col = database.db['%s@%s' % (database.name, name)]

    def find_all(self):
        return self.col.find()

    def get_column(self, name):
        return TableColumn(self, name)

    def find_first(self):
        record = self.col.find_one()
        return record

    def count(self):
        return self.col.count()

    def insert(self, data):
        return str(self.col.insert(data))


class TempTable(Table):
    def __init__(self):
        self.name = None
        self.data = dict()

    def add_column(self, name, column):
        self.data[name] = column

    def list(self):
        data = dict()
        for name in self.data.keys():
            data[name] = self.data.get(name).find_all()
        return data

    def find_all(self):
        rows = []
        for i in range(self.count()):
            row = dict()
            for key in self.data.keys():
                row[key] = self.data.get(key).get(i)
            rows.append(row)
        return rows

    def find_first(self):
        pass  # TODO

    def count(self):
        if len(self.data.keys()) < 1:
            return 0
        c1 = self.data[list(self.data.keys())[0]]
        return c1.count()

    def get(self, column_name):
        return self.data.get(column_name)

    @staticmethod
    def create(cols):
        """
        从形如{'song': TableColumn, 'game': TableColumn}的字典中创建TempTable
        如果已经是Table了，直接返回
        """
        if isinstance(cols, Table):
            return cols
        table = TempTable()
        table.data = cols
        return table


class TableColumn(object):
    """
    列式数据库的列
    """

    def __init__(self, table, name):
        self.name = name
        self.table = table

    def find_all(self):
        records = self.table.find_all()
        try:
            data = [record.get(self.name) for record in records]
            if self.name == '_id':
                data = [str(item) for item in data]
            return data
        except:
            print(records, self.table)

    def count(self):
        return len(self.find_all())

    def get(self, i):
        return self.find_all()[i]


class TempTableColumn(TableColumn):
    """
    临时表的列
    """

    def __init__(self, name=None):
        self.name = name
        self.data = []

    def append(self, item):
        self.data.append(item)

    def find_all(self):
        data = []
        for item in self.data:
            if isinstance(item, ObjectId):
                data.append(str(item))
            else:
                data.append(item)
        return data

    def get(self, i):
        item = self.data[i]
        if isinstance(item, ObjectId):
            return str(item)
        else:
            return item


def make_table_with_columns_and_rows(columns, rows):
    """
    create a table dict with columns and rows
    """
    table = TempTable()
    for i in range(len(columns)):
        col = columns[i]
        if table.get(col) is None:
            table.add_column(col, TempTableColumn())
        l = table.get(col)
        for row in rows:
            l.append(row.get(col))
    return table


def print_table(db_name, table_name):
    table = Table(Database(db_name), table_name)
    records = table.find_all()
    for record in records:
        print(record)


def split_text_before(text, word):
    """
    get the text before word(or None) with the remaining
    eg. get text before ' from '/' where ' keyword with the remaining
    """
    if word is None:
        return [text, '']
    pos = text.find(word)
    if pos < 0:
        return [text, '']
    return [text[:pos], text[pos + len(word):]]


def get_columns_of_table(table):
    record = table.find_first()
    if record is None:
        return []
    return list(record.keys())


def get_size_of_table(table):
    return table.count()
    # return len(table[get_columns_of_table(table)[0]])


def get_rows_of_table(table):
    """
    return rows of table like ['value1', 'value2', 'value3']
    """
    return table.find_all()
    # columns = get_columns_of_table(table)
    # rows = []
    # for i in range(get_size_of_table(table)):
    #     row = []
    #     print(columns)
    #     for col in columns:
    #         row.append(table[col][i])
    #     rows.append(row)
    # return rows


def get_key_rows_of_table(table):
    """
    return rows of table like {'column1':'value1','column2':'value2'}
    """
    return table.find_all()
    # columns = get_columns_of_table(table)
    # rows = []
    # for i in range(get_size_of_table(table)):
    #     row = {}
    #     for col in columns:
    #         row[col] = table[col][i]
    #     rows.append(row)
    # return rows


def where_execute(sql_str):
    """
    return a funtion witch accept a table and return filtered table back
    execute the where sub query.
    just return a function as judgement
    """
    import re

    sql_str = sql_str.strip()
    where_type = 'no_string'
    if sql_str[-1] == "'":
        where_type = 'string'
    identity_re = r'[a-zA-Z0-9\.]+'
    c1 = re.match(identity_re, sql_str).group()
    remaining_str = sql_str[sql_str.find(c1) + len(c1):].strip()
    op = remaining_str[0]
    remaining_str = remaining_str[1:].strip()
    c2 = remaining_str
    if where_type == 'string':
        c2 = remaining_str[1:-1]

    def is_row_match(cols, row, key_row):
        value1 = key_row.get(c1)
        if where_type == 'string':
            value2 = c2
        else:
            value2 = key_row[c2]
        if op == '=':
            return value1 == value2
        elif op == '>':
            return value1 > value2
        else:
            print('error happen in where sub-query')
            return 'error'

    def where_filter(table):
        cols = get_columns_of_table(table)
        rows = get_rows_of_table(table)
        key_rows = get_key_rows_of_table(table)
        result_rows = []
        for i in range(get_size_of_table(table)):
            row = rows[i]
            key_row = key_rows[i]
            if is_row_match(cols, row, key_row):
                result_rows.append(row)
        return make_table_with_columns_and_rows(cols, result_rows)

    return where_filter


def cartesian_product(table1, table2):
    columns1 = get_columns_of_table(table1)
    columns2 = get_columns_of_table(table2)
    columns = []
    columns.extend(columns1)
    columns.extend(columns2)
    rows = []
    rows1 = get_rows_of_table(table1)
    rows2 = get_rows_of_table(table2)
    for row1 in rows1:
        for row2 in rows2:
            row = []
            row.extend(row1)
            row.extend(row2)
            rows.append(row)
    return make_table_with_columns_and_rows(columns, rows)


def from_execute(session, sql_str):
    """
    return a table filtered by where sub-query if exists
    """
    splited_sql = split_text_before(sql_str, ' where ')
    where = None
    table_names = splited_sql[0].strip().split(',')
    table_names = [item.strip() for item in table_names]
    if len(splited_sql[1].strip()) > 0:
        where_sql = splited_sql[1].strip()
        where = where_execute(where_sql)
    database = session.current_database

    if len(table_names) == 1:
        tbl = Table(database, table_names[0])
    elif len(table_names) == 2:
        table1 = Table(database, table_names[0])
        table2 = Table(database, table_names[1])
        tbl = cartesian_product(table1, table2)
    else:
        print('from sub-query only accept one or two table-name')
        return 'error'
    if where is not None:
        tbl = where(tbl)
    return tbl


def do_select_execute(session, sql_str):
    splited_sql = split_text_before(sql_str, ' from ')
    columns = splited_sql[0].split(',')
    columns = [item.strip() for item in columns]
    from_sql = splited_sql[1].strip()
    table = from_execute(session, from_sql)

    def select_func(table):
        if len(columns) == 1 and columns[0] == '*':
            return table
        result_table = {}

        def beautify_column_name(col_name):
            if table.name is not None and col_name.startswith(table.name + '.'):
                return col_name[len(table.name) + 1:]
            else:
                return col_name

        for col in [beautify_column_name(x) for x in columns]:
            result_table[col] = table.get_column(col)
        return result_table

    table = select_func(table)
    table = TempTable.create(table)
    return table.find_all()


def select_execute(session, sql_str):
    select_pos = sql_str.find('select ')
    select_sql = sql_str[(select_pos + len('select ')):]
    return do_select_execute(session, select_sql)


def _get_longest_str(lst):
    longest = None
    for item in lst:
        if longest is None:
            longest = item
        else:
            if len(item) > len(longest):
                longest = item
    return longest


def _group_by_count(lst, count):
    """
    将列表按个数分组，每count个做一组
    """
    now_count = 0
    cur = []
    for item in lst:
        now_count += 1
        cur.append(item)
        if now_count >= count:
            group = cur
            cur = []
            now_count = 0
            yield group
    if len(cur) > 0:
        yield cur


def insert_execute(session, sql_str):
    """
    执行insert语句
    insert into TABLE_NAME values (a=1, b='abc', ...), (), ...
    """
    matched = re.findall(
        r'(\'([^\']|(\\\'))*?\')|((?<!\')[a-zA-Z_][a-zA-Z0-9_]+)|(\d+)|((?<!\')\d*\.\d*([Ee]\d+)?)|(=)|(\()|(\))',
        sql_str)
    tokens = []
    for m in matched:
        token = _get_longest_str(m)
        if token.startswith("'"):
            token = token[1:-1]
        tokens.append(token)
    table_name = tokens[2]
    table = session.current_database.get_table(table_name)
    values = []
    cur_value = []
    value_started = False
    for i in range(4, len(tokens)):
        token = tokens[i]
        if token == '(':
            value_started = True
        elif token == ')':
            value_started = False
            values.append(list(_group_by_count(cur_value, 3)))
            cur_value = []
        else:
            cur_value.append(token)
    ids = []
    for value in values:
        data = dict()
        for item in value:
            data[item[0]] = item[2]
        ids.append(table.insert(data))
    return ids


def update_execute(session, sql_str):
    """
    执行update语句
    update TABLE_NAME set xxx = xxx where ...
    """


def create_execute(session, sql_str):
    """
    执行create database/table xxx语句
    create database xxx暂时等价于use xxx
    create table xxx也可以无视，直接插入即可
    """
    t1 = re.split(r'\s+', sql_str.strip())
    if t1[1] == 'database':
        session.change_db(t1[2])
    elif t1[1] == 'table':
        table = Table(session.current_database, t1[2])
    else:
        raise Exception('unsupported create sql %s' % sql_str)
    return True


def drop_execute(session, sql_str):
    """
    执行drop database/table xxx语句
    """


def use_execute(session, sql_str):
    """
    执行use DB_NAME语句
    """
    sql_str = sql_str.strip()
    db_name = sql_str[3:].strip()
    session.change_db(db_name)
    return True


def get_sql_type(sql_str):
    sql_str = sql_str.strip()
    if sql_str.startswith('create'):
        return 'create'
    elif sql_str.startswith('drop'):
        return 'drop'
    elif sql_str.startswith('insert'):
        return 'insert'
    elif sql_str.startswith('update'):
        return 'update'
    elif sql_str.startswith('use'):
        return 'use'
    elif sql_str.startswith('select'):
        return 'select'
    else:
        raise Exception('Unsupported SQL %s' % sql_str)


sql_type_handler_mapping = {
    'create': create_execute,
    'drop': drop_execute,
    'insert': insert_execute,
    'update': update_execute,
    'use': use_execute,
    'select': select_execute,
}


def squeal(session, sql_str):
    """
    execute sql_str as squeal language
    as the squeal str always starts with select, so do select_execute
    """
    sql_type = get_sql_type(sql_str)
    handler = sql_type_handler_mapping[sql_type]
    return handler(session, sql_str)