import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
import datetime
import json

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def get_catalog_data():
    """
        Returns JSON string for all records in the catalog
        Fetches all rows in Category table
         and corresponding child records from Item table
    Args:
    """
    # create a list for dictionary objects
    dictionary_list = []
    categories = session.query(Category).\
        order_by(Category.category_name.asc()).all()
    for category in categories:
        # dictionary for Category
        d_row = {'category_id': category.category_id,
                 'category_name': category.category_name}
        items = session.query(Item).filter_by(
            category_id=category.category_id).all()
        cat_item_list = []
        for counter, item in enumerate(items):
            # dictionary for Category and Item
            cat_item_list.append({'item_id': item.item_id,
                                  'category_id': item.category_id,
                                  'item_name': item.item_name,
                                  'description': item.description})
        d_row['Item'] = cat_item_list
        dictionary_list.append(json.dumps(d_row))

    # create string of JSON data from the dictionary list
    json_str = ''
    for counter, l in enumerate(dictionary_list):
        if counter < len(dictionary_list) - 1:
            json_str += l + ','
        else:
            json_str += l
    return '{"Category":['+json_str+']}'


def get_category_data():
    """
        Returns query result set for records in Category table
    Args:
    """
    categories = session.query(Category).\
        order_by(Category.category_name.asc()).all()
    return categories


def get_category_first_data():
    """
        Returns first record in Category table ordered by category_name
    Args:
    """
    categories = session.query(Category).\
        order_by(Category.category_name.asc()).all()
    for category in categories:
        return category.category_name


def get_category_count():
    """
        Returns count of categories
    Args:
    """
    return session.query(Category).count()


def get_item_count():
    """
        Returns count of items
    Args:
    """
    return session.query(Item).count()


def check_if_category_exists(category_name):
    """
        Returns TRUE is category exists
    Args:
        category_name: name of category
    """
    try:
        session.query(Category). \
            filter_by(category_name=category_name).one()
        return True
    except sqlalchemy.orm.exc.NoResultFound:
        return False


def get_category_items_data(category_name):
    """
        Returns category and all items
    Args:
        category_name: name of category
    """
    # get category id from category table
    dictionary_list = []
    category = session.query(Category). \
        filter_by(category_name=category_name).one()

    d_row = {'category_id': category.category_id,
             'category_name': category.category_name}
    cat_id = category.category_id
    # get items for this category
    category_items = session.query(Item).filter_by(
        category_id=cat_id).all()

    cat_item_list = []
    for counter, item in enumerate(category_items):
        # dictionary for Category and Item
        cat_item_list.append({'item_id': item.item_id,
                              'category_id': item.category_id,
                              'item_name': item.item_name,
                              'description': item.description})
    d_row['Item'] = cat_item_list
    dictionary_list.append(json.dumps(d_row))

    # create string of JSON data from the dictionary list
    json_str = ''
    for counter, l in enumerate(dictionary_list):
        if counter < len(dictionary_list) - 1:
            json_str += l + ','
        else:
            json_str += l
    return '{"Category":['+json_str+']}'


def get_category_items_item_data(category_name, item_name):
    """
        Returns item details for an item in the Items table
        for a category
    Args:
        category_name: category name for which items are to be selected
        item_name: item name for which item details to be selected
    """
    category = session.query(Category).\
        filter_by(category_name=category_name).one()

    cat_id = category.category_id

    # get item details for this item
    category_items_item = session.query(Item).filter_by(
        category_id=cat_id, item_name=item_name).one()

    return category_items_item


def get_category_items_item_data_for_json(category_name, item_name):
    """
        Returns item details for an item in the Items table
        for a category
    Args:
        category_name: category name for which items are to be selected
        item_name: item name for which item details to be selected
    """
    dictionary_list = []
    category = session.query(Category). \
        filter_by(category_name=category_name).one()

    d_row = {'category_id': category.category_id,
             'category_name': category.category_name}
    cat_id = category.category_id

    # get item details for this item
    cat_item_list = []
    category_items_item = session.query(Item).filter_by(
        category_id=cat_id, item_name=item_name).one()
    cat_item_list.append({'item_id': category_items_item.item_id,
                          'category_id': category_items_item.category_id,
                          'item_name': category_items_item.item_name,
                          'description': category_items_item.description})
    d_row['Item'] = cat_item_list
    dictionary_list.append(json.dumps(d_row))

    # create string of JSON data from the dictionary list
    json_str = ''
    for counter, l in enumerate(dictionary_list):
        if counter < len(dictionary_list) - 1:
            json_str += l + ','
        else:
            json_str += l
    return '{"Category":['+json_str+']}'


def get_categories_and_item_count_data():
    """
        Returns all categories and the item count
            for each category
    Args:
    """
    # get category id from category table
    category_row = {}
    categories = session.query(Category). \
        order_by(Category.category_name.asc()).all()
    for category in categories:
        cat_id = category.category_id
        # get item count for this category
        category_items_count = session.query(Item).filter_by(
            category_id=cat_id).count()
        category_row[category.category_name] = category_items_count
    return sorted(category_row.items())


