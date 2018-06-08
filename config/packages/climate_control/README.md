<p align="center">
  <img src="https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/HA%20Pics/Climate%20Control.jpg" width="250"/>
</p>
<h1 align="center">Climate Control Package</h1>
<p align="center">Be sure to :star: my repo!</p>
<hr *** </hr>
<p align="center">This package enables control of my IR Controlled Air Conditioners and 3 Speed Ceiling fans via an Input Select on the UI with TTS.</p>
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
<h4 align="left">Package User Inputs:</h4>
<p align="left">******************************</br>
<h4 align="left">Package Scenes:</h4>
<p align="left">******************************</br>
<h4 align="left">Package Automations:</h4>
<h4 align="left">Air Conditioners</h4>
<p align="left">There is an input select for my Air Conditions with options for Off/Cold/Heat each one selects an automation detailed below.</br>
<h4 align="left">Fans</h4>
<p align="left">There is an input select for my Fans with options for Off/Low/Medium/High each one selects an automation detailed below.</br>
<h4 align="left">Xiaomi Smart Buttons</h4>
<p align="left">There is an input select for my Smart Buttons are used for single press and cycle through the Fan input selects for each room that has a fan.</br>
<h4 align="left">Package Scenes:</h4>
<p align="left">The Scenes in this package simple call Air Conditioner IR codes from the Broadlink Switch component they were there from before I changed to an input select and I just decided to keep them you could just as easily use the switch calls here. I was considering creating a custom component for my air conditioner but it is either really hot or cold when we use them so I only use the pre-set settings for cold and hot respectively.</br>
<h4 align="left">Package Automations:</h4>
<h4 align="left">Air COnditioners</h4>
<p align="left">The automations for the Air Conditioners are pretty straight forward they just call on the above scenes nothing to complicated here.</p>
<h4 align="left">Fans</h4>
<p align="left">The automations for the fans are a little more complicated as I used a 4ch sonoff and used seperate channels to control each speed of the fan. What I wanted to avoid when switching between fan speed selections was to have more than one of the fan speed switches on at the same time. When each fan speed is selected from the input select these automations make sure all other switches on the sonoff are off then turns on the speed selected.</p>
<hr --- </hr>

| Take me back to the packages thanks!| [Packages](https://github.com/JamesMcCarthy79/Home-Assistant-Config/tree/master/config/packages) | 
| --- | --- |

<hr --- </hr>
