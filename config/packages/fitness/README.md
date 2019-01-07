<p align="center">
  <img src="https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/HA%20Pics/Fitness.jpg"/>
</p>
<h1 align="center">Fitness Package</h1>
<p align="center">Be sure to :star: my repo!</p>
<hr *** </hr>
<p align="center">This package integrates my Mi Band 3 into HA by utilising a 3rd party App called Notify & Fitness which allows me to sync the band with Google Fit and receive intents with tasker. Please be aware that this package only works with Android phones if you own an IOS device you should through it in the bin and buy an Android :wink:</p>
<hr --- </hr> 

<h4 align="left">Package Credits:</h4>

hemantkamalakar - [Google Fit Custom Component](https://github.com/hemantkamalakar/haconfigs/blob/master/custom_components/sensor/google_fit.py)

Joakim Sørensen - [Inspiration gained from this Fitbit Card](https://sharethelove.io/picture-elements-cards/fitbit-card)

<hr --- </hr>

<p align="center">
  <img src="https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/HA%20Pics/Google_Fit.png"/>
</p>

<h4 align="left">Package Dependencies:</h4>

- [Mi Band 3](https://www.banggood.com/Original-Xiaomi-miband-3-Heart-Rate-Monitor-Bluetooth-Smart-Wristband-Bracelet-p-1145408.html?ID=224&cur_warehouse=HK)

- [Android Phone](https://www.reddit.com/r/Android/comments/ad8uul/apple_treats_you_like_a_user_android_treats_you/)

- [Google Fit App](https://play.google.com/store/apps/details?id=com.google.android.apps.fitness)

- [Notify & Fitness App](https://play.google.com/store/apps/details?id=com.mc.miband1&hl=en_AU)


- [Tasker APP](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm&hl=en_AU)

- [MQTT Publisher Plugin for Tasker](https://play.google.com/store/apps/details?id=net.nosybore.mqttpublishplugin)

<h4 align="left">Package:</h4>
<h4 align="left">Notify & Fitness</h4>

Once you have your band setup with the Mi Fit App you can download the Notify & Fitness for Mi Band you will need the pro or paid version in order to sync with Google Fit and use Tasker Integration. As just mentioned, this app allows you to sync your Mi Band with Google Fit and receive/send intents from Tasker and a whole lot more but for the purposes of this package I will run you through what I did to get the required metrics out of the Mi Band and display them in the Lovelace Card above.

Once you are synced with your Mi Band in the Notify App click on the icon with 3 lines next to the home icon and then scroll down to the bottom of the screen and click on More Options.

<p align="center">
  <img src="https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/fitness/Fitness%20Pics/NaF-001.jpg" width="450"/>
</p>

Next scroll to the bottom and select "Auto sync to Google Fit"

<p align="center">
  <img src="https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/fitness/Fitness%20Pics/NaF-002.jpg" width="450"/>
</p>

That’s it from the Notify & Fitness App side, you should however have a look through all of the available options as there are some cool ones for custom notification and using the button from the band to perform actions on your phone like pause music etc.

<h4 align="left">Google Fit</h4>

Once you sync everything up you should now be seeing your steps with in the Google Fit App, the app itself will calculate distance, time and calories based on your steps. If you want more accuracy you can measure your step length and enter it in the Notify & Fitness app directly above where you enabled step sync in the previous step. You will need to enter your weight & height directly into the Google Fit App in order to access these from the custom component below.

<p align="center">
  <img src="https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/fitness/Fitness%20Pics/NaF-003.jpg" width="450"/>
</p>

<h4 align="left">Google Fit Custom Component</h4>

The Google Fit Custom Component will pull the following metrics from your google fit account:
    - steps
    - distance
    - time
    - calories
    - weight
    - height

Please download the [Google Fit Custom Component](https://github.com/hemantkamalakar/haconfigs/blob/master/custom_components/sensor/google_fit.py) and place it here /config/custom_components/sensor/google_fit.py.

Next you will need to adjust the following from my package with your own details, you can enter your credentials directly here or use the secrets file as I have done.

```
####################################################
#                                                  #
#               Sensors - Google Fit               #
#                                                  #
####################################################

  - platform: google_fit
    client_id: !secret google_fit_client_id
    client_secret: !secret google_fit_client_secret
    scan_interval: 30
```
In order to generate your client_id and client_secret, see the prerequisites for
[Google Calender component](https://www.home-assistant.io/components/calendar.google/#prerequisites)

You will need to restart HA, upon restart you will be prompted to authorize your device (your HA instance) in your Google Project you created in the earlier steps.

Google Fit Setup                                                                                                                           |  Google Project Auth
:-----------------------------------------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/fitness/Fitness%20Pics/Google%20Fit%20Setup.png)  |  ![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/fitness/Fitness%20Pics/Auth%20Access.png)|

<h4 align="left">It can take up to 6 hours for your first sensors to appear with data so be patient!</h4>

<h4 align="left">Tasker</h4>

The Google Fit sync did not provide all the metrics I wanted to get from the band but having a look through the available intents provided by the Notify & Fitness App I was able to extract the following information.

    - steps
    - heart rate
    - battery state
    - mi band connection status
    - when I fall asleep
    - when I wake
    - when I don’t have the band on my wrist
    
I have found that the sync time (6 Hours) wasn't good enough to keep constant track of my steps throughout the day, so I pull this metric out with tasker. All the above sensors are trigger events for Tasker to act on, so whenever my fitness band has a heartrate reading Tasker is set to listen to this event and act on it. In this cause the action is to send the heartrate payload to my MQTT Broker and I can then create an MQTT sensor in HA happy days. In order to publish to MQTT you will need the MQTT Publisher plugin for Tasker.

<h4 align="left">Steps</h4>

Create Profile on Event Intent Received and then create an associated task Action Plugin MQTT Publisher, under configuration enter in your 

- broker address - your MQTT Broker address preferable one with external access
- port           - your MQTT Broker Port
- username       - your MQTT user
- password       - your MQTT password
- topic          - the topic your sensor will listen to
- payload        - this will be the value from the intent we have just setup "%value" should go here

Tasker Steps Event                                                                                                            |  Tasker Steps Action
:----------------------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/fitness/Fitness%20Pics/Steps%201.jpg)|  ![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/fitness/Fitness%20Pics/Steps%202.jpg)|

<h4 align="left">Heart Rate</h4>

Create Profile on Event Intent Received and then create an associated task Action Plugin MQTT Publisher, under configuration enter in your 

- broker address - your MQTT Broker address preferable one with external access
- port           - your MQTT Broker Port
- username       - your MQTT user
- password       - your MQTT password
- topic          - the topic your sensor will listen to
- payload        - this will be the value from the intent we have just setup "%value" should go here

Tasker Heart Rate Event                                                                                                    |  Tasker Heart Rate Action
:-------------------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/fitness/Fitness%20Pics/HR%201.jpg)|  ![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/fitness/Fitness%20Pics/HR%202.jpg)|

<h4 align="left">Battery State</h4>

Create Profile on Event Intent Received and then create an associated task Action Plugin MQTT Publisher, under configuration enter in your 

- broker address - your MQTT Broker address preferable one with external access
- port           - your MQTT Broker Port
- username       - your MQTT user
- password       - your MQTT password
- topic          - the topic your sensor will listen to
- payload        - this will be the value from the intent we have just setup "%value" should go here

Tasker Battery Event                                                                                                         |  Tasker Battery Action
:---------------------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/fitness/Fitness%20Pics/Batt%201.jpg)|  ![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/fitness/Fitness%20Pics/Batt%202.jpg)|

<h4 align="left">Connection Status</h4>

Create Profile on Event Intent Received and then create an associated task Action Plugin MQTT Publisher, under configuration enter in your 

- broker address - your MQTT Broker address preferable one with external access
- port           - your MQTT Broker Port
- username       - your MQTT user
- password       - your MQTT password
- topic          - the topic your sensor will listen to
- payload        - this will be the value from the intent we have just setup "%value" should go here

Tasker Connection Event                                                                                                         |  Tasker Connection Action
:------------------------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/fitness/Fitness%20Pics/Connect%201.jpg)|  ![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/fitness/Fitness%20Pics/Connect%202.jpg)|

Tasker Disconnection Event                                                                                                         |  Tasker Disconnection Action
:---------------------------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/fitness/Fitness%20Pics/Disconnect%201.jpg)|  ![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/fitness/Fitness%20Pics/Disconnect%202.jpg)|

<h4 align="left">Sleep State</h4>

Create Profile on Event Intent Received and then create an associated task Action Plugin MQTT Publisher, under configuration enter in your 

- broker address - your MQTT Broker address preferable one with external access
- port           - your MQTT Broker Port
- username       - your MQTT user
- password       - your MQTT password
- topic          - the topic your sensor will listen to
- payload        - this will be the value from the intent we have just setup "%value" should go here

Tasker Asleep Event                                                                                                            |  Tasker Asleep Action
:-----------------------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/fitness/Fitness%20Pics/Asleep%201.jpg)|  ![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/fitness/Fitness%20Pics/Asleep%202.jpg)|

Tasker Awake Event                                                                                                            |  Tasker Awake Action
:----------------------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/fitness/Fitness%20Pics/Awake%201.jpg)|  ![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/fitness/Fitness%20Pics/Awake%202.jpg)|

<hr --- </hr>

<h4 align="left">Band Off Wrist</h4>

Create Profile on Event Intent Received and then create an associated task Action Plugin MQTT Publisher, under configuration enter in your 

- broker address - your MQTT Broker address preferable one with external access
- port           - your MQTT Broker Port
- username       - your MQTT user
- password       - your MQTT password
- topic          - the topic your sensor will listen to
- payload        - this will be the value from the intent we have just setup "%value" should go here

Tasker Off Wrist Event                                                                                                              |  Tasker Off Wrist Action
:----------------------------------------------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/fitness/Fitness%20Pics/Off%20Wrist%201.jpg)|  ![](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/fitness/Fitness%20Pics/Off%20Wrist%202.jpg)|

