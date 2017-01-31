from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
import json
import dbmodule

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def catalog_json():
    """
        Returns JSON object for all records in the catalog
    Args:
    """
    json_string = dbmodule.get_catalog_data()
    return jsonify(json.loads(json_string))


def category_json():
    """
        Returns JSON object for all records in the Category table
    Args:
    """
    categories = dbmodule.get_category_data()
    return jsonify(Categories=[c.serialize for c in categories])


def items_json():
    """
        Returns JSON object for all records in the Items table
    Args:
    """
    items = dbmodule.get_item_data()
    return jsonify(Items=[i.serialize for i in items])


def category_items_json(category_name):
    """
        Returns JSON object for all items in the Items table
        for a category
    Args:
        category_name: category name for which items are to be selected
    """
    check_category_exists = dbmodule.check_if_category_exists(category_name)
    if not check_category_exists:
        message = 'Category: ' + category_name + ' does not exists...NOTE: search is case sensitive'
        msg = {"message": message}
        json_string = json.dumps(msg)
        return jsonify(json.loads(json_string))

    json_string = dbmodule.get_category_items_data(category_name)
    return jsonify(json.loads(json_string))


def items_latest_json():
    """
        Returns JSON object for all records in the Items table
        order by time descending
    Args:
    """
    items_latest = dbmodule.get_items_latest_data()

    dictionary_list = []
    latest_item_list = []
    d_row = {}
    for key, value in items_latest.items():
        latest_item_list.append({'item': key,
                                 'category': value})
    d_row['RecentItems'] = latest_item_list
    dictionary_list.append(json.dumps(d_row))
    json_str = ''
    for counter, l in enumerate(dictionary_list):
        if counter < len(dictionary_list) - 1:
            json_str += l + ','
        else:
            json_str += l
    return jsonify(json.loads(json_str))


def category_items_item_json(category_name, item_name):
    """
        Returns JSON object for an item in the Items table
        for a category
    Args:
        category_name: category name for which items are to be selected
        item_name: item name for which item details to be selected
    """
    check_category_exists = dbmodule.check_if_category_exists(category_name)
    if not check_category_exists:
        message = 'Category: ' + category_name + ' does not exists...NOTE: search is case sensitive'
        msg = {"message": message}
        json_string = json.dumps(msg)
        return jsonify(json.loads(json_string))

    json_string = dbmodule.get_category_items_item_data_for_json(category_name, item_name)
    return jsonify(json.loads(json_string))
