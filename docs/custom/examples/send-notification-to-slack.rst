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
is the receiver and sendPolicy), and then we rely on *SendCommitMessageToSlackViaJava* from 
the shared pipeline. Here is the new *my-jenkinsfile.groovy* 

.. code-block:: groovy

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
Here, the key-value pair is hard-coded into config. See :ref:`Configurations` for information
on how to define this pairing.
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

*InsertTeamSlack.groovy*: 

.. code-block:: groovy

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

*InsertDefaultEmailRecipients.groovy*:

  .. code-block:: groovy

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
Here is an example of a usable *TeamFinalizeJob.groovy*:

.. code-block:: groovy
    def call(Map config=[:])
    {
        SendCommitMessageToSlackViaJava(config)
        SendCommitEmailMessageViaJava(config)
        FinalizeWorkspace(config)
    }

Here is an updated *my-jenkinsfile.groovy* that utilies these steps:

.. code-block:: groovy

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

**Message Destination**

In Slack, a message can be sent to a channel or a person. For a channel, 
use the syntax `'channel':#proj-kosi-pipeline-library-qa-messages'` and for
a user, use their member ID `'channel':'U0238VB96L9'`.

In email, us the syntax `'to':['pdl-kosipipeline-admin@keysight.com']`, and  
multiple emails can be added to the array.

**Controlling when messages are sent with `sendPolicy`**

These are the supported notification policies, i.e. the string values that 
are expected for `config.email.sendPolicy` and `config.slack.sendPolicy`.

**`'always'`**: With this policy, this step will always return **true**.

**`'never'`**: With this policy, this step will always return **false**.

**`'onFail'`**: With this policy, this step will return **true** if the currentBuild.result is **FAILURE** or **UNSTABLE**. These are evaluated by the step JobHasFailed

**`'onFailOrFirstSuccess'`**: This is the default policy. With this policy, this step will return **true** if the job has failed. It will also return true if the previous run failed according to JobHasFailed or does not exist and the present job did not fail.

**`'onFailOrStateChange'`**: With this policy, this step will return **true** if the job has failed. It will also return **true** if the value in currentBuild.result of the previous run is different from the currentBuild.result of the present run.