<h4 align="left">Package Sensors</h4>

All of the Tasker actions we just created will now be waiting for you on your Broker so we need to setup the MQTT Sensors to get them into HA. You will need to adjust the MQTT Sensors from my package to reflect your topics and sensors names accordingly.

```
####################################################
#                                                  #
#                  Sensors - MQTT                  #
#                                                  #
####################################################

  - platform: mqtt
    name: "James Steps"
    state_topic: "steps/james/huawei"
    
  - platform: mqtt
    name: "James BMI"
    state_topic: "bmi/james/huawei"
    unit_of_measurement: "BMI"
    
  - platform: mqtt
    name: "James Heart Rate"
    state_topic: "hr/james/huawei"
    unit_of_measurement: "bpm"
    
  - platform: mqtt
    name: "James MiBand Battery"
    device_class: battery
    state_topic: "mibatt/james/huawei"
    unit_of_measurement: "%"
    
  - platform: mqtt
    name: "James MiBand Status"
    state_topic: "mistatus/james/huawei"
    
  - platform: mqtt
    name: "Tina Steps"
    state_topic: "steps/tina/samsung"
    unit_of_measurement: "steps"
```

I have set up a target weight sensor also you will need to adjust according to your own target weight.

<h4 align="left">Gain Weight</h4>

