.. _introduction:

Quick Start
===================================================

.. code-block:: shell

    pip install flask-socketio-lit-html

Example: User
===================================================
Basic example is a User component.

How it works
===================================================

The model of the component - the Python class - is used to auto generated all the stuff when register it with :meth:`webcomponent_base.IndexModel.register`.
The next html tags are then available:

- <`componentname`> : The component html tag to use in .html
- <ul-`componentname`> : A dynamic list of all the components
- <form-`componentname`> : A Form to add new component or modify one

Generate a Rest API
----------------------
Register the component blueprint which contains the next JSON endpoints:

- GET  `/componentname` : The component implementation - a static javascript module
- GET  `/componentname/<int:index>` : The component with the primary key `index`
- GET  `/componentname/all` : The list of all components indexes in database
- POST `/componentname` : The JSON new user or the user to modify if `index` key is set

Integrate lit-element in Flask jinja
----------------------
The webcomponent inherit from lit-element, business methods have to be overwritten in the jinja template extending `webcomponent_base.js`. Following blocks are available :

- `render` : the HTML view of the component
- `style` : CSS for the component - Global CSS is ignored with shadow DOM
- `form` : an html form which can be used to create component or modify one

Update html on server side data changes
----------------------
A socketio message is send by the server to the component JS module after a POST request completes. It contains the new or updated index. Its name is
cls+'update' where cls is your python component class. For example it could be `Userupdate`. Then the component updates itself.
