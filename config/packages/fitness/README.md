<p align="center">
  <img src="https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/HA%20Pics/Fitness.jpg"/>
</p>
<h1 align="center">Fitness Package</h1>
<p align="center">Be sure to :star: my repo!</p>
<hr *** </hr>
<p align="center">This package was utilising a custom google fit component however it has been causing errors due to authentication. In the interim I am using tasker to pull the steps from my phone and post them to a MQTT topic I can read in HA</p>
<hr --- </hr> 

<h4 align="left">Package Credits:</h4>
<p align="left">If you have any ideas for improvement then your name will go here :+1:</br>

<hr --- </hr>

<h4 align="left">Package Dependencies:</h4>

- Android Phone

- Knowledge of Tasker and its Plugins

- [Tasker APP](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm&hl=en_AU)

- [MQTT Publisher Plugin for Tasker](https://play.google.com/store/apps/details?id=net.nosybore.mqttpublishplugin)

<h4 align="left">Package Automations:</h4>
<h4 align="left">Steps with Tasker</h4>

Step 1 - Create Profile on Event Steps Taken (I used 25 steps to be the trigger but you can choose whatever you want)

Tasker Proile                                                                                                 |  Tasker Profile
:------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------:
![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/HA%20Pics/Tasker%20Profile%201.jpg)  |  ![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/HA%20Pics/Tasker%20Profile%202.jpg)

Step 2 - Create Task to publish those to your MQTT Broker and use whatever topic you like this will what is subscribed to in your MQTT sensors from the package.

Tasker Task                                                                                                |  Tasker Task
:---------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------:
![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/HA%20Pics/Tasker%20Task%201.jpg)  |  ![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/HA%20Pics/Tasker%20Task%202.jpg)
<h4 align="left">Things to be added in future</h4>

I have a MiBand 3 which I'm able to get metrics into google fit app via the use of a 3rd party app called [Notify & Fitness](https://play.google.com/store/apps/details?id=com.mc.miband1) From there I was trying to use a custom component for google fit to extract those metrics into Home Assistant. This component is having troubles with authentication and requires some more work. 
What can I do with these once I can get them well for starters I would track my steps and exercise with InfluxBD and Grafana.
I would then use the sleep tracker to notify HA when I'm in a deep sleep and turn off things like ceiling fans etc.

<hr --- </hr>

| Take me back to the packages thanks!| [Packages](https://github.com/JamesMcCarthy79/Home-Assistant-Config/tree/master/config/packages) | 
| --- | --- |

<hr --- </hr>
