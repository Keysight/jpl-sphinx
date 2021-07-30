==========================
Send Notification to Slack
==========================

Introduction
=========================
This chapter of the KOSi Pipeline Library guide describes the steps to send
notifications to users.  The two supported communication vehicles are Slack 
and email. Slack is the recommended choice. The notifications are useful for 
alerting users of a build failure.

The paths for Slack and email follow a similar pattern. The two configurables 
of both paths are 

1. The notification destination--.i.e. user(s) to send the message to. If this information is absent, the path silently does nothing.
2. the ‘sendPolicy’, which determines whether to send the message depending on the build status of the commit. 

A Simple Example
=========================
Say, we are developing our pipeline in *my-jenkinsfile.groovy*, which currently does nothing:

.. code-block:: groovy
    :caption: my-jenkinsfile.groovy

    // groovylint-disable BracesForMethod,BracesForTryCatchFinally,BracesForIfElse
    // groovylint-disable MethodName,VariableName,ImplementationAsType
    @Library('Keysight Pipeline Library') _
    LoadRequiredLibrariesForGeneralWorkflows()

    Map config = [:]

    if(!config.agentLabel)
    {
        config.agentLabel = 'windows'
    }

    pipeline
    {
        agent
        {
            label config.agentLabel
        }

        stages
        {
            stage("Do Nothing")
            {
                steps
                {
                    echo "Do Nothing"
                }
            }
        }       

        post
        {
            always 
            {
                FinalizeJobWithoutClean(config)
            }
        }
    }

To add the capability of sending notifications, we first add a key-value pair 
in the *config* map (the key is the communication channel, and the value 
is the receiver and sendPolicy). See :ref:`Configurations` for information
on how to define this pairing. Then we rely on *SendCommitMessageToSlackViaJava* from 
the shared keysight pipeline library to send the message. Here is the new *my-jenkinsfile.groovy* 

.. code-block:: groovy
    :caption: my-jenkinsfile.groovy

    // groovylint-disable BracesForMethod,BracesForTryCatchFinally,BracesForIfElse
    // groovylint-disable MethodName,VariableName,ImplementationAsType
    @Library('Keysight Pipeline Library') _
    LoadRequiredLibrariesForGeneralWorkflows()

    def config = [
    'slack':[
        'channel':'#proj-kosi-pipeline-library-qa-messages',
        'sendPolicy':'onFailOrFirstSuccess'
        ]
    ]
    //for email,  use the commented lines
    //'email':[
    //    'to':['pdl-kosipipeline-admin@keysight.com'],
    //    'sendPolicy':'onFailOrFirstSuccess'
    //]

    if(!config.agentLabel)
    {
        config.agentLabel = 'windows'
    }

    pipeline
    {
        agent
        {
            label config.agentLabel
        }

        stages
        {
            stage("Do Nothing")
            {
                steps
                {
                    echo "Do Nothing"
                }
            }
        }       

        post
        {
            always 
            {
                SendCommitMessageToSlackViaJava(config)
                //SendCommitEmailMessageViaJava(config)
                FinalizeJobWithoutClean(config)
            }
        }
    }
Now, the key-value pair is hard-coded into config.
In order to avoid hard-coding, see :ref:`Using a custom configuration step`.

Using a custom configuration step
=========================

.. warning::
    While most of the code in the jenkinsfiles is showing usage of the KOSi 
    Pipeline Library, the agent labels are specific to the setup of the 
    Jenkins Manager and will likely need to be adjusted. The documentation 
    uses the standard labels **any**, **none**, **windows**, **linux**, and 
    **mac**. For the moab environment one can use **windows**, **rhl-node10** 
    and **mac-node10**.

Alternatively, we can insert the configurations by defining a custom groovy step using 
the *call()* function in a new file. This pattern is common in environments
where the library is owned by a specific team, and allows us to avoid hard-coding 
the configuration into dozens of jenkinsfiles. Here, are two custom steps for Slack and email, 
respectively: 

