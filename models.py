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
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
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
    logs = relationship("Logbook", back_populates="animal",
                        cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"""
    \n Animal {self.id}\r 
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
    \n Logbook {self.id}\r 
    Animal ID = {self.animal_id}\r 
    Notes = {self.notes}
    """
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    
    # python3 
    # import models
    # >>> lion = models.Animal(name="lion", habitat="savannah")
    # don't need an id since generated, or log since a relationship
    
    # >>> lion.name
    # >>>'lion'
    # >>> lion.id #nothing since we have not put it into the database yet.
    # >>> models.session.add(lion)
    # >>> models.session.commit()
    # >>> lion.id
    # >>> 1
    # >>> lion.habitat
    # 'savannah'
    # >>> lion_log = models.Logbook(animal_id=1, notes="great pouncer")
    # >>> models.session.add(lion_log)
    # >>> models.session.commit()
    # >>> lion_log.id
    # 1
    # Access the relationship like attributes
    #     >>> lion_log.animal
    #  Animal 1
    #     Name = lion
    #     Notes = savannah
    # >>> 
# It goes into the relationship ... finds the animal it relates to
# then it goes to the other table, and pulls the information on that.
# >>> lion_log.animal
#  animal 1
#     Name = lion
#     Notes = savannah
    
# >>> lion.logs
# [
    
#  ogbook 1
#     Animal ID = 1
#     Notes = great pouncer
#     ]
# >>> 
# >>> lion_log2 = models.Logbook(animal_id=1, notes="really likes meat")
# The relationship items print, missing the first letter and even when viewing in the sql viewer I'm not seeing why.abs
# >>> exit()
# (env) (base) curtisoneal@curtiss-mbp sqlalchemy_dbs % sqlite3 zoo.db
# SQLite version 3.33.0 2020-08-14 13:23:32
# Enter ".help" for usage hints.
# sqlite> .tables
# animals   logbook:
# sqlite> select * from animals;
# 1|lion|savannah
# sqlite> 
# sqlite> select * from `logbook:` 
#    ...> ;
# 1|1|great pouncer
# 2|1|really likes meat
# sqlite> 
# -- I had a type in the table definition of logbook with a colon after the name.
# the relationships do not show, since they are not columns
# what happens if I make a log for an animal that does not exist? Let's try it.abs
# sqlite> .exit
# >>> import models
# >>> seal_log = models.Logbook(animal_id=2, notes="likes to wave")
# >>> models.session.add(seal_log)
# >>> models.session.commit()
# >>> seal_log.id
# 3
# >>> seal_log.animal
# >>>      (returns nothing/None)
# >>> print(seal_log.animal)
# None
# >>> 
# so this open relationship to an id that doesn't exist is important since
# it is based on an id, and if we create a second animal that gets that id
# the relationship that we left open will relate to that new animal that is erroneous
# >>> wombat = models.Animal(name="wombat", habitat="forest")
# >>> models.session.add(wombat)
# >>> models.session.commit()
# >>> seal_log.animal

    
#  Animal 2
#     Name = wombat
#     Notes = forest
    
# So you'd be better off desining a flow that either checks that an animal exists first when a user
# would go to create a relationship entry, or force them to create the animal first.abs
# lion = models.session.query(models.Animal).filter(models.Animal.name=="lion").first()
# if you don' tput the .first() You will get back a query object instead of the single class item.abs
# >>> lion = models.session.query(models.Animal).filter(models.Animal.name=="lion").first()
# >>> lion.name
# 'lion'
# >>> wombat = models.session.query(models.Animal).filter(models.Animal.name=="wombat").first()
# >>> wombat.name
# 'wombat'
# >>> lion_log = models.session.query(models.Logbook).filter(models.Logbook.animal_id==1).first()
# >>> lion_log.animal

    
#  Animal 1
#     Name = lion
#     Notes = savannah
    
# >>> seal_log = models.session.query(models.Logbook).filter(models.Logbook.animal_id==2).first()
# >>> seal_log.animal

    
#  Animal 2
#     Name = wombat
#     Notes = forest
# >>> lion_log.notes
# 'great pouncer'
# >>> seal_log.notes
# 'likes to wave'
# >>> lion.habitat= "grasslands"
# >>> lion.habitat
# 'grasslands'
# >>> models.session.dirty
# IdentitySet([
    
#  Animal 1
#     Name = lion
#     Notes = grasslands
#     ])
# >>> models.session.commit()
# >>> lion_log.animal
#  Animal 1
#     Name = lion
#     Notes = grasslands
# >>> seal = wombat
# >>> seal.name
# 'wombat'
# >>> seal.name = "seal"
# >>> seal.habitat = "ocean"
# >>> models.session.dirty
# IdentitySet([
    
#  Animal 2
#     Name = seal
#     Notes = ocean
#     ])
# >>> models.session.commit()
# >>> seal_log.animal_id =1
# >>> seal_log.animal

    
#  Animal 1
#     Name = lion
#     Notes = grasslands
    
# >>> seal_log.animal

    
#  Animal 1
#     Name = lion
#     Notes = grasslands
    
# >>> lion.logs
# [
    
#  Logbook 1
#     Animal ID = 1
#     Notes = great pouncer
#     , 
    
#  Logbook 2
#     Animal ID = 1
#     Notes = really likes meat
#     , 
    
#  Logbook 3
#     Animal ID = 1
#     Notes = likes to wave
# What this shows is that if you alter the foreign key of the relationship it will 
# Assign itself to another entry, and confuse what you were trying to represent
# >>> seal_log.animal_id = 2
# >>> seal.logs
# [
    
#  Logbook 3
#     Animal ID = 2
#     Notes = likes to wave
#     ]
# >>> (Put it back)
# >>> models.session.commit()
# >>> models.session.delete(seal)
# >>> models.session.commit()
# >>> print(seal_log)

    
#  Logbook 3
#     Animal ID = None
#     Notes = likes to wave

# So note that the Animal ID is None if we delete the associated record.
# >>> models.session.delete(lion_log)
# >>> models.session.commit()
# >>> lion.logs
# [
    
#  Logbook 2
#     Animal ID = 1
#     Notes = really likes meat
#     ]
# >>> 
# You can build Cascade into your model that will keep these joined when you delete.
# THis option tells sqlalchemy what to do with the child when the parent is deleted.
# https://teamtreehouse.com/library/relational-databases-with-sqlalchemy/cascade
# default value of the relationships's cascade value is cascade="save-update"
# But you can set it to cascade="all, delete-orphan"
#  "All", synomnym for save update and a few other options we want to keep. #  for an 
# item is updated in a session all its related objects get updated.abs
# delete - means that when we delete a parent object its related child objects will also 
# be marked for deletion

# if we delete lion all related lion logs will be deleted.
# delete orphan - means that if an object is disassociated with any object then it will be 
# marked for deletion 
# if we are looking at a lion's list of logs, and we delete it, it would also be deleted from the 
# logbook table 
# Since we are changing how the DB works we delete the Zoo.db file. To recreate it.
# >>> exit()
#added cascade="all, delete, delete-orphan" to the relationship in the parent
# (env) (base) curtisoneal@curtiss-mbp sqlalchemy_dbs % python3 models.py
# recreated

# >>> bat = models.Animal(name="Bruce", habitat="Gotham")
# >>> cat = modles.Animal(name="Selena", habitat="Diamond Store")
# >>> wombat = models.Animal(name="wombat", habitat="forest")
# >>> models.session.add(bat)
# >>> models.session.add(cat)
# >>> models.session.add(wombat)

# >>> bat_log = models.Logbook(animal_id=1, notes="Punches things")
# >>> cat_log = models.Logbook(animal_id=2, notes="Steals things")
# >>> wombat_log = models.Logbook(animal_id=3, notes="Has cube shaped poop")
# Can't seem to add more than one at a time.
# >>> models.session.add(bat_log)
# >>> models.session.add(cat_log)
# >>> models.session.add(wombat_log)
# models.session.commit()
# #Checked in SQLite browser
# Supposed to add two logs for two animals
# >>> cat_log2=models.Logbook(animal_id=2, notes="Has many cats")
# >>> bat_log2=models.Logbook(animal_id=1, notes="Has many bats")
# >>> wombat_log2=models.Logbook(animal_id=1, notes="Has no Superhero")
# >>> models.session.add(cat_log2)
# >>> models.session.add(bat_log2)
# >>> models.session.add(wombat_log2)
# >>> models.session.commit()
# >>> models.session.commit()
# >>> bat_log2.id
# 5
# >>> cat_log2.id
# 4
# >>> bat_log.id
# 3
# >>> models.session.delete(wombat)
# >>> models.session.commit()
# >>> for logs in models.session.query(models.Logbook):
# ...      print(logs)
# ... 
#  Logbook 1
#     Animal ID = 2
#     Notes = Steals things
    
#  Logbook 3
#     Animal ID = 1
#     Notes = Punches things
    
#  Logbook 4
#     Animal ID = 2
#     Notes = Has many cats
    
#  Logbook 5
#     Animal ID = 1
#     Notes = Has many bats
    
#  Logbook 6
#     Animal ID = 1
#     Notes = Has no Superhero
# Has no superhero was assigned to Bat not wombat
# >>> for animal in models.session.query(models.Animal):
# ...     print(animal)
# ... 

#  Animal 1
#     Name = Bruce
#     Notes = Gotham
    
#  Animal 2
#     Name = Selena
#     Notes = Diamond Store

# How delete orphan if we delete 
# >>> del bat.logs[0]
# >>> del bat.logs[0]
# >>> for logs in models.session.query(models.Logbook):
# ...      print(logs)
# ... 
 
#  Logbook 1
#     Animal ID = 2
#     Notes = Steals things
     
#  Logbook 4
#     Animal ID = 2
#     Notes = Has many cats
    
#  Logbook 5
#     Animal ID = 1
#     Notes = Has many bats
    
#  Logbook 6
#     Animal ID = 1
#     Notes = Has no Superhero
# in my local version del bat.logs[0] did not delete that log.abs