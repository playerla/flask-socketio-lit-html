.. _web_component_base_js:

Webcomponent\_base JS module
============================

This module requires the SocketIO library to be loaded
:code:`<script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js"></script>`

.. class:: Item

    .. method:: Item.newItem(properties)
        :async:

        Create the new item on the backend. Use POST endpoint.
        (Extends constructor method which doesn't support parameters, use it directly after document.createElement call)

        :param string properties: The properties dict to create the new item.
        :return: The webcomponent item with its database index set.

    .. method:: Item.set()

        Update this item on the backend. Use POST endpoint to send the instance properties values.

    .. method:: Item.delete_()

        Delete this item on the backend and frontend. Use DELETE on 'endpoint/<index>' resource.

.. raw:: html

    <hr width=50 size=10>

Example usage:

`example-item` is your component name. "Custom element names require a dash to be used in them; they can't be single words." (mozilla.org)

.. code-block:: html
   :linenos:

   <example-item index=2></example-item>




.. class:: ItemForm

    .. method:: ItemForm.change_event()

        Call it after form validation to update the element.
        It set properties from input field with the corresponding id. For example an input with id 'email' will set the email property.

    .. method:: ItemForm.add_event()

        Call it after form validation to create a new orphan :class:`Item`. 
        Construct and post the element to the Backend with :meth:`Item.newItem()`.
        Fire an item-created event with the newly created item: `document.getElementById('item-form').addEventListener('item-created', (e) => e.detail);`

.. raw:: html

    <hr width=50 size=10>

Example usage:

.. code-block:: html
   :linenos:

   <form-example-item></form-example-item>




.. class:: ItemList

   .. attribute:: items[]

        A dynamic list of your component

.. raw:: html

    <hr width=50 size=10>

Example usage:

.. code-block:: html
   :linenos:

   <ul-example-item></ul-example-item>