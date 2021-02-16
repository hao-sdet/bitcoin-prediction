from dataclasses import dataclass


@dataclass(frozen=True)
class MySqlConfiguration:
    address: str
    user: str
    password: str
    database: str
