webcomponent\_base JS module
=========================

.. method:: Item.newItem(arg)
   :async:

    Create the new item on the backend. Use POST endpoint.
    (Constructor method, use it directly after createElement call)

   :param string properties: The properties dict to create the new item.
   :return: The webcomponent item with its database index set.

.. raw:: html

    <hr width=50 size=10>

Example usage:

.. code-block:: html
   :linenos:

   <item index=2></item>