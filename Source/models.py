__author__ = 'Kostya'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, Date, Integer, ForeignKey, String, DECIMAL, DateTime
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.hybrid import hybrid_property
import datetime

Base = declarative_base()


class Entity(Base):
    __tablename__ = 'Entities'

    id = Column('EntityID', BigInteger, primary_key=True)
    created = Column('Created', Date)
    created_by_user_id = Column('CreatedByUserID', Integer, ForeignKey('Users.UserID'))
    created_by = relationship('User', foreign_keys=[created_by_user_id])

    updated = Column('Updated', Date)
    updated_by_user_id = Column('UpdatedByUserID', Integer, ForeignKey('Users.UserID'))
    updated_by = relationship('User', foreign_keys=[updated_by_user_id])
    deleted = Column('Deleted', Date)

    def __init__(self, user=None):
        self.created = datetime.date.today()
        self.updated = datetime.date.today()
        if type(user) is User:
            self.created_by = user
            self.updated_by = user
        elif isinstance(user, User):
            self.created_by_user_id = user.user_id
            self.updated_by_user_id = user.user_id
        else:
            self.created_by_user_id = user
            self.updated_by_user_id = user


class User(Base):
    __tablename__ = 'Users'

    id = Column('UserID', Integer, primary_key=True)
    entity_id = Column('EntityID', BigInteger, ForeignKey('Entities.EntityID'))
    entity = relationship('Entity', foreign_keys=[entity_id])
    first_name = Column('FirstName', String(20))
    last_name = Column('LastName', String(20))

    @hybrid_property
    def full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    login_id = Column('LoginID', String(20), ForeignKey('Authorizations.Login'))
    login = relationship('Authorization', foreign_keys=[login_id])

    contacts = relationship('ContactInfo')

    def __repr__(self):
        return '<User("%s", "%s")>' % (self.first_name, self.last_name)

    def __init__(self, fname, lname):
        self.first_name = fname
        self.last_name = lname


class Client(User):
    __tablename__ = 'Clients'

    id = Column('ClientID', Integer, primary_key=True)
    user_id = Column('UserID', Integer, ForeignKey('Users.UserID'))

    def __init__(self, fname, lname):
        super(Client, self).__init__(fname, lname)


class Employee(User):
    __tablename__ = 'Employees'

    id = Column('EmployeeID', Integer, primary_key=True)
    user_id = Column('UserID', Integer, ForeignKey('Users.UserID'))
    time_zone = Column('TimeZone', Integer)
    birth_date = Column('BirthDate', Date)

    def __init__(self, fname, lname, time_zone=0, birth_date=None):
        super(Employee, self).__init__(fname, lname)
        self.time_zone = time_zone
        self.birth_date = birth_date


class Authorization(Base):
    __tablename__ = 'Authorizations'

    login = Column('Login', String(20), primary_key=True)
    password = Column('Password', String(40))
    user = relationship('User', uselist=False, backref='Authorizations')

    def __init__(self, login, password):
        self.login = login
        self.password = password


class ContactInfoType(Base):
    __tablename__ = 'ContactInfoTypes'

    id = Column('ContactInfoTypeID', Integer, primary_key=True)
    type_name = Column('ContactInfoTypeName', String(10))

    #enum-like stuff
    skype = 1
    primary_email = 3
    secondary_email = 4
    phone = 5


class ContactInfo(Base):
    __tablename__ = 'ContactInfo'

    contact = Column('Contact', String(40))
    user_id = Column('UserID', Integer, ForeignKey('Users.UserID'), primary_key=True)
    user = relationship('User', foreign_keys=[user_id])

    type_id = Column('ContactInfoTypeID', Integer, ForeignKey('ContactInfoTypes.ContactInfoTypeID'), primary_key=True)
    __contact_type = relationship('ContactInfoType', foreign_keys=[type_id])

    @hybrid_property
    def type_name(self):
        return self.__contact_type.type_name

    def __init__(self, contact_type, contact):
        self.type_id = contact_type
        self.contact = contact


class ProjectStatus(Base):
    __tablename__ = 'ProjectStatuses'

    id = Column('ProjectStatusID', Integer, primary_key=True)
    status_name = Column('StatusName', String(20))

    #enum simulation
    active = 1
    completed = 2
    closed = 3


