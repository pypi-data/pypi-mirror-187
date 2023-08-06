
from typing import List, Optional, Any, Sequence, Union, Generator

# TODO: replace with interface
from sqlalchemy import Table
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session
import sqlalchemize.select as select

import sessionize.utils.features as features
import sessionize.utils.types as types

Connection = Union[Engine, Session]


def select_records(
    sa_table: Union[Table, str],
    connection: Connection,
    chunksize: Optional[int] = None,
    schema: Optional[str] = None,
    sorted: bool = False,
    include_columns: Optional[Sequence[str]] = None
) -> Union[List[types.Record], Generator[List[types.Record], None, None]]:
    """
    Queries database for records in table.
    Returns list of records in sql table.
    Returns a generator of lists of records if chunksize is not None.
    
    Parameters
    ----------
    sa_table: sa.Table
        SqlAlchemy table mapped to sql table.
    connection: sa.engine.Engine, sa.orm.Session, or sa.engine.Connection
        connection used to query database.
    chunksize: int, default None
        if not None, returns generator of lists of records.
    
    Returns
    -------
    list of sql table records or generator of lists of records.
    """
    table = features._get_table(sa_table, connection, schema=schema)
    if chunksize is None:
        return select_records_all(table, connection, sorted=sorted,
                                  include_columns=include_columns)
    else:
        return select_records_chunks(table, connection, chunksize, sorted=sorted,
                                     include_columns=include_columns)


def select_records_all(
    sa_table: Union[Table, str],
    connection: Connection,
    schema: Optional[str] = None,
    sorted: bool = False,
    include_columns: Optional[Sequence[str]] = None
) -> List[types.Record]:
    """
    Queries database for records in table.
    Returns list of records in sql table.
    
    Parameters
    ----------
    sa_table: sa.Table
        SqlAlchemy table mapped to sql table.
    connection: sa.engine.Engine, sa.orm.Session, or sa.engine.Connection
        connection used to query database.
    
    Returns
    -------
    list of sql table records.
    """
    table = features._get_table(sa_table, connection, schema=schema)
    return select.select_records_all(table, connection, sorted, include_columns)


def select_records_chunks(
    sa_table: Union[Table, str],
    connection:Connection,
    chunksize: int = 2,
    schema: Optional[str] = None,
    sorted: bool = False,
    include_columns: Optional[Sequence[str]] = None
) -> Generator[List[types.Record], None, None]:
    """
    Queries database for records in table.
    Returns a generator of chunksized lists of sql table records.
    
    Parameters
    ----------
    sa_table: sa.Table
        SqlAlchemy table mapped to sql table.
    connection: sa.engine.Engine, sa.orm.Session, or sa.engine.Connection
        connection used to query database.
    chunksize: int
        size of lists of sql records generated.
    
    Returns
    -------
    Generator of lists of sql table records.
    """
    table = features._get_table(sa_table, connection, schema=schema)
    return select.select_records_chunks(table, connection, chunksize, sorted, include_columns)


def select_existing_values(
    sa_table: Union[Table, str],
    connection: Connection,
    column_name: str,
    values: Sequence,
    schema: Optional[str] = None
) -> list:
    """
    Queries database for existing values in table column.
    Returns list of matching values that exist in table column.
    
    Parameters
    ----------
    table: sa.Table
        SqlAlchemy table mapped to sql table.
    records: list[Record]
        list of records to select from.
        Use df.to_dict('records') to convert Pandas DataFrame to records.
    connection: sa.engine.Engine, sa.orm.Session, or sa.engine.Connection
        connection used to query database
    
    Returns
    -------
    List of matching values.
    """
    table = features._get_table(sa_table, connection, schema=schema)
    return select.select_existing_values(table, connection, column_name, values)


def select_column_values(
    sa_table: Union[Table, str],
    connection: Connection,
    column_name: str,
    chunksize: Optional[int] = None,
    schema: Optional[str] = None
) -> Union[list, Generator[list, None, None]]:
    """
    Queries database for vaules in sql table column.
    Returns list of values in sql table column.
    Returns a lists of values.
    Returns a generator of lists of values if chunksize is not None.
    
    Parameters
    ----------
    table: sa.Table
        SqlAlchemy table mapped to sql table.
    column_name: str
        name of sql table column.
    connection: sa.engine.Engine, sa.orm.Session, or sa.engine.Connection
        connection used to query database.
    chunksize: int, default None
        if not None, returns generator of lists of values.
    
    Returns
    -------
    list of sql table column values or generator of lists of values.
    """
    table = features._get_table(sa_table, connection, schema=schema)
    if chunksize is None:
        return select_column_values_all(table, connection, column_name)
    else:
        return select_column_values_chunks(table, connection, column_name, chunksize)


