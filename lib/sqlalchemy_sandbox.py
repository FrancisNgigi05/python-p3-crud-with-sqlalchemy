#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    __tableargs__ = (
        # Ensures that id is a primary key
        PrimaryKeyConstraint(
            'id',
            name='id_pk'),
            # Ensures that Email is unique
            UniqueConstraint(
                'email',
                name='unique_email'),
            # Ensures that new values meet specific criteria
            CheckConstraint(
                'grade BETWEEN 1 AND 12',
                name='grade_between_1_and_12')
    )
    Index('index_name', 'name')

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    def __repr__(self):
        return f"Student {self.id}:"\
            + f"{self.name},"\
            + f"Grade {self.grade}"

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    #use our engine to configure a 'Session' class
    Session = sessionmaker(bind=engine)

    #use 'Sessopm' class to create 'session' object
    session = Session()

    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )

    # session.add(albert_einstein)
    
    
    # Saving multiple records in a single line of code
    session.bulk_save_objects([albert_einstein, alan_turing])
    session.commit()

    # Querying the whole table
    all = [student for student in session.query(Student)]
    print(all)    

    # Querying for the whole table using the all() method
    students = session.query(Student).all()
    print(students)

    # Querrying for the names in the table
    name = [name for name in session.query(Student.name)]
    print(name)

    # Using the order_by() method to all me to sort any column
    students_by_name = [student for student in session.query(Student.name).order_by(Student.name)]
    print(students_by_name)

    # Sorting results in descending order using the desc() method
    students_by_grade_desc = [student for student in session.query(Student.name, Student.grade).order_by(desc(Student.grade))]

    print(students_by_grade_desc)

    # Limititng my results using the limit() method
    oldest_student = [student for student in session.query(Student.name, Student.birthday).order_by(desc(Student.grade)).limit(1)]

    print(oldest_student)

    # Instead of using the limit() method the quicker way is to use the first() method and does not require list interpretation
    oldest_Student = session.query(Student.name, Student.birthday).order_by(desc(Student.grade)).first()
    print(oldest_Student)

    # Using func to give me access to common SQL operations through functions like sum() and count()
    student_count = session.query(func.count(Student.id)).first()
    print(student_count)

    # Using the filter() method to filter the results
    query = session.query(Student).filter(Student.name.like('%Alan%'), Student.grade == 11)

    for record in query:
        print(record.name)

    # Updating data withoud using any method
    for student in session.query(Student):
        student.grade += 1

    session.commit()

    print([(student.name, student.grade) for student in session.query(Student)])


    # Using the update() method to update data
    session.query(Student).update({Student.grade: Student.grade + 1})

    print([(student.name, student.grade) for student in session.query(Student)])

    # Deleting data from the table
    query = session.query(Student).filter(Student.name == "Albert Einstein")

    # Retrieve first matching record as object
    albert_einstein = query.first()

    # Delete record
    session.delete(albert_einstein)

    session.commit()

    # Try to retrieve deleted record
    albert_einstein = query.first()
    
    print(albert_einstein)