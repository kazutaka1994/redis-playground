from psycopg2 import pool
from psycopg2.extras import RealDictCursor

from ..config import PostgresConfig
from ..models import User
from .base import UserRepositoryInterface


class PostgresUserRepository(UserRepositoryInterface):
    def __init__(self, config: PostgresConfig):
        self.config = config
        self.pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            host=config.host,
            port=config.port,
            database=config.database,
            user=config.user,
            password=config.password,
        )

    def __del__(self):
        if hasattr(self, "pool") and self.pool:
            self.pool.closeall()

    def get_by_id(self, user_id: int) -> User | None:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT id, name, email, created_at FROM users WHERE id = %s", (user_id,)
                )
                row = cur.fetchone()
                return User(**dict(row)) if row else None
        finally:
            self.pool.putconn(conn)

    def get_by_email(self, email: str) -> User | None:
        conn = self.pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT id, name, email, created_at FROM users WHERE email = %s", (email,)
                )
                row = cur.fetchone()
                return User(**dict(row)) if row else None
        finally:
            self.pool.putconn(conn)
