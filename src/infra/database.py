from abc import ABC, abstractmethod
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, select, func
from src.infra.security import PasswordHasher

FILE_NAME = 'sqlite:///university.db'
metaData = MetaData()
engine = create_engine(FILE_NAME)
DEFAULT_ADMIN = {
    "first_name": "Admin",
    "last_name": "User",
    "user_name": "admin@example.com",
    "password": PasswordHasher.hash_password("admin123")
}

class Database(ABC):
    def __init__(self):
        self.engine = engine
        self.metadata = metaData
        self.table = self._create_table() 

    @abstractmethod
    def _create_table(self):
        pass

    def insert(self, values: dict) -> None:
        with self.engine.begin() as conn:
            conn.execute(self.table.insert().values(**values))

    def select_by_id(self, id: int) -> dict | None:
        with self.engine.connect() as conn:
            result = conn.execute(
                self.table.select().where(self.table.c.id == id)
            ).fetchone()
            return dict(result._mapping) if result else None

    def select_all(self) -> list[dict]:
        with self.engine.connect() as conn:
            result = conn.execute(self.table.select()).fetchall()
            return [dict(row._mapping) for row in result]

    def update_by_id(self, id: int, values: dict) -> None:
        with self.engine.begin() as conn:
            conn.execute(
                self.table.update().where(self.table.c.id == id).values(**values)
            )

    def delete_by_id(self, id: int) -> None:
        with self.engine.begin() as conn:
            conn.execute(self.table.delete().where(self.table.c.id == id))

    def number_of_records(self) -> int:
        with self.engine.connect() as conn:
            stmt = select(func.count()).select_from(self.table)
            return conn.execute(stmt).scalar()


class StudentsDB(Database):
    def _create_table(self):
        return Table(
            'students',
            self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('first_name', String),
            Column('last_name', String),
            Column('password', String),
            Column('credit_hours', Integer, default=0)
        )


class SubjectsDB(Database):
    def _create_table(self):
        return Table(
            "subjects",
            self.metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("name", String, nullable=False),
            Column("student_id", Integer, ForeignKey("students.id"), nullable=False),
            Column("credit_hours", Integer, nullable=False)
        )

    def select_by_student_id(self, student_id: int) -> list[dict]:
        with self.engine.connect() as conn:
            result = conn.execute(
                self.table.select().where(self.table.c.student_id == student_id)
            ).fetchall()
            return [dict(row._mapping) for row in result]

    def getCreditHours_by_student_id(self, student_id: int) -> int:
        subjects = self.select_by_student_id(student_id)
        return sum(sub["credit_hours"] for sub in subjects) if subjects else 0


class AdminsDB(Database):
    def _create_table(self):
        return Table(
            "admins",
            self.metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("first_name", String, nullable=False),
            Column("last_name", String, nullable=False),
            Column("user_name", String, nullable=False),
            Column("password", String, nullable=False)
        )

    def select_by_user_name(self, user_name: str) -> dict | None:
        with self.engine.connect() as conn:
            result = conn.execute(
                self.table.select().where(self.table.c.user_name == user_name)
            ).fetchone()
            return dict(result._mapping) if result else None

    def ensure_default_admin(self):
        if self.number_of_records() == 0:
            self.insert(DEFAULT_ADMIN)


class CoursesDB(Database):
    def _create_table(self):
        return Table(
            "courses",
            self.metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("name", String, nullable=False),
            Column("code", String, nullable=False),
            Column("credit_hours", Integer, nullable=False)
        )

    def select_by_code(self, code: str) -> dict | None:
        with self.engine.connect() as conn:
            result = conn.execute(
                self.table.select().where(self.table.c.code == code)
            ).fetchone()
            return dict(result._mapping) if result else None