def select_column_values_all(
    sa_table: Union[Table, str],
    connection: Connection,
    column_name: str,
    schema: Optional[str] = None
) -> list:
    """
    Queries database for vaules in sql table column.
    Returns list of values in sql table column.
    Returns a lists of values.
    
    Parameters
    ----------
    table: sa.Table
        SqlAlchemy table mapped to sql table.
    column_name: str
        name of sql table column.
    connection: sa.engine.Engine, sa.orm.Session, or sa.engine.Connection
        connection used to query database.
    
    Returns
    -------
    list of sql table column values.
    """
    table = features._get_table(sa_table, connection, schema=schema)
    return select.select_column_values_all(table, connection, column_name)


def select_column_values_chunks(
    sa_table: Union[Table, str],
    connection: Connection,
    column_name: str,
    chunksize: int,
    schema: Optional[str] = None
) -> Generator[list, None, None]:
    """
    Queries database for vaules in sql table column.
    Returns a generator of lists of values.
    
    Parameters
    ----------
    table: sa.Table
        SqlAlchemy table mapped to sql table.
    column_name: str
        name of sql table column.
    connection: sa.engine.Engine, sa.orm.Session, or sa.engine.Connection
        connection used to query database.
    chunksize: int, default None
        Returns generator of chunksized lists of values.
    
    Returns
    -------
    Generator of chunksized lists of sql table column values.
    """
    table = features._get_table(sa_table, connection, schema=schema)
    return select.select_column_values_chunks(table, connection, column_name, chunksize)


def select_records_slice(
    sa_table: Union[Table, str],
    connection: Connection,
    start: Optional[int] = None,
    stop: Optional[int] = None,
    schema: Optional[str] = None,
    sorted: bool = False,
    include_columns: Optional[Sequence[str]] = None
) -> List[types.Record]:
    """

    start: Starting index where the slicing of table records starts.
    stop: Ending index where the slicing of table records stops. Non-inclusive.

    The index is not necessarily the primary key value.
    0 is always the first record's index.
    -1 is always the last record's index.

    start is optional, is 0 if None
    stop is optional, is the last index + 1 if None.

    """
    table = features._get_table(sa_table, connection, schema=schema)
    return select.select_records_slice(table, connection, start, stop, sorted, include_columns)


def select_record_by_index(
    sa_table: Union[Table, str],
    connection: Connection,
    index: int,
    schema: Optional[str] = None,
    include_columns: Optional[Sequence[str]] = None
) -> types.Record:
    """
    Select a record by index.
    """
    table = features._get_table(sa_table, connection, schema=schema)
    if index < 0:
        row_count = features.get_row_count(table, connection)
        if index < -row_count:
            raise IndexError('Index out of range.') 
        index = select._calc_positive_index(index, row_count)
    records = select_records_slice(table, connection, index, index+1, include_columns=include_columns)
    if len(records) == 0:
        raise IndexError('Index out of range.')
    return records[0]


def select_first_record(
    sa_table: Union[Table, str],
    connection: Connection,
    schema: Optional[str] = None,
    include_columns: Optional[Sequence[str]] = None
) -> Union[dict, None]:
    """
    Select first record in table
    Returns dictionary or
    Returns None if table is empty
    """
    table = features._get_table(sa_table, connection, schema=schema)
    for chunk in select_records_chunks(table, connection,
                                       schema=schema, chunksize=1,
                                       include_columns=include_columns):
        return chunk[0]
    return None


def select_column_values_by_slice(
    sa_table: Union[Table, str],
    connection: Connection,
    column_name: str,
    start: Optional[int] = None,
    stop: Optional[int] = None,
    schema: Optional[str] = None
) -> list:
    """
    Select a subset of column values by slice.
    """
    table = features._get_table(sa_table, connection, schema=schema)
    return select.select_column_values_by_slice(table, connection, column_name, start, stop)


