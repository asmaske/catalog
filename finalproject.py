from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash
from flask import session as login_session
from flask import make_response

import json
import random
import string

from modules import jsonmodule
from modules import dbmodule
from modules import authmodule


app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"

"""
    Google Auth Routes section
"""


# Create anti-forgery state token
@app.route('/login')
def show_login():
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in xrange(32))
    app.secret_key = state

    # login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # if request.args.get('state') != login_session['state']:
    # Validate state token
    if request.args.get('state') != app.secret_key:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    return authmodule.gconnect_method(code, CLIENT_ID)


@app.route('/logoff')
def gdisconnect():
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token

    authmodule.gdisconnect_method(access_token)
    msg_status = 'logoff'
    return render_template('message.html',
                           msg_status=msg_status,
                           message='Successfully logged off')

"""
    JSON Routes section
"""


# JSON data for catalog
@app.route('/catalog/json')
def get_catalog_json():
    """
        route to get all catalog data in JSON format
    """
    return jsonmodule.catalog_json()


# JSON data for categories
@app.route('/catalog/categories/json')
def get_category_json():
    """
        route to get all category data in JSON format
    """
    return jsonmodule.category_json()


# JSON data for items
@app.route('/catalog/items/json')
def get_item_json():
    """
        route to get all items data in JSON format
    """
    return jsonmodule.items_json()


# JSON data for all items of a category
@app.route('/catalog/<string:category_name>/items/json')
def get_category_items_json(category_name):
    """
        route to get all items data for a category in JSON format
    """
    return jsonmodule.category_items_json(category_name)


# JSON data for a specific item
@app.route('/catalog/<string:category_name>/<string:item_name>/json')
def get_category_items_item_json(category_name,
                                 item_name):
    """
        route to get item details for an item in JSON format
    """
    return jsonmodule.category_items_item_json(category_name,
                                               item_name)


# JSON data for latest items
@app.route('/catalog/latestitems/json')
def get_latest_items_json():
    """
        route to get latest items list in JSON format
    """
    return jsonmodule.items_latest_json()


"""
    Templates route section
"""


# display page for catalog
@app.route('/', methods=['GET', 'POST'])
@app.route('/catalog/', methods=['GET', 'POST'])
def show_catalog():
    """
        route to display catalog data and most recent items
        on web page
        link to add a new item
    """
    if request.method == 'POST':
        operation = ''
        if request.form['addcat-additem']:
            operation = request.form['addcat-additem']
        if operation == 'Add Category':
            return redirect(url_for('add_category'))
        elif operation == 'Add Item':
            return redirect(url_for('add_item'))
    else:
        # get category count and item count
        cat_count = dbmodule.get_category_count()
        item_count = dbmodule.get_item_count()

        # get category and it's item count
        categories_and_item_count =\
            dbmodule.get_categories_and_item_count_data()
        items_latest = dbmodule.get_items_latest_data()
        if 'username' not in login_session:
            login_status = 'FALSE'
        else:
            login_status = 'TRUE'
        return render_template(
            'category.html',
            category_count=cat_count,
            item_count=item_count,
            categories_and_item_count=categories_and_item_count,
            items_latest=items_latest,
            login_status=login_status)


# display page for items of a category
@app.route('/catalog/<string:category_name>/items',
           methods=['GET', 'POST'])
def show_category_items(category_name):
    """
        route to display all items for a category on web page
    """
    if request.method == 'POST':
        if request.form['addcat-additem']:
            operation = request.form['addcat-additem']
            # display 'add_item' page when user clicks 'Add'
            if operation == 'Add Category':
                return redirect(url_for('add_category'))
            elif operation == 'Add Item':
                return redirect(url_for('add_item'))
    else:
        # get category and it's item count
        categories_and_item_count =\
            dbmodule.get_categories_and_item_count_data()
        category_items, items_count = \
            dbmodule.get_items_and_count_data(category_name)
        if 'username' not in login_session:
            login_status = 'FALSE'
        else:
            login_status = 'TRUE'
        return render_template(
            'category_items.html',
            login_status=login_status,
            categories_and_item_count=categories_and_item_count,
            category_items=category_items,
            category_name=category_name,
            count=items_count)


