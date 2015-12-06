# Catalog application

Application uses endangered animals families catalog to demonstrate CRUD operations on the database (Create, Read, Update, Delete). 

## Main Features

Build with Flask Framework. Incorporates OAuth 2.0 protocol to login through Facebook and Google providers. Implements multiple file upload system. Uses python object-relational mapping (ORM) library SQLAlchemy to create database schema, populate, connect and query relational database. Implements JSON API endpoint on url: /catalog.json. Uses WTForms library for user input validation. Application prevents cross-site request forgery (CSRF) attacks.

 
## Installation:

Use supplied Vagrant file. For Vagrant set up see the following link:  
[Vagrant installation](https://www.udacity.com/wiki/ud197/install-vagrant)
Once Vagrant is installed use vagrant up and vagrant ssh to boot and connect to a virtual machine.  
Navigate to the vagrant directory-- cd /vagrant



## Quick start:

1. Enter your App ID and App Secret obtained from Facebook developer page into fb_client_secrets.json file. Likewise assign your App ID to appID variable in login.html file located inside templates directory. 

2. Enter your client id and client secret obtained from Google developer console into client_secrets.json file. Likewise assign your client id to data-clientid variable in login.html file found in templates directory.

3. Run the following commands in this order:
	* python database_schema.py 
	* python lotsofitems.py 
	* python application.py

4. Launch application locally from command line: 
	* python application.py 
   and visit the page in your favorite browser on http://localhost:8000

## Requirements:

For full requirements list see requirements.txt
