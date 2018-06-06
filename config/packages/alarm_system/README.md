<p align="center">
  <img src="https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/HA%20Pics/MQTT%20Alarm%20Panel.png"/>
</p>
<h1 align="center">Alarm System Package</h1>
<p align="center">Be sure to :star: my repo!</p>
<hr *** </hr>
<p align="center">This package utilises the MQTT Control Panel in conjunction with my Xiaomi Gateway and Door, Window & Motion Sensors to act as an Alarm System.</p>
<hr --- </hr> 

<h4 align="left">Package Credits:</h4>
<p align="left">Stanvx - https://github.com/stanvx/Home-Assistant-Configuration</br>

<hr --- </hr>

<h4 align="left">Package Dependencies:</h4>
<p align="left">- MQTT Alarm Panel</br>
<p align="left">- Door/Window/Motion Sensors already added into HA</br>
<p align="left">- TTS capable device (only if you wish to take advantage of spoken notifications)</br>
<p align="left">- Sound file for siren simulation, I used the Xiaomi Gateway to play the siren sounds.</br>
<p align="left">- Notify component setup if you want to receive notifications on your phone.</br>
<p align="left">- Template sensors sensor.door_count & sensor.window_count are required for numeric state conditions in some &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;automations.</br>
<h4 align="left">Package Automations:</h4>
<h4 align="left">Trigger Alarm While Armed Away</h4>
<p align="left">This automation sets the sensors that will be used to triggered the alarm in away mode. In this automation you will need to include what window, door and motion sensors you wish to use to trigger your alarm. Once any of these has been changed to the relevant state it will change the alarm state to "triggered" which will be used in the automations below. It will also play a TTS message telling you that you have 60 seconds to reset the system or the alarm will sound.</p>
<h4 align="left">Trigger Alarm While Armed Home</h4>
<p align="left">This automation sets the sensors that will be used to triggered the alarm in home mode. In this automation you will need to include what window, door and motion sensors you wish to use to trigger your alarm. Once any of these has been changed to the relevant state it will change the alarm state to "triggered" which will be used in the automations below. It will also play a TTS message telling you that you have 60 seconds to reset the system or the alarm will sound.</p>
<h4 align="left">Alarm Pending Cancel</h4>
<p align="left">This automation is really only for annoying my wife as we constantly have to reset the alarm panel when she has to go back inside to get something she forgot. It is triggered only when the alarm panel state goes from "pending" to "disarm" and it plays a message "what did you forget this time".</p>
<h4 align="left">Open Doors Notification on Alarm Set</h4>
<p align="left">This automation uses the sensor.door_count numeric state, if its state is higher than 1 (as my front door is always open when we set the alarm) then trigger a TTS notification to let me know and cancel pending arm. This really ensures we don't set the alarm unless all doors are closed.</p>
<h4 align="left">Open Windows Notification on Alarm Set</h4>
<p align="left">This automation uses the sensor.window_count numeric state, if its state is higher than 0 then trigger a TTS notification to let me know and cancel pending arm. This really ensures we don't set the alarm unless all windows are closed.</p>
<h4 align="left">Start Siren on Alarm Trigger</h4>
<p align="left">This automation uses the to "triggered" alarm state to trigger the Xiaomi Gateway to start playing the siren sound. It also plays a TTS message over the in-house  system to let the intruder know the police have been notified. Lastly it will trigger the command_line switch which uses a python script that notifies my Android phone that Alarm has been triggered.</p>
<h4 align="left">Stop Alarm Siren</h4>
<p align="left">This automation uses the from "triggered" alarm state to trigger the Xiaomi Gateway to stop playing the siren sound. It also plays a TTS message over the in-house system to let us know the alarm has been deactivated. Lastly it will trigger the command_line switch which uses a python script that notifies my Android phone that Alarm has been deactivated.</p>
<hr --- </hr>

| Take me back to the packages thanks!| [Packages](https://github.com/JamesMcCarthy79/Home-Assistant-Config/tree/master/config/packages) | 
| --- | --- |

<hr --- </hr>
