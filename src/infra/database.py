from abc import ABC, abstractmethod
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey

FILE_NAME = 'sqlite:///university.db'
metaData = MetaData()
engine = create_engine(FILE_NAME)

class Database(ABC):
    def __init__(self):
        """initialize the database connection and create the table, and i made sure that the metadataand engine is created only once"""
        self.engine = engine
        self.metadata = metaData
        self.table = self._create_table() 
        self.metadata.create_all(self.engine)   

    @abstractmethod
    def _create_table(self):
        """Child class must return a SQLAlchemy Table"""
        pass

    def insert(self, values: dict) -> None:
        """insert an Item record in the table"""
        with self.engine.begin() as conn:
            conn.execute(self.table.insert().values(**values))

    def select_by_id(self, id: int) -> dict | None:
        """select an Item record by its ID"""
        with self.engine.connect() as conn:
            result = conn.execute(
                self.table.select().where(self.table.c.id == id)
            ).fetchone()

            if result is None:
                return None

            return dict(result._mapping)

    def select_all(self) -> list[dict]: 
        """select all Item records"""
        with self.engine.connect() as conn:
            result = conn.execute(self.table.select()).fetchall()
            return [dict(row._mapping) for row in result]
        
        
    def update_by_id(self, id: int, values: dict) -> None:
        """update an Item record by its ID"""
        with self.engine.begin() as conn:
            conn.execute(
                self.table.update()
                .where(self.table.c.id == id)
                .values(**values)
            )

    def delete_by_id(self, id: int) -> None:
        """delete an Item record by its ID"""
        with self.engine.begin() as conn:
            conn.execute(
                self.table.delete().where(self.table.c.id == id)
            )


class StudentsDB(Database):

    def _create_table(self):
        return Table(
            'students',
            self.metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('first_name', String),
            Column('last_name', String),
            Column('password', String),
            Column('credit_hours', Integer)
        )

class SubjectsDB(Database):

    def _create_table(self):
        return Table(
            "subjects",
            self.metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("name", String, nullable=False),

            Column(
                "student_id", Integer, ForeignKey("students.id"), nullable=False)
        )
        
class AdminsDB(Database):

    def _create_table(self):
        return Table(
            "admins",
            self.metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("first_name", String, nullable=False),
            Column("last_name", String, nullable=False),
            Column("user_name", String, nullable=False),
            Column("password", Integer, nullable=False)
        )
        
    def select_by_username(self, user_name: str) -> dict | None:
        """select an Admin record by its username"""
        with self.engine.connect() as conn:
            result = conn.execute(
                self.table.select().where(self.table.c.user_name == user_name)
            ).fetchone()

            if result is None:
                return None

            return dict(result._mapping)
    
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

