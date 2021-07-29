.. _global-pipeline-libraries:

=======================================
Configure the Global Pipeline Libraries
=======================================

The shared pipeline libraries are configured in the Jenkins general
configuration page. It's pretty self-explanatory when one logs into the page, so
not a lot of details will be provide here. In terms of settings, all of the
pipeline libraries are hosted in git and should default to using the **master**
branch. The other piece of information that is needed is the name and git clone
url of the library which are listed out below. The KPL libraries are publicly
accessible, so there is no need to set a credential.

Essential Libraries
-------------------

Keysight Pipeline Library
    https://bitbucket.it.keysight.com/scm/keysightpl/keysight-pipeline-library.git

    This is a loading library that provides a number of steps which load the
    core library, configuration library and the extension libraries. While it
    may be convienent to use the centrally maintained repo, many teams may find
    it convienent to replace this with their own fork so they can add workflows
    appropriate for their products. It is recommended to always call the library
    the "Keysight Pipeline Library" so jenkinsfiles can be easily moved from
    one jenkins instance to another.

Keysight Pipeline Library Configuration
    The url for the configuation library is provided by the user.

    When using a fork of the Keysight Pipeline Library, it's very convienent to
    setup this library to point to the same url and put both the jenkins instance
    configuration file and the 'keysightPipelineLibraryConfigurationVersion.txt'
    file in that fork.

Kpl Core Library
    https://bitbucket.it.keysight.com/scm/keysightpl/kpl-core.git

    This library contains the base methods used by all of the libraries. For
    example the RunResourceScript step that will copy a python script from the
    library resources folder to the local workspace and execute it.

Extension Libraries
-------------------

Kpl Ansible Extensions
    https://bitbucket.it.keysight.com/scm/keysightpl/kpl-ansible-extensions.git

Kpl Bitbake Extensions
    to be created...

    For embedded linux builds

Kpl C++ Extensions
    to be created...

Kpl Container Extensions
    https://bitbucket.it.keysight.com/scm/keysightpl/kpl-container-extensions.git 

Kpl Counter Extensions
    https://bitbucket.it.keysight.com/scm/keysightpl/kpl-counter-extensions.git

Kpl Npm Extensions
    to be created...

Kpl Os Package Management Extensions
    https://bitbucket.it.keysight.com/scm/keysightpl/kpl-os-packagemanagement-extensions.git

Kpl Python Extensions
    to be created...

Kpl SemVer Extensions
    to be created...

Kpl Tap Extensions
    to be created...

Kpl VisualStudio Extensions
    to be created...