```
####################################################
#                                                  #
#                Sensors - Template                #
#                                                  #
####################################################

  - platform: template
    sensors:
      target_weight:
        friendly_name: Target Weight
        entity_id: sensor.weight
        value_template: "{{ 85 - states.sensor.weight.state|int }}"
```

<h4 align="left">Loss Weight</h4>

```
####################################################
#                                                  #
#                Sensors - Template                #
#                                                  #
####################################################

  - platform: template
    sensors:
      target_weight:
        friendly_name: Target Weight
        entity_id: sensor.weight
        value_template: "{{ states.sensor.weight.state|int - 15 }}"
```

Lastly I was not able to get BMI directly from any source, as this figure doesn't fluctuate to greatly I have decided to put it in manually so I can calculate my body fat %. Once you have got you BMI you can use it to calculate your body fat % with the below sensor.

```
####################################################
#                                                  #
#                Sensors - Template                #
#                                                  #
####################################################

  - platform: template
    sensors:
      body_fat:
        friendly_name: Body Fat
        entity_id: sensor.weight
        value_template: "{{ ((1.20 * states.sensor.james_bmi.state|int) + (0.23 * 39) - 16.2)|round }}"
        unit_of_measurement: '%'
```

<h4 align="left">Future Plans</h4>

I wan't to be able to pull in my sleep statistics also which will require some adjustsments to the custom component but there is an api for it in the google api docs so it can be done. I also want to add my automations around this data straight off the bat I can think of using the sleep trigger to turn off ceiling fans and engage some kind of night mode for lighting perhaps. Happy to hear what you guys are automating with these data inputs.

| Take me back to the packages thanks!| [Packages](https://github.com/JamesMcCarthy79/Home-Assistant-Config/tree/master/config/packages) | 
| --- | --- |

<hr --- </hr>
