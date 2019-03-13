from sqlalchemy import Integer, ForeignKey, String, Column, create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy import inspect
from sqlite3 import Cursor
# from MySQLdb import _mysql

# data = 'mysql://root:magic202@localhost:3306/herbtest'
metadata = MetaData(engine)
Base = declarative_base()   

def init_sqlalchemy(data='mysql://root:magic202@localhost:3306/codexDB'):
    global engine
    engine = create_engine(data)
                            # , echo = True
    
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

class Herb(Base):
    __tablename__ = 'herb'

    id = Column('id', Integer, primary_key=True, nullable=False)
    name = Column(String(60))
    description = Column(String(100))

    attribute_ref = relationship('Attribute', secondary='co_attribute')
    element_ref = relationship('Element', secondary='co_element')
    sign_ref = relationship('Sign', secondary='co_sign')
    planet_ref = relationship('Planet', secondary='co_planet')
    def __repr__(self):
        return "<Herb('%s'')>" % (
        self.name)
 
class Attribute(Base):
    __tablename__ = 'attribute'

    id = Column(Integer, primary_key=True, nullable=False)
    attribute_type = Column(String(60))

    herb_ref = relationship('Herb', secondary='co_attribute')
    def __repr__(self): 
        return "<Attribute('%s'')>" % (
        self.attribute_type)
class Co_attribute(Base):
    __tablename__ = 'co_attribute'

    id = Column(Integer, primary_key = True, nullable = False, autoincrement=True)
    herb_id = Column(Integer, ForeignKey('herb.id'), primary_key=True)
    herb_name = Column(String(60))
    attribute_type = Column(String(60))
    attribute_id = Column(Integer, ForeignKey('attribute.id'), primary_key=True)

    herb = relationship(Herb, backref=backref("herb_attribute_assoc"))
    attribute = relationship(Attribute, backref=backref("attribute_assoc"))
   
class Element(Base):
    __tablename__ = 'element'
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    element_type = Column(String(60))

    herb_ref = relationship('Herb', secondary='co_element')
    def __repr__(self): 
        return "<Element('%s'')>" % (
        self.element_type)
class Co_element(Base):
    # class contains two foreign key columns which are enough to model the many-to-many relationship
    __tablename__ = 'co_element'

    id = Column(Integer, primary_key = True, autoincrement=True)
    herb_id = Column(Integer,  ForeignKey('herb.id'), primary_key=True)
    herb_name = Column(String(60)) 
    ''' ,  ForeignKey('herb.herb_name')'''
    element_type = Column(String(60))
    element_id = Column(Integer, ForeignKey('element.id') , primary_key=True)
    
    #we include these mappers to offer better manipulation of the tables
    herb = relationship(Herb, backref=backref("herb_element_assoc"))
    element = relationship(Element, backref=backref("element_assoc"))

class Sign(Base):
    __tablename__ = 'sign'
    id = Column(Integer, primary_key=True, nullable=False)
    sign_type = Column(String(60))

    herb_ref = relationship('Herb', secondary='co_sign')
    def __repr__(self):
        return "<Sign('%s'')>" % (
        self.sign_type)
class Co_sign(Base):
    __tablename__ = 'co_sign'

    id = Column(Integer, primary_key = True, nullable = False, autoincrement=True)
    herb_id = Column(Integer,  ForeignKey('herb.id'), primary_key=True)
    herb_name = Column(String(60))
    sign_type = Column(String(60))
    sign_id = Column(Integer, ForeignKey('sign.id') , primary_key=True)

    herb = relationship(Herb, backref=backref("herb_sign_assoc"))
    sign = relationship(Sign, backref=backref("sign_assoc"))

class Planet(Base):
    __tablename__ = 'planet'
    id = Column(Integer, primary_key=True, nullable=False)
    planet_type = Column(String(60))

    herb_ref = relationship('Herb', secondary='co_planet')
    def __repr__(self):
        return "<Planet('%s'')>" % (
        self.planet_type)
class Co_planet(Base):
    __tablename__ = 'co_planet'

    id = Column(Integer, primary_key = True, nullable = False, autoincrement=True)
    herb_id = Column(Integer,  ForeignKey('herb.id'), primary_key=True)
    herb_name = Column(String(60))
    planet_type = Column(String(60))
    planet_id = Column(Integer, ForeignKey('planet.id') , primary_key=True)

    herb = relationship(Herb, backref=backref("herb_planet_assoc"))
    planet = relationship(Planet, backref=backref("planet_assoc"))

init_sqlalchemy()
