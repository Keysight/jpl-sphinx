===================================
Jenkins Instance Configuration File
===================================

The Keysight Pipeline Library needs to have a git repository that contains
a configuration file for the library. This is typically created and owned
by the administrator of the Jenkins instance. The bare minimum setup for
the repo is shown below; however, is it not uncommon to fork the **Keysight
Pipeline Library** which is a small loading library and allows the team
to create steps that load the libraries required for their specific workflows.

.. code-block:: none

  my-configuration-library.git
  ├─ resources
  │   ├─ ${jenkins-instance-name}.libconfig.yml
  │   └─ keysightPipelineLibraryConfigurationVersion.txt
  └─ readme.md

.. note::

  Normally, a KPL Sibling library would have a **docs** folder.  This may be
  helpful, but often *loading* and *configuration* libraries are so simple that
  the readme.md file is sufficent.

The text ${jenkins-instance-name} should be replace the hostname part of the
Jenkins URL in the general configuration.  For example, if the Jenkins instance
is configured to be https://jenkins.keysight.com, then we want to create a
text file called "jenkins.libconfig.yml.

Below is a sample jenkins instance configuration file; however, it should not be
considered an authoratative reference for what the configuation file should look
like. In the configuation map initialization process, the contents are
initalized by the imported libraries, values are inserted or overridden by the
jenkins instance configuration and finally values are merged in from the
jenkinsfile.

.. code-block:: yaml

   artifactory:
       repo: generic-local-team-keysight
       vaultPathForCredentials: moab/shared-secrets/accounts/keysight:password

   vault:
       agentLabelForNodeToAuthenticateWithVault: vault-authenticator
       roleIdJenkinsCredential: vault-jenkins-approle-role-id
       secretIdJenkinsCredential: vault-jenkins-approle-secret-id
