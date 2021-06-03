
Link Testing Playground
=======================
.. code-block:: RST

  .. code-block:: RST
  
**Using :ref: keyword in autosectionlabel**

reStructuredText

.. code-block:: 
    :ref:`The Second Section of Getting Started` This link indicates that the autosectionlabel extension in conf.py is working

rendered text
    :ref:`The Second Section of Getting Started` This link indicates that the autosectionlabel extension in conf.py is working    

**Use of targets for implicit hyperlinking**

reStructuredText

.. code-block:: 
    target1_ should link to Second Section of Getting Started using implicit hyperlinking (is feature of restructure text, not sphinx autosectionlabel) if target1 is correctly defined in the second section

rendered text
    target1_ should link to Second Section of Getting Started using implicit hyperlinking (is feature of restructure text, not sphinx autosectionlabel) if target1 is correctly defined in the second section

**Using custom links and autosectionlabel :ref:** 

reStructuredText

.. code-block:: 
    :ref:`Links to 3rd Section of Getting Started<The Third Section of Getting Started>` using custom link and sphinx autosectionlabel

rendered text
    :ref:`Links to 3rd Section of Getting Started<The Third Section of Getting Started>` using custom link and sphinx autosectionlabel

**Using autosectionlabel to link to target in other document**

reStructuredText

.. code-block:: 
    :ref:`header1` intended behavior is linking to header target in show_host_info comments

rendered text
    :ref:`header1` intended behavior is linking to header target in show_host_info comments

**Using autosectionlabel with custom link for function in other document**

reStructuredText

.. code-block:: 

    :ref:`Second header custom2<header2>` intended behavior is linking to header target in show_host_info comments

rendered text
    :ref:`Second header custom2<header2>` intended behavior is linking to header target in show_host_info comments

**Use :py domain to link to argument in python module**

reStructuredText

.. code-block:: 
    :py:meth:`get_argument_parser()<show_host_info.get_argument_parser>`

rendered text
    :py:meth:`get_argument_parser()<show_host_info.get_argument_parser>`

**Use :py domain to python module**

reStructuredText

.. code-block:: 
    See the :py:mod:`show_host_info` script.

rendered text
    See the :py:mod:`show_host_info` script.


.. warning::
     Cannot place `targets <https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#implicit-hyperlink-targets>`_ straight into module; causes error in parsing module.


.. note::

    Link from text to a heading in any other part of the document (or other documents) by using the :ref: command with the heading text as the parameter

    Or can use sphinx `python signatures <https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#python-signatures>`_.

Getting Started
===============
See the :py:mod:`show_host_info` script. (it should link to the module documentation)

See the :py:meth:`get_ip_addresses<show_host_info.get_ip_addresses>` method in the :py:mod:`show_host_info` script.  (should also link)

See the **ShowHostInfo** step (should link)


The Second Section of Getting Started
=====================================
.. _target1:
This section is used to test if links within the same section are working. 

The Third Section of Getting Started
====================================
This section is used to test if links within the same section are working using custom links from above