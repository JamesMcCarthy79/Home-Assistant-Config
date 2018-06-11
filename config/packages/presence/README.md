<p align="center">
  <img src="https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/HA%20Pics/Presence.png"/>
</p>
<h1 align="center">Presence Package</h1>
<p align="center">Be sure to :star: my repo!</p>
<hr *** </hr>
<p align="center">This package incorporates the device trackers I use to detect our home or away presence and use these to fire off Automations and TTS messages.</p>
<hr --- </hr> 

<h4 align="left">Package Credits:</h4>
<p align="left">andrewjfreyer - https://github.com/andrewjfreyer/presence</br>
<p align="left">HA Forum - Need to find link</br>
<hr --- </hr>

<h4 align="left">Package Dependencies:</h4>
<p align="left">- MQTT Broker</br>
<h4 align="left">Package Device Trackers:</h4>
<h4 align="left">Ping</h4>
<p align="left">This tracker uses the ping component as a metric for calculating if I have just arrived home or just left home, it isn't good for much then that as our phones go to sleep and turn Wi-Fi off when they do. It works quiet well to establish just got home/just left however.</br>
<h4 align="left">Owntracks</h4>
<p align="left">This tracker uses GPS location from our phones to update HA as to where we are this component works to varing degrees, I have managed to improve this with tasker on my android firing whenever I connect/disconnect from known Wi-FI networks.</br>
<h4 align="left">BLE Detection</h4>
<p align="left">This tracker uses 3 Rasberry Pi Zero's located around the house and calulates occupancy via mean average sensor.</br>
<h4 align="left">Package Inputs:</h4>
<h4 align="left">There are 2 input boolaens which are triggered by the BLE trackers located around the house, these are then used to update home/away status aswell as trigger automations.</h4>
<h4 align="left">Package Sensors:</h4>
<h4 align="left">In this package I use the MQTT json.batt value to provide battery level for our phones, also use json.confidence value to use as part of the mean average sensor. I use a min_max sensor to get the mean average of the 3 Pi Zero's json.confidence value and use that average as the trigger for the input boolean switch status. Lastly there are a couple of Google travel time sensors telling me the time to and from work.</h4>
<h4 align="left">Package Automations:</h4>
<h4 align="left">James Occupancy Home</h4>
<p align="left">This automation uses the mean average of the occupancy sensor of above 10 to turn on the input boolean as the likelyhood of me being home is very high.</p>
<h4 align="left">James Occupancy Away</h4>
<p align="left">This automation uses the mean average of the occupancy sensor of below 10 to turn on the input boolean as the likelyhood of me being away is very high.</p>
<h4 align="left">James Home</h4>
<p align="left">This automation updates the device_tracker.admin_samsung state to home if input boolean is turned on.</p>
<h4 align="left">James Away</h4>
<p align="left">This automation updates the device_tracker.admin_samsung state to away if input boolean is turned off.</p>
<h4 align="left">James/Tina Home Announcement</h4>
<p align="left">This automation plays a specific TTS message notifying everyone that we have arrived, as with any of my TTS stuff it really is to mess with my wife as she hates them.</p>
<h4 align="left">James Work Travel Announcement</h4>
<p align="left">These automations plays specfic TTS announcements to let my family know I have arrived safely at work, I've just left work with est travel time, I'm 25/15/5 mins from home.</p>
<h4 align="left">James at Shops</h4>
<p align="left">This automation plays a TTS message to let my wife know I'm at the shops and to send me a list of anything else we might need. I will be updating this with another project that puts a Pi with camera in the fridge using machinebox to create a shopping list based on the status of the fridge contents.</p>
<hr --- </hr>

| Take me back to the packages thanks!| [Packages](https://github.com/JamesMcCarthy79/Home-Assistant-Config/tree/master/config/packages) | 
| --- | --- |

<hr --- </hr>
