import uuid
from typing import Any

import structlog
from sqlalchemy import create_engine


class OrmClient:
    def __init__(
            self,
            user: str,
            password: str,
            host: str,
            database: str,
            isolation_level: str = "AUTOCOMMIT"
    ) -> None:
        connection_string = f"postgresql://{user}:{password}@{host}/{database}"
        print(connection_string)
        self.engine = create_engine(connection_string, isolation_level=isolation_level)
        self.db = self.engine.connect()
        self.log = structlog.get_logger(self.__class__.__name__).bind(service="db")

    def close_connection(self) -> None:
        self.db.close()

    def send_query(self, query: Any) -> list[Any]:
        print(query)
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event="request",
            query=str(query),
        )
        dataset = self.db.execute(statement=query)
        result = [row for row in dataset]
        log.msg(
            event="response",
            dataset=[dict(row) for row in result],
        )
        return result

    def send_bulk_query(self, query: Any) -> None:
        print(query)
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event="request",
            query=str(query),
        )
        self.db.execute(statement=query)
