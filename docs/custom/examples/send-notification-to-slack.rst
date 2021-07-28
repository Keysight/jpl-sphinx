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
              FinalizeJobWithoutClean(config)
          }
      }
  }
Here, the key-value pair is hard-coded into config. In order to avoid hard-coding, see below.

Using a custom configuration step
=========================
Alternatively, we can insert the configurations by defining a custom groovy step using 
the *call()* function in a new file. This pattern is common in environments
where the library is owned by a specific team, and allows us to avoid hard-coding 
the configuration into dozens of jenkinsfiles. Here, the custom step is defined in *InsertTeamSlack.groovy*:

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

Additionally, a separate finalization step is often used to make the pipeline more simple. 
Here is an example of a usable *TeamFinalizeJob.groovy*:\

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
              FinalizeJobWithoutClean(config)
          }
      }
  }

Configurations
=========================

.. warning::
    While most of the code in the jenkinsfiles is showing usage of the KOSi 
    Pipeline Library, the agent labels are specific to the setup of the 
    Jenkins Manager and will likely need to be adjusted. The documentation 
    uses the standard labels **any**, **none**, **windows**, **linux**, and 
    **mac**. For the moab environment one can use **windows**, **rhl-node10** 
    and **mac-node10**.