<p align="center">
  <img src="https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/HA%20Pics/trash%20recycle.jpg"/>
</p>
<h1 align="center">Trash Recycle Package</h1>
<p align="center">Be sure to :star: my repo!</p>
<hr *** </hr>
<p align="center">This package is designed to remind you to take out the bins but more importantly remind if it is also a recycle bin week as their pickups are normally every other week. This package was originally created by skalavala and has been modified to fit my purpose.</p>
<hr --- </hr> 

<h4 align="left">Package Credits:</h4>
<p align="left">skalavala - https://github.com/skalavala/smarthome</br>
<p align="left">Stanvx - https://github.com/stanvx/Home-Assistant-Configuration</br>

<hr --- </hr>

<h4 align="left">Package Dependencies:</h4>
<p align="left">- MQTT Broker</br>
<p align="left">- Sensors for Time & Date please see my sensor.yaml for details</br>
<p align="left">- Everything else required is already in the package</br>
<h4 align="left">Package Sensors:</h4>
<p align="left">The sensors in this package will determine if it's an even or odd week of the year, and track day of the week to set reminders for trash and recycle days respectively. </br>
<h4 align="left">Package Automations:</h4>
<h4 align="left">Trash Pickup Day Changed</h4>
<p align="left">This automation publishes a MQTT topic when the UI input select for Trash Day has been changed for the above sensors to track</p>
<h4 align="left">Recycle Pickup Day Changed</h4>
<p align="left">This automation publishes a MQTT topic when the UI input select for Recycle Day has been changed for the above sensors to track</p>
<h4 align="left">Recycle Pickup Week Changed</h4>
<p align="left">This automation publishes a MQTT topic when the UI input select for Recycle Week has been changed for the above sensors to track</p>
<h4 align="left">Restore Trash Recycle Settings on Startup</h4>
<p align="left">This automation restores your input select settings on a Home Assistant restart.</p>
<h4 align="left">Trash Pickup Reminder</h4>
<p align="left">This automation reminds me by TTS message "Attention! Tomorrow is the Trash Pickup day. Please don't forget to put the trash bin outside tonight!" at 5pm the night before bin day as I set my trash day from the UI as the day before it is collected.</p>
<h4 align="left">Recycle Pickup Reminder</h4>
<p align="left">This automation reminds me by TTS message "Attention! Tomorrow is the Recycle Pickup day. Please don't forget to put the recycle bin outside tonight!" at 4:59pm the night before bin day as I set my trash day from the UI as the day before it is collected.</p>
<h4 align="left">Bins Taken Out</h4>
<p align="left">This automation lets HA know I have taken out the bins and resets the trash recycle reminders for the next week.</p>
<h4 align="left">Remind Later</h4>
<p align="left">This automation postpones the trash reminder to 9pm to remind me again before I go to bed, it also plays a TTS message "Ok lazy, will remind you again before bed!"</p>
<h4 align="left">Reset Trash Reminders</h4>
<p align="left">This automation resets the trash reminders for the next week.</p>
<hr --- </hr>

| Take me back to the packages thanks!| [Packages](https://github.com/JamesMcCarthy79/Home-Assistant-Config/tree/master/config/packages) | 
| --- | --- |

<hr --- </hr>
