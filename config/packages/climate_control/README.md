<p align="center">
  <img src="https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/HA%20Pics/Climate%20Control.png" width="450"/>
</p>
<h1 align="center">Climate Control Package</h1>
<p align="center">Be sure to :star: my repo!</p>
<hr *** </hr>
<p align="center">This package enables control of my IR Controlled Air Conditioners and 3 Speed Ceiling fans via an Input Select on the UI with TTS whilst still maintaining original 3 speed wall switch functionality for WAF.</p>
<hr --- </hr> 

<h4 align="left">Package Credits:</h4>
<p align="left">Me :bowtie:</br>

<hr --- </hr>

<h4 align="left">Package Dependencies:</h4>
<p align="left">- MQTT Broker</br>
<p align="left">- IR Controlled Air Conditioner</br>
<p align="left">- 3 Speed Fan controlled by either IR or SONOFF will work</br>
<p align="left">- Preconfigured Switches for IR or Sonoff devices</br>
<p align="left">- Optional Temperature/Humidity/Lux Sensors</br>
<p align="left">- Notify Component</br>

<h4 align="left">Package Fans:</h4>
<p align="left">I now use Sonoff iFan02 to smart control my 3 speed ceiling fans, they require the use of the MQTT Fan component. To setup your own you will need to adjust the following variables.

``name:``
``command_topic:``
``speed_command_topic:``
``state_topic:``
``speed_state_topic:``
``state_value_template:``</br>

These worked great but the iFan02 didn't break out enough GPIO to connect to the original 3 speed wall switch to maintain normal operation. My wife was not impressed with having to use her phone or Alexa to turn on the fans anytime she wanted to use them and as we have kids they need to be constantly adjusted and turned off at random times of the day. I was under the pump to come up with a solution, so I thought I could use an ESP32 and detect the position of the 3-speed switch, then relay that via MQTT for the fan to act on that topic. I used a 240v to 5v step down convertor so that I could power the devices from behind the original wall plate. These power a Pycom WiPy but any ESP device would work, the 3 speed wall switch main feed connects to the ESP ground wire and the corresponding speed positions connect to GPIO pins on the ESP. When the wall switch is rotated it connects that GPIO to ground and the code reacts to that sending a unique MQTT topic.

I also have a Xiaomi Mi Smart Pedestal Fan this has been integrated into HA with the help of this [custom component](https://community.home-assistant.io/t/mi-smart-pedestal-fan/49998/52) and whilst basic functions are working not all options for the fan are there, but enough to make it usable within Home Assistant. 

<h4 align="left">Package Automations:</h4>
<h4 align="left">Air Conditioners</h4>
<p align="left">There is an input select for my Air Conditions with options for Off/Cold/Heat each one selects an automation detailed below. The automations for the Air Conditioners are pretty straight forward they just call on the above scenes nothing to complicated here.</br>
<h4 align="left">Fans</h4>
<p align="left">There is an input select for my Fans with options for Off/Low/Medium/High each one selects a MQTT topic of the corresponding fan. I also have the fans on a 2 hour timer so they switch off after we go to sleep or in my wifes case after she has turned them on to be in a room for 10 minutes and then leave them on.</br>
<h4 align="left">Original Wall Switches</h4>
<p align="left">There is a MQTT Topic for each of my wall switch positions this topic changes the Fan input_select metioned above.</br>
<h4 align="left">Xiaomi Smart Buttons</h4>
<p align="left">There is an input select for my Smart Buttons are used for single press and cycle through the Fan input selects for each room that has a fan.</br>
<h4 align="left">Package Scenes:</h4>
<p align="left">The Scenes in this package simple call Air Conditioner IR codes from the Broadlink Switch component they were there from before I changed to an input select and I just decided to keep them you could just as easily use the switch calls here. I was considering creating a custom component for my air conditioner but it is either really hot or cold when we use them so I only use the pre-set settings for cold and hot respectively.</br>

<hr --- </hr>

| Automations! | [Node-RED-Flow](https://github.com/JamesMcCarthy79/Home-Assistant-Config/tree/master/config/packages/climate_control/Node-RED-Flow) | [YAML](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/climate_control/climate_control.yaml) |
| --- | --- | --- |

| Take me back to the packages thanks!| [Packages](https://github.com/JamesMcCarthy79/Home-Assistant-Config/tree/master/config/packages) | 
| --- | --- |

<hr --- </hr>
