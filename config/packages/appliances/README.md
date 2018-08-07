<p align="center">
  <img src="https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/HA%20Pics/Appliances_2.jpg" width="450"/>
</p>
<h1 align="center">Appliance Control Package</h1>
<p align="center">Be sure to :star: my repo!</p>
<hr *** </hr>
<p align="center">This package enables control and notifications of my smart and not so smart appliances. I get notifications when my washer or dryer have finished thiers cycles over TTS. This also allows me to automate my Xiaomi Robovac. You can use the automations within the yaml file or use the Node-RED Flow in the link below.</p>
<hr --- </hr> 

<h4 align="left">Package Credits:</h4>
<p align="left">Stanvx - https://github.com/stanvx/Home-Assistant-Configuration</br>
<p align="left">Me :bowtie:

<hr --- </hr>

<h4 align="left">Package Dependencies:</h4>
<p align="left">- Smart Power Consumption Plugs - I used Xiaomi Zigbee Smart PLugs</br>
<p align="left">- Door Sensors - I used Xiaomi Door Sensors</br>
<p align="left">- Xiaomi Robovac - Optional</br>
<p align="left">- Notify Component</br>
<h4 align="left">Package User Inputs:</h4>
<h4 align="left">Disable Washer/Dyrer Notifications</h4>
<p align="left">These are input_booleans that are triggered via automation to turn off the TTS notifications.</br>
<h4 align="left">Washer/Dyrer Status</h4>
<p align="left">These are input_selects that are triggered via automation to monitor the state of the appliances.</br>
<h4 align="left">Package Sensors:</h4>
<p align="left">These sensors provide the states for appliance status aswell as load power for both dryer & washer.</br>
<h4 align="left">Package Automations:</h4>
<h4 align="left">Washer/Dryer State</h4>
<p align="left">These automations set the state of the Washer/Dryer according to the state of the load power of the smart plug they are connected to. If above 10 set to running, if below 6 set to finishing, if on finishing wait one minute and then set to clean. Once clean we get a TTS notification to tell us that it has finished.</br>
<h4 align="left">Charge Appliances Overnight</h4>
<p align="left">I have a bunch of appliances plugged into a smart power strip and I just simply allow it to turn on at 1am and off again at 4am which is enough time to charge them back to full for the next days opperation.</br>
<h4 align="left">Robovac Error Notification</h4>
<p align="left">Anyone with a Xiaomi product knows that all notifications happen in Chinese these announcements can mean its finished, stuck, needs a filter change, charging etc, so in case of my Robovac encoutering an error I monitor that state and send a pushbullet notification to tell me there is an issu with the Robovac.</p>
<hr --- </hr>

| Automations! | [Node-RED-Flow](https://github.com/JamesMcCarthy79/Home-Assistant-Config/tree/master/config/packages/appliances/Node-RED-Flow) | [YAML](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/appliances/appliances.yaml) |
| --- | --- | --- |

| Take me back to the packages thanks!| [Packages](https://github.com/JamesMcCarthy79/Home-Assistant-Config/tree/master/config/packages) | 
| --- | --- |

<hr --- </hr>
