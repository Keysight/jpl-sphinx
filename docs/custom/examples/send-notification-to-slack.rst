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
2. Whether to send the message depending on the build status of the commit. This is the ‘sendPolicy’



.. warning::
    While most of the code in the jenkinsfiles is showing usage of the KOSi 
    Pipeline Library, the agent labels are specific to the setup of the 
    Jenkins Manager and will likely need to be adjusted. The documentation 
    uses the standard labels **any**, **none**, **windows**, **linux**, and 
    **mac**. For the moab environment one can use **windows**, **rhl-node10** 
    and **mac-node10**.