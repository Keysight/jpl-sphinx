===============================
Keysight Pipeline Library Setup
===============================

Setting up the Keysight Pipeline Library for use involves a few steps. First we
need to setup the integration with a HashiCorp Vault instance.  Next we need to
create a configuation file for the jenkins instance. Lastly, we need to declare
the various KPL pipeline libraries as global shared libraries in Jenkins.

.. note::

  If only a few select parts of the library are desired, it's possible to skip
  everything except the setup of the global shared pipeline libraries. (That could
  even be done as a library setup for a folder in Jenkins if the user is willing
  to avoid or allow-list the steps that the Jenkins sandboxing rules will block.)
  However, skipping this work will not allow the user to fully utilize the
  library.

.. toctree::
   :titlesonly:
   :glob:

   *