# display page for description of an item
@app.route('/catalog/<string:category_name>/<string:item_name>',
           methods=['GET', 'POST'])
def show_category_items_item(category_name, item_name):
    """
        route to display item description for an item on web page
    """
    if request.method == 'POST':
        operation = ''
        if request.form['edit-delete']:
            operation = request.form['edit-delete']
        if operation == 'Edit':
            return redirect(url_for('edit_item',
                                    category_name=category_name,
                                    item_name=item_name))
        if operation == 'Delete':
            return redirect(url_for('delete_item',
                                    category_name=category_name,
                                    item_name=item_name))
    else:
        category_items_item =\
            dbmodule.get_category_items_item_data(category_name, item_name)
        if 'username' not in login_session:
            login_status = 'FALSE'
        else:
            login_status = 'TRUE'
        if category_items_item is not None:
            itm_desc = category_items_item.description
            return render_template('category_items_item.html',
                                   login_status=login_status,
                                   category_name=category_name,
                                   item_name=item_name,
                                   description=itm_desc)
        else:
            message = category_name + ' and ' + item_name +\
                      ' combination does not exist'
            login_status = login_status
            msg_status = 'failed'
            return render_message_page(login_status, msg_status, message)


# display page for adding a new category
@app.route('/catalog/category/add',
           methods=['GET', 'POST'])
def add_category():
    """
        route to add a category
    """
    # check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    else:
        login_status = 'TRUE'

    if request.method == 'POST':
        operation = ''
        if request.form['add-cancel']:
            operation = request.form['add-cancel']
        if operation == 'Cancel':
            # if cancelled return to home page
            return redirect(url_for('show_catalog'))
        if operation == 'Add':
            new_cat_name = request.form['new-category']
            msg_status = dbmodule.add_category(new_cat_name)
            if 'username' not in login_session:
                login_status = 'FALSE'
            else:
                login_status = 'TRUE'
            if msg_status == 'success':
                login_status = login_status
                msg_status = msg_status
                message = 'Successfully added ' + new_cat_name
                return render_message_page(login_status, msg_status, message)
            else:
                login_status = login_status
                msg_status = msg_status
                message = 'Duplicate Category ' + new_cat_name
                return render_message_page(login_status, msg_status, message)
    else:
        return render_template('add_category.html', login_status=login_status)


# display page for adding a new item
@app.route('/catalog/item/add',
           methods=['GET', 'POST'])
def add_item():
    """
        route to add an item
    """
#    check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    else:
        login_status = 'TRUE'

    if request.method == 'POST':
        operation = ''
        if request.form['add-cancel']:
            operation = request.form['add-cancel']
        if operation == 'Cancel':
            # if cancelled return to home page
            return redirect(url_for('show_catalog'))
        if operation == 'Add':
            new_item_cat_name = request.form['new-item-category']
            new_item = request.form['new-item']
            new_item_desc = request.form['new-item-description']
            msg_status = dbmodule.add_item(new_item_cat_name,
                                           new_item,
                                           new_item_desc)
            if msg_status == 'success':
                login_status = login_status
                msg_status = msg_status
                message = 'Successfully added ' + new_item\
                          + ' for Category ' + new_item_cat_name
                return render_message_page(login_status, msg_status, message)
            else:
                login_status = login_status
                msg_status = msg_status
                message = 'Duplicate Item ' + new_item\
                          + ' for Category ' + new_item_cat_name
                return render_message_page(login_status, msg_status, message)
    else:
        # get all category data for drop down
        categories = dbmodule.get_category_data()
        # get first category
        first_category = dbmodule.get_category_first_data()
        return render_template('add_item.html',
                               login_status=login_status,
                               categories=categories,
                               first_category=first_category)


