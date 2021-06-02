
Link Testing Playground
=======================

:ref:`The Second Section of Getting Started` This link indicates that the autosectionlabel extension in conf.py is working

target1_ should link to Second Section of Getting Started using implicit hyperlinks (not sphinx autosectionlabel)

:ref:`Links to 3rd Section of Getting Started<The Third Section of Getting Started>` using custom link and sphinx autosectionlabel

:ref:`header1` intended behavior is linking to header target in show_host_info comments

:ref:`Second header custom2<header2>` intended behavior is linking to header target in show_host_info comments

.. warning::
     Cannot place `targets<https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#implicit-hyperlink-targets>`_ straight into module; causes error in parsing module.

See the :py:mod:`show_host_info` script. (it should link to the module documentation)

:py:meth:`get_argument_parser()<show_host_info.get_argument_parser>`

.. note::

    Link from text to a heading in any other part of the document (or other documents) by using the :ref: command with the heading text as the parameter

    Or can use sphinx `python signatures <https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#python-signatures>`_.

Getting Started
===============

See the :py:meth:`get_ip_addresses<show_host_info.get_ip_addresses>` method in the **show_host_info** script.  (should also link)






See the **ShowHostInfo** step (should link)

.. _target1:
The Second Section of Getting Started
=====================================
This section is used to test if links within the same section are working. 

The Third Section of Getting Started
====================================
This section is used to test if links within the same section are working using custom links from above