def get_item_data():
    """
        Returns query result set for records in Items table
    Args:
    """
    items = session.query(Item).all()
    return items


def get_items_latest_data():
    """
        Returns key-value pair for records in Items and Category table
            ORDER BY create_ts DESC
    Args:
    """
    # get all records from items order by timestamp desc
    count = 0
    outer_list = []
    items = session.query(Item).order_by(Item.create_ts.desc()).all()
    for item in items:
        if count >= 10:
            break
        count += 1
        inner_list = [item.item_name]
        item_cat_id = item.category_id
        # get the category name for the item
        category = session.query(Category). \
            filter_by(category_id=item_cat_id).one()
        inner_list.append(category.category_name)
        outer_list.append(inner_list)
    return outer_list


def get_items_and_count_data(category_name):
    """
        Returns all items and their count in the Items table
        for a category
    Args:
        category_name: id for which items are to be selected
    """
    # get category id from category table
    category = session.query(Category).\
        filter_by(category_name=category_name).all()
    cat_id = 0
    for cat in category:
        cat_id = cat.category_id
    # get items for this category
    category_items = session.query(Item).filter_by(
        category_id=cat_id).all()
    category_items_count = session.query(Item).filter_by(
        category_id=cat_id).count()
    return category_items, category_items_count


def get_item_description_data(cat_name, item_name):
    """
        Returns description for an item of a given category
    Args:
        cat_name: category name
        item_name: item name
    """
    # get category id for category name
    category = session.query(Category). \
        filter_by(category_name=cat_name).one()
    cat_id = category.category_id

    # get item details for this item
    item = session.query(Item).filter_by(
        item_name=item_name, category_id=cat_id).one()
    return item.description


def update_item_description(item_name, cat_name, description):
    """
        update Item table using data from edit web page
    Args:
        item_name: item name
        cat_name: category_name
        description: description of item
    Return:
        return 'success' if updated
        return 'failed' if update fails
    """
    # get category_id for category_name
    category = session.query(Category). \
        filter_by(category_name=cat_name).one()

    # get item details for this item
    # get item details for this item and category
    cat_id = category.category_id
    item = session.query(Item).filter_by(
        category_id=cat_id, item_name=item_name).one()

    # set column to new value
    item.description = description

    try:
        session.add(item)
        session.commit()
        return 'success'
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        return 'failed'


# def update_item_image(item_name, cat_name, image):
#     """
#         update Item table using data from edit web page
#     Args:
#         item_name: item name
#         cat_name: category_name
#         image: image of item
#     Return:
#         return 'success' if updated
#         return 'failed' if update fails
#     """
#     # get category_id for category_name
#     category = session.query(Category). \
#         filter_by(category_name=cat_name).one()
#
#     # get item details for this item
#     # get item details for this item and category
#     cat_id = category.category_id
#     item = session.query(Item).filter_by(
#         category_id=cat_id, item_name=item_name).one()
#
#     # set column to new value
#     # f = open(image, "rb")
#     # f_data = f.read()
#     # f.close()
#     # item.image = f_data
#
#     try:
#         session.add(item)
#         session.commit()
#         return 'success'
#     except sqlalchemy.exc.IntegrityError:
#         session.rollback()
#         return 'failed'


def delete_item_data(category_name, item_name):
    """
        delete item in Item table
    Args:
        category_name: name of category
        item_name: item name
    Return:
        return 'success' if inserted
        return 'failed' if delete fails
    """
    # get category_id for category_name
    category = session.query(Category). \
        filter_by(category_name=category_name).one()

    # get item details for this item and category
    cat_id = category.category_id
    item = session.query(Item).filter_by(
        category_id=cat_id, item_name=item_name).one()
    try:
        session.delete(item)
        session.commit()
        return 'success'
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        return 'failed'


def add_item(new_item_cat_name, new_item,
             new_item_desc):
    """
        add item in Item table
    Args:
        new_item_cat_name: new item's category
        new_item: new item's name
        new_item_desc: new item's description
    Return:
        return 'success' if inserted
        return 'failed' if item+category_id composite exists
    """
    # get category id for category name
    category = session.query(Category).\
        filter_by(category_name=new_item_cat_name).one()
    new_item = Item(item_name=new_item,
                    description=new_item_desc,
                    create_ts=datetime.datetime.now(),
                    category=category)
    try:
        session.add(new_item)
        session.commit()
        return 'success'
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        return 'failed'


def add_category(new_cat_name):
    """
        add new category in Category table
    Args:
        new_cat_name: new category's name
    Return:
        return 'success' if inserted
        return 'failed' if category name exists
    """
    new_category = Category(category_name=new_cat_name)
    try:
        session.add(new_category)
        session.commit()
        return 'success'
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        return 'failed'
