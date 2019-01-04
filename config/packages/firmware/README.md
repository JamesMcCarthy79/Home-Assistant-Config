<p align="center">
  <img src="https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/HA%20Pics/Firmware_2.png"/>
</p>
<h1 align="center">Firmware Package</h1>
<p align="center">Be sure to :star: my repo!</p>
<hr *** </hr>
<p align="center">This package keeps track of my current firmware installed on my various devices and alerts me when an update is available.</p>
<hr --- </hr> 

<h4 align="left">Package Credits:</h4>

Me :bowtie:

Sonoff Firmware Sensor - [DavidFW1960](https://github.com/DavidFW1960/home-assistant)

Mikrotik RouterOS Sensor - [dmxsir](https://community.home-assistant.io/t/mikrotik-latest-routeros-sensor/60349)

<hr --- </hr>

<h4 align="left">Firmwares Monitored:</h4>
<p align="left">- Home Assistant</br>
<p align="left">- HA Podcast</br>
<p align="left">- Sonoff Tasmota</br>
<p align="left">- Mikrotik RouterOS</br>
<h4 align="left">To be Added when time allows:</h4>
<p align="left">- Ubiquiti</br>
<p align="left">- Xiaomi (As I don't use the App)</br>
<h4 align="left">Package Automations:</h4>
<p align="left">All sensors are monitored for state change, when a new update is available Node-RED generates a Persistent Notification and then checks to see if I am home then it will play an announcement over TTS with the update type and the version of update available. If I'm not home, then it will notify me via pushbullet with the same information. I am just installing my Yeelights this week so I will add flashing the lights a certain colour when updates are available.</p>
<hr --- </hr>

| Automations! | [Node-RED-Flow](https://github.com/JamesMcCarthy79/Home-Assistant-Config/tree/master/config/packages/firmware/Node-RED-Flow) | [YAML](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/firmware/firmware.yaml) |
| --- | --- | --- |

| Take me back to the packages thanks!| [Packages](https://github.com/JamesMcCarthy79/Home-Assistant-Config/tree/master/config/packages) | 
| --- | --- |

<hr --- </hr>