class Project(Base):
    __tablename__ = 'Projects'

    id = Column('ProjectID', Integer, primary_key=True)

    entity_id = Column('EntityID', BigInteger, ForeignKey('Entities.EntityID'))
    entity = relationship('Entity', foreign_keys=[entity_id])

    client_id = Column('ClientID', Integer, ForeignKey('Clients.ClientID'))
    client = relationship('Client', foreign_keys=[client_id])
    project_start = Column('ProjectStart', Date)
    title = Column('Title', String(100), primary_key=True)

    status_id = Column('ProjectStatusID', Integer, ForeignKey('ProjectStatuses.ProjectStatusID'))
    __status = relationship('ProjectStatus', foreign_keys=[status_id])
    month_payment = Column('MonthPaymentDollars', DECIMAL)

    @hybrid_property
    def status_name(self):
        return self.__status.status_name

    def __init__(self, client, title, start_date, status_id=ProjectStatus.active):
        self.client = client
        self.title = title
        self.project_start = start_date
        self.status_id = status_id
        self.month_payment = 0


class TaskStatus(Base):
    __tablename__ = 'TaskStatuses'

    id = Column('TaskStatusID', Integer, primary_key=True)
    status_name = Column('StatusName', String(20))

    #enum constants
    new = 1
    pushed = 2
    fixed = 3
    reopened = 4
    completed = 5
    cancelled = 6


class Task(Base):
    __tablename__ = 'Tasks'

    id = Column('TaskID', Integer, primary_key=True)

    entity_id = Column('EntityID', BigInteger, ForeignKey('Entities.EntityID'))
    entity = relationship('Entity', foreign_keys=[entity_id])

    project_id = Column('ProjectID', Integer, ForeignKey('Projects.ProjectID'))
    project = relationship('Project', foreign_keys=[project_id])

    title = Column('Title', String(100))

    status_id = Column('TaskStatusID', Integer, ForeignKey('TaskStatuses.TaskStatusID'))
    __status = relationship('TaskStatus', foreign_keys=[status_id])

    pushes = relationship('TaskPush')

    @hybrid_property
    def task_owner_id(self):
        return sorted(self.pushes, key=lambda p: p.date, reverse=True)[0].push_to_employee_id

    @hybrid_property
    def task_owner(self):
        return sorted(self.pushes, key=lambda p: p.date, reverse=True)[0].push_to

    @hybrid_property
    def status_name(self):
        return self.__status.status_name

    def __init__(self, title, status_id=TaskStatus.new):
        self.title = title
        self.status_id = status_id


class TaskPush(Base):
    __tablename__ = 'TaskPushes'

    date = Column('PushDate', DateTime, primary_key=True)

    push_by_employee_id = Column('PushByEmployeeID', Integer, ForeignKey('Employees.EmployeeID'))
    push_by = relationship('Employee', foreign_keys=[push_by_employee_id])

    push_to_employee_id = Column('PushToEmployeeID', Integer, ForeignKey('Employees.EmployeeID'))
    push_to = relationship('Employee', foreign_keys=[push_to_employee_id])

    task_id = Column('TaskID', Integer, ForeignKey('Tasks.TaskID'), primary_key=True)
    task = relationship('Task', foreign_keys=[task_id])

    comment = Column('PushComment', String(2000))

    def __init__(self, comment):
        self.comment = comment
        self.date = datetime.datetime.now()


class Job(Base):
    __tablename__ = 'Jobs'

    id = Column('JobID', BigInteger, primary_key=True)

    entity_id = Column('EntityID', BigInteger, ForeignKey('Entities.EntityID'))
    entity = relationship('Entity', foreign_keys=[entity_id])

    task_id = Column('TaskID', Integer, ForeignKey('Tasks.TaskID'))
    task = relationship('Task', foreign_keys=[task_id])

    description = Column('Description', String(200))
    duration_minutes = Column('DurationMinutes', Integer)

    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        assert duration > 0
        return duration

    def __init__(self, description, duration):
        self.description = description
        self.duration_minutes = duration