# display page to edit an item
@app.route('/catalog/<string:category_name>/<string:item_name>/edit/',
           methods=['GET', 'POST'])
def edit_item(category_name, item_name):
    """
        route to edit an item
        user can only edit description
    """
    # check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    else:
        login_status = 'TRUE'

    if request.method == 'POST':
        operation = ''
        if request.form['save-cancel']:
            operation = request.form['save-cancel']

        if operation == 'Cancel':
            # if cancelled return to home page
            return redirect(url_for('show_catalog'))

        # get form data
        desc = request.form['edit-desc']

        # update if user clicks Edit button
        if operation == 'Save':
            msg_status = dbmodule.update_item_description(item_name,
                                                          category_name,
                                                          desc)
            if msg_status == 'success':
                login_status = login_status
                msg_status = msg_status
                message = 'Successfully deleted ' + item_name\
                          + ' for Category ' + category_name
                return render_message_page(login_status, msg_status, message)
            else:
                login_status = login_status
                msg_status = msg_status
                message = 'Duplicate Item ' + item_name\
                          + ' for Category ' + category_name
                return render_message_page(login_status, msg_status, message)
    else:
        # get description for item
        description = dbmodule.get_item_description_data(category_name,
                                                         item_name)
        return render_template('edit_item.html',
                               login_status=login_status,
                               item_name=item_name,
                               category_name=category_name,
                               description=description)


# display page to delete an item
@app.route('/catalog/<string:category_name>/<string:item_name>/delete/',
           methods=['GET', 'POST'])
def delete_item(category_name, item_name):
    """
        route to delete an item
    """
    # check if user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    else:
        login_status = 'TRUE'

    if request.method == 'POST':
        operation = ''
        if request.form['delete-cancel']:
            operation = request.form['delete-cancel']

        if operation == 'Cancel':
            # if cancelled return to home page
            return redirect(url_for('show_catalog'))

        # delete item if user clicks Delete button
        if operation == 'Delete':
            msg_status = dbmodule.delete_item_data(category_name,
                                                   item_name)
            if msg_status == 'success':
                login_status = login_status
                msg_status = msg_status
                message = 'Successfully deleted ' + item_name\
                          + ' for Category ' + category_name
                return render_message_page(login_status, msg_status, message)
            else:
                login_status = login_status
                msg_status = msg_status
                message = 'Problem deleting '\
                          + item_name + ' for Category ' + category_name
                return render_message_page(login_status, msg_status, message)
    else:
        return render_template('delete_item.html',
                               login_status=login_status,
                               item_name=item_name,
                               category_name=category_name)


def render_message_page(login_status, msg_status, message):
    return render_template('message.html',
                           login_status=login_status,
                           msg_status=msg_status,
                           message=message)


# display page to add a image
# commented: need to understand how to convert filestorage to blob
# @app.route('/catalog/<string:category_name>/<string:item_name>/addimage/',
#            methods=['GET', 'POST'])
# def add_item_image(category_name, item_name):
#     """
#         route to add an iimage
#     """
#     # check if user is logged in
#     # if 'username' not in login_session:
#     #     return redirect('/login')
#
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             print 'no files'
#         files = request.files['file']
#         msg_status = dbmodule.update_item_image(item_name,
#                                                 category_name,
#                                                 files)
#         if msg_status == 'success':
#             return render_template('message.html',
#                                    msg_status=msg_status,
#                                    message='Successfully saved image '
#                                            + item_name
#                                            + ' for Category '
#                                            + category_name)
#         else:
#             return render_template('message.html',
#                                    msg_status=msg_status,
#                                    message='Error in saving image '
#                                            + item_name
#                                            + ' for Category '
#                                            + category_name)
#     else:
#         return render_template('add_item_image.html',
#                                item_name=item_name,
#                                category_name=category_name)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
