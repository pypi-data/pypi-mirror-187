"""
"""
from typing import List, TYPE_CHECKING
from inspect import isfunction

from asyncpg import Record

from .constants import *
from .field import Field
from .table import Table


if TYPE_CHECKING:
    from supersql import Supersql


class Action():
    def __init__(self, query: str, *args, processor = None):
        self.query = {
            'statement': query,
            'arguments': args,
            'processor': processor
        }
        self.successor = None
    
    def print(self):
        statement = self.query.get('statement')
        arguments = self.query.get('arguments')
        return f'{statement}'
    
    def __str__(self):
        statement = self.query.get('statement')
        arguments = self.query.get('arguments')
        processor = self.query.get('processor')
        return f'{statement} {processor()}'


class Query():
    def __init__(self, engine: 'Supersql'):
        self._engine = engine
        self._sql = []
        self._args = []
    
    def __str__(self) -> str:
        return ' '.join(s() for s in self._sql)

    def _conditional(self, condition: Field, param: any, command: str):
        def _():
            if isinstance(condition, str):
                msg = '''
                    To prevent SQL Injection please use parameterized query with string
                    or use Supersql <type, 'Field'> syntax.
                '''
                if param is None: raise ValueError(msg)
                self._args.append(Field.QUOTE(param))
                sql = f'{command} {condition}'
            elif not isinstance(condition, Field):
                msg = f'''
                    Supersql {command} command only accepts <type, 'Field'> or a parameterized
                    string and param second argument.
                '''
                raise ValueError(msg)
            else:
                self._args.append(condition._arg)
                sql = f'''{command} {condition._sql}''' 
            return sql
        self._sql.append(_)
        return self

    def do(self):
        pass

    async def go(self):
        pass

    def _limit_offset(self, value: int, command: str):
        if not isinstance(value, int):
            raise ValueError(f'{command} only accepts integer values')
        self._sql.append(f'''{command} {value}''')

    def AND(self, condition: Field | str, param = None):
        return self._conditional(condition, param, AND)

    def FROM(self, *tables: List[str | int]):
        def _():
            _tables = [Table.COERCE(t) for t in tables]
            return f'''FROM {', '.join(_tables)}'''
        self._sql.append(_)
        return self
    
    def LIMIT(self, limit: int):
        return self._limit_offset(limit, LIMIT)
    
    def OFFSET(self, offset: int):
        return self._limit_offset(offset, OFFSET)

    def OR(self, condition: Field | str, param = None):
        return self._conditional(condition, param, OR)

    def SELECT(self, *fields) -> 'Query':
        """Pythonic interface to SQL SELECT allowing python
        to be used to build SQL queries.

        Parameters:
            fields (List[str | int]): Variable args param that accepts either a string of
            Supersql Field Type.
            Raises an error if a type other than str | Field is used.
        """
        def _():
            _fields = [Field.COERCE(f) for f in fields]
            return f'''SELECT {', '.join(_fields)}'''
        self._sql.append(_)
        return self

    def WHERE(self, condition: Field | str, param = None):
        return self._conditional(condition, param, WHERE)
