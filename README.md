# Catalog project

Catalog project is a Python based web project.


### Tech

The project uses the following software:

* [Python](https://www.python.org/) - Programming Language
* [Vagrant](https://www.vagrantup.com/) - Virtual Machine
* [Bootstrap](http://www.getbootstrap.com/) - Front end framework

## Project Details

### Setup

#### 1. Vagrant environment and project files
+ Setup Vagrant environment by cloning the fullstack-nanodegree-vm repo
+ Copy/Clone the project source '<Vagrant location>\fullstack-nanodegree-vm-master\vagrant\catalog'

### Running the application
+ Navigate to the full-stack-nanodegree-vm\vagrant directory in command terminal
+ Execute command vagrant up to start the virtual machine
+ Execute command vagrant ssh to start the shell
+ cd to /vagrant/catalog directory
+ run command python database_setup.py to setup database and schema
+ run command python lotofitems.py to insert initial data into tables
+ run command python final_project.py to start application
+ Launch browser and enter **http://localhost:8000/**
+ NOTE: Authorized users can login using their Google account credentials
+ Home page displays current categories and list of most recently added items
+ User can navigate to view items under a category by clicking a category name
+ On items page, user can click an item name to view the item details
+ Home button will navigate back to home page
+ Login button allows authorized user to login
+ Authorized users can add a new category, add/edit/delete an item

#### JSON routes
+ Following routes are implemented to view data in JSON format
    + /catalog/json route to get all catalog data
    + /catalog/categories/json route to get all categories data
    + /catalog/item/json route to get all items data
    + /catalog/category_name/items/json route to get all items data for a category
    + /catalog/category_name/item_name/json route to get item details for an item of a category
    + /catalog/latestitems/json route to get latest items
    
#### Directory Structure
* catalog
    + README.md
    + client_secrets.json (security file)
    + database_setup.py (creates database schema)
    + finalproject.py (main)
    + lotsofitems.py (seeds tables with initial data)
    + modules
        + authmodule.py
        + dbmodule.py
        + jsonmodule.py
    + static
        + css
            + bootstrap-theme.min.css
            + bootstrap-theme.min.css.map
            + bootstrap.min.css
            + bootstrap.min.css.map
            + glyphicons-halflings-regular.eot
            + glyphicons-halflings-regular.svg
            + glyphicons-halflings-regular.ttf
            + glyphicons-halflings-regular.woff
            + glyphicons-halflings-regular.woff2
            + styles.css
        + js
            + bootstrap.min.js
            + jquery-3.1.1.min.js
            + npm.js
    + templates
        + add_category.html
        + add_item.html
        + base.html
        + category.html
        + category_items.html
        + category_items_item.html
        + delete_item.html
        + edit_item.html
        + login.html
        + message.html
