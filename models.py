# notes on the venv and start up
# mac:
#     python3 -m venv env
#     source ./env/bin/activate
    
# Windows: python -m venv env
# .\env\Scripts\activate

# Both:
#     pip install requests
#     pip freeze > requirements.txt

# reminders
# git init 
# git add .  
# git commit -m 'Initial commit'
# git branch -M main
# git remote add origin https://github.com/CurtisONeal/<name>.git
# git push -u origin main

# reminder for second commit.... if you just tried git push
# git push --set-upstream origin main


# https://teamtreehouse.com/library/relational-databases-with-sqlalchemy/double-trouble


#Zoo theme walk through

# Animals
# ID (PK) / Name / Habitat

#s Zookeeper log
# ID (PD)  /Animal ID (FK) / Notes
#  pip freeze > requirements.txt 


from sqlalchemy import ( create_engine, Column, Integer,
                       Engine, String, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine("sqlite:///zoo.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# one class per table

class Animal(Base):
    __tablename__ = 'animals'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    habitat = Column(String)
    logs = relationship("Logbook", back_populates="animals")

    def __repr__(self):
        return f"""
    \nAnimal {self.id}\r 
    Name = {self.name}\r 
    Notes = {self.habitat}
    """

class Logbook(Base):
    __tablename__ = 'logbook:'
    
    id = Column(Integer, primary_key=True)
    animal_id = Column(Integer, ForeignKey("animals.id"))
    notes = Column(String)
    animal = relationship("Animal", back_populates='logs')
    
    def __repr__(self):
        return f"""
    \nLogbook {self.id}\r 
    Animal ID = {self.animal_id}\r 
    Notes = {self.notes}
    """
if __name__ == "__main__":
    Base.metadata.create_all(engine)