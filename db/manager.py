from utils.filters import Field
from .base import db

class Model:
    def __init_subclass__(cls):
        cls._table_name = f"{cls.__name__.lower()}s"
        cls._columns = {
            name: Field(name, py_type)
            for name, py_type in cls.__annotations__.items()
        }
        setattr(cls, "id", Field("id", int))

    @classmethod
    def create_table(cls):
        conn = db.get_connection()
        with conn.cursor() as cur:
            columns = ", ".join(f"{name} {field.sql_type()}" for name, field in cls._columns.items())
            cur.execute(f"CREATE TABLE IF NOT EXISTS {cls._table_name} (id SERIAL PRIMARY KEY, {columns})")
            conn.commit()

    def __init__(self, **kwargs):
        self._values = {"id": None}
        for key, val in kwargs.items():
            setattr(self, key, val)

    def save(self):
        conn = db.get_connection()
        with conn.cursor() as cur:
            values = {name: getattr(self, name) for name in self._columns}
            if self.id:
                set_values = ", ".join(f"{name} = %({name})s" for name in self._columns)
                cur.execute(f"UPDATE {self._table_name} SET {set_values} WHERE id = %(id)s", {"id": self.id, **values})
            else:
                columns = ", ".join(values.keys())
                placeholders = ", ".join(f"%({name})s" for name in values)
                cur.execute(f"INSERT INTO {self._table_name} ({columns}) VALUES ({placeholders}) RETURNING id", values)
                self.id = cur.fetchone()["id"]
            conn.commit()

    @classmethod
    def select(cls, where=None):
        conn = db.get_connection()
        with conn.cursor() as cur:
            if where:
                where_sql, values = where.to_sql()
                query = f"SELECT * FROM {cls._table_name} WHERE {where_sql}"
            else:
                query = f"SELECT * FROM {cls._table_name}"
                values = {}

            cur.execute(query, values)
            return [cls(**row) for row in cur.fetchall()]