.. code-block:: groovy
    :caption: InsertTeamSlack.groovy

    def call(Map config = [:])
    {
        def slackChannel = '#proj-trustforge-builds'
        if( !config.slack  )
        {
            config.slack = ['channel':slackChannel]
        }
        else if( !config.slack.channel)
        {
            config.slack.channel = slackChannel
        } 

        return config
    }

.. code-block:: groovy
    :caption: InsertDefaultEmailRecipients.groovy

    def call(Map config=[:])
    {
        def emailToList = ['scott_selberg@keysight.com']
        emailToList.add('chris_grove@keysight.com')
        emailToList.addAll(['chris_hales@keysight.com'])

        if(!config?.email)
        {
            config.email = ['to':emailToList]
        }
        else if(!config?.email?.to)
        {
            config.email.to = emailToList
        }

        return config
    }

Additionally, a separate finalization step is often used to make the pipeline more simple. 
Here is an example of a usable step, located in a separate file:
.. where is this file?

.. code-block:: groovy
    :caption: TeamFinalizeJob.groovy
    def call(Map config=[:])
    {
        SendCommitMessageToSlackViaJava(config)
        SendCommitEmailMessageViaJava(config)
        FinalizeWorkspace(config)
    }

Here is an updated *my-jenkinsfile.groovy* that utilizes these steps:

.. code-block:: groovy
    :caption: my-jenkinsfile.groovy

  // groovylint-disable BracesForMethod,BracesForTryCatchFinally,BracesForIfElse
  // groovylint-disable MethodName,VariableName,ImplementationAsType
  @Library('Keysight Pipeline Library') _
  LoadRequiredLibrariesForGeneralWorkflows()

  config = InsertTeamSlackChannel(config)
  config = InsertDefaultEmailRecipients(config)

  if(!config.agentLabel)
  {
      config.agentLabel = 'windows'
  }

  pipeline
  {
      agent
      {
          label config.agentLabel
      }

      stages
      {
          stage("Do Nothing")
          {
              steps
              {
                  echo "Do Nothing"
              }
          }
      }       

      post
      {
          always 
          {
          TeamFinalizeJob(config)
          }
      }
  }

Configurations
=========================

.. code-block:: groovy
    :caption: Example configuration for Slack

    def config = [
        'slack':[
            'channel':'#proj-kosi-pipeline-library-qa-messages',
            'sendPolicy':'onFailOrFirstSuccess'
        ]
    ]

.. code-block:: groovy
    :caption: Example configuration for email

    def config = [
        'email':[
            'to':['pdl-kosipipeline-admin@keysight.com'],
            'sendPolicy':'onFailOrFirstSuccess'
        ]
    ]

**Message Destination**

In Slack, a message can be sent to a channel or a person. For a channel, 
use the syntax `'channel' : #proj-kosi-pipeline-library-qa-messages'` and for
a user, use their member ID `'channel' : 'U0238VB96L9'`.

In email, us the syntax `'to' : ['pdl-kosipipeline-admin@keysight.com']`, and  
multiple emails can be added to the array.

**Controlling when messages are sent with 'sendPolicy'
**

These are the supported notification policies, i.e. the string values that 
are expected for `config.email.sendPolicy` and `config.slack.sendPolicy`.

`'always'`: Step returns **true**; message always sent

`'never'`: Step returns **false**; message never sent

`'onFail'`: Step returns **true** if the currentBuild.result is **FAILURE** or **UNSTABLE**. These are evaluated by the step JobHasFailed. Sends message on build failure.

`'onFailOrFirstSuccess'`: This is the default policy. Step returns **true** if the job has failed, or if the previous run failed according to JobHasFailed, or if the present job is new.

`'onFailOrStateChange'`: Step returns **true** if the job has failed. Returns **true** if the value in currentBuild.result of the previous run is different from the currentBuild.result of the present run.


