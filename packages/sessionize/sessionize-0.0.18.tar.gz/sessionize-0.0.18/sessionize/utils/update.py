from typing import List, Optional, Union

from sqlalchemy import Table
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session
import sqlalchemize.update as update

import sessionize.utils.types as types
import sessionize.utils.features as features


def update_records_session(
    table: Union[Table, str],
    records: List[types.Record],
    session: Session,
    schema: Optional[str] = None
) -> None:
    """
    Update sql table records from list records.
    Only adds sql records updates to session, does not commit session.
    Sql table must have primary key.
    Do not pass any records that do not already have primary key matches in table.
    
    Parameters
    ----------
    table: sa.Table
        SqlAlchemy table mapped to sql table.
        Use sessionize.engine_utils.get_table to get table.
    records: list[Record]
        list of records to update.
        Use df.to_dict('records') to convert Pandas DataFrame to records.
    session: sa.orm.session.Session
        SqlAlchemy session to add sql updates to.
    schema: str, default None
        Database schema name.
    table_class: DeclarativeMeta, default None
        pass in the table class if you already have it
        otherwise, will query sql for it each time.

    Returns
    -------
    None
    """
    table = features._get_table(table, session, schema=schema)
    update.update_records_session(table, records, session)


def update_records(
    sa_table: Union[Table, str],
    records: List[types.Record],
    engine: Engine,
    schema: Optional[str] = None
) -> None:
    table = features._get_table(sa_table, engine, schema=schema)
    update.update_records(table, records, engine)