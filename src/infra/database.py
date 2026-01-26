from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

FILE_NAME = 'sqlite:///university.db'

class Database:
    def __init__(self):
        self.engine = create_engine(FILE_NAME)
        self.metadata = MetaData()

        self.students = Table('students', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('first_name', String),
            Column('last_name', String),
            Column('password', Integer),
            Column('credit_hours', Integer)
        )

        self.metadata.create_all(self.engine)

    def InsertStatement(self, values: dict) -> None:
        with self.engine.begin() as conn:   
            conn.execute(self.students.insert().values(**values))

    def SelectById(self, id: int)-> list:
        with self.engine.connect() as conn:
            result = conn.execute(
                self.students.select().where(self.students.c.id == id)
            )
            result = result.fetchone()
            if result is None:
                return []
            dict_result = {'id':result[0], 'first_name':result[1],'last_name':result[2],'password':result[3],'credit_hours':result[4]}

            return dict_result

    def UpdateById(self, id: int, values: dict) -> None:
        with self.engine.begin() as conn:
            conn.execute(
                self.students.update()
                .where(self.students.c.id == id)
                .values(**values)
            )
    def DeleteById(self, id: int) -> None:
        with self.engine.begin() as conn:
            conn.execute(
                self.students.delete().where(self.students.c.id == id)
            )