def select_column_value_by_index(
    sa_table: Union[Table, str],
    connection: Connection,
    column_name: str,
    index: int,
    schema: Optional[str] = None
) -> Any:
    """
    Select a column value by index.
    """
    table = features._get_table(sa_table, connection, schema=schema)
    return select.select_column_value_by_index(table, connection, column_name, index)


def select_primary_key_records_by_slice(
    sa_table: Union[Table, str],
    connection: Connection,
    _slice: slice,
    schema: Optional[str] = None,
    sorted: bool = False
) -> List[types.Record]:
    """
    Select primary key values by slice.
    """
    table = features._get_table(sa_table, connection, schema=schema)
    return select.select_primary_key_records_by_slice(table, connection, _slice, sorted)


def select_primary_key_values(
    sa_table: Union[Table, str],
    connection: Connection,
    schema: Optional[str] = None
) -> List[types.Record]:
    table = features._get_table(sa_table, connection, schema=schema)
    return select_primary_key_records_by_slice(table, connection, slice(None, None))


def select_primary_key_record_by_index(
    sa_table: Union[Table, str],
    connection: Connection,
    index: int,
    schema: Optional[str] = None
) -> types.Record:
    """
    Select primary key values by index.
    """
    table = features._get_table(sa_table, connection, schema=schema)
    if index < 0:
        row_count = features.get_row_count(table, connection)
        if index < -row_count:
            raise IndexError('Index out of range.') 
        index = select._calc_positive_index(index, row_count)
    return select_primary_key_records_by_slice(table, connection, slice(index, index+1))[0]


def check_slice_primary_keys_match(
    sa_table: Union[Table, str],
    connection: Connection,
    start: int,
    stop: int,
    records: Sequence[types.Record],
    schema: Optional[str] = None
) -> bool:
    """
    Check if records have matching primary key values to slice of table records
    """
    table = features._get_table(sa_table, connection, schema=schema)
    slice_key_values = select_primary_key_records_by_slice(table, connection, slice(start, stop))
    keys = features.primary_keys(table)
    records_key_values = [{key:record[key] for key in keys} for record in records]

    if len(slice_key_values) != len(records_key_values):
        return False

    for slice_key_value in slice_key_values:
        if slice_key_value not in records_key_values:
            return False

    return True


def check_index_keys_match(
    sa_table: Union[Table, str],
    connection: Connection,
    index: int,
    record: types.Record,
    schema: Optional[str] = None
) -> bool:
    """
    Check if record's primary key values match index table record.
    """
    table = features._get_table(sa_table, connection, schema=schema)
    keys = features.primary_keys(table)
    key_record = select_primary_key_record_by_index(table, connection, index)
    return {key:record[key] for key in keys} == key_record


def select_record_by_primary_key(
    sa_table: Union[Table, str],
    connection: Connection,
    primary_key_value: types.Record,
    schema: Optional[str] = None,
    include_columns: Optional[Sequence[str]] = None
) -> types.Record:
    """
    Select a record by primary key values
    """
    table = features._get_table(sa_table, connection, schema=schema)
    return select.select_record_by_primary_key(table,
                                                     connection,
                                                     primary_key_value,
                                                     include_columns)


def select_records_by_primary_keys(
    sa_table: Union[Table, str],
    connection: Connection,
    primary_keys_values: Sequence[types.Record],
    schema: Optional[str] = None,
    include_columns: Optional[Sequence[str]] = None
) -> List[types.Record]:
    """
    Select the records that match the primary key values
    """
    table = features._get_table(sa_table, connection, schema=schema)
    return select.select_records_by_primary_keys(table,
                                                       connection,
                                                       primary_keys_values,
                                                       schema=schema,
                                                       include_columns=include_columns)


def select_column_values_by_primary_keys(
    sa_table: Table,
    connection: types.SqlConnection,
    column_name: str,
    primary_keys_values: Sequence[types.Record]
) -> list:
    """
    Select multiple values from a column by primary key values
    """
    return select.select_column_values_by_primary_keys(sa_table,
                                                       connection,
                                                       column_name,
                                                       primary_keys_values)


def select_value_by_primary_keys(
    sa_table: Union[Table, str],
    connection: Connection,
    column_name: str,
    primary_key_value: types.Record,
    schema: Optional[str] = None
) -> Any:
    """
    Select a single value from a column by primary key values
    """
    table = features._get_table(sa_table, connection, schema=schema)
    return select.select_value_by_primary_keys(table, connection, column_name, primary_key_value)