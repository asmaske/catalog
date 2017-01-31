from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item
import datetime

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# insert category and items for Soccer
var_category = Category(category_name="Soccer")
session.add(var_category)
session.commit()
var_item = Item(item_name="Shin guards",
                description="A shin guard is a piece of equipment worn on the front of a player's shin to protect them from injury.",
                create_ts=datetime.datetime.now(), category=var_category)
session.add(var_item)
session.commit()
var_item = Item(item_name="Jersey",
                description="A loose shirt worn by a member of team as part of a uniform",
                create_ts=datetime.datetime.now(), category=var_category)
session.add(var_item)
session.commit()
var_item = Item(item_name="Soccer cleats",
                description="Shoes that have cleats on them",
                create_ts=datetime.datetime.now(),
                category=var_category)
session.add(var_item)
session.commit()

# insert category and items for Basketball
var_category = Category(category_name="Basketball")
session.add(var_category)
session.commit()

# insert category and items for Baseball
var_category = Category(category_name="Baseball")
session.add(var_category)
session.commit()
var_item = Item(item_name="Bat",
                description="A baseball bat is a smooth wooden or metal club used in the baseball to hit the ball after it is thrown by the pitcher.",
                create_ts=datetime.datetime.now(),
                category=var_category)
session.add(var_item)
session.commit()
var_item = Item(item_name="Ball",
                description="The ball features a rubber or cork center, wrapped in yarn, and covered, "
                            "with two strips of white horsehide or cowhide, tightly stitched together.",
                create_ts=datetime.datetime.now(),
                category=var_category)
session.add(var_item)
session.commit()

# insert category and items for Hockey
var_category = Category(category_name="Ice Hockey")
session.add(var_category)
session.commit()
var_item = Item(item_name="Stick",
                description="An ice hockey stick is a piece of equipment used in ice hockey to shoot, pass, and carry the puck.",
                create_ts=datetime.datetime.now(),
                category=var_category)
session.add(var_item)
session.commit()

# insert category and items for Tennis
var_category = Category(category_name="Tennis")
session.add(var_category)
session.commit()
var_item = Item(item_name="Racket",
                description="The parts of a tennis racket are the head, rim, face, neck, butt/butt cap, handle and strings."
                            " Vibration dampers may be interlaced in the proximal part of the string array for improved feel.",
                create_ts=datetime.datetime.now(),
                category=var_category)
session.add(var_item)
session.commit()
var_item = Item(item_name="Ball",
                description="Tennis balls are fluorescent yellow at major sporting events, but in recreational play can be virtually any color."
                            " Tennis balls are covered in a fibrous felt which modifies their aerodynamic properties,"
                            " and each has a white curvilinear oval covering it",
                create_ts=datetime.datetime.now(),
                category=var_category)
session.add(var_item)
session.commit()


print 'added categories and items'