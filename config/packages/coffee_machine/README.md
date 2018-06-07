<p align="center">
  <img src="https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/HA%20Pics/Coffee%20Machine.jpeg"/>
</p>
<h1 align="center">Coffee Machine Package</h1>
<p align="center">Be sure to :star: my repo!</p>
<hr *** </hr>
<p align="center">This package incorporates the water level sensor I installed into my Aldi coffee machine to let me know if the water reservoir is low and to fill it up before I start making a coffee. I used an esp32 with HC-SR04 ultrasonic sensor installed into the lid of the water tank, and it measures the level of the water and publishes it via MQTT.</p>
<hr --- </hr> 

<h4 align="left">Package Credits:</h4>
<p align="left">me :bowtie: - will create a seperate repo with code used</br>

<hr --- </hr>

<h4 align="left">Package Dependencies:</h4>
<p align="left">- MQTT Broker</br>
<p align="left">- Everything else required is already in the package</br>
<h4 align="left">Package Sensors:</h4>
<p align="left">The MQTT sensor simply subscribes to the topic posted by my esp32 water level sensor.</br>
<h4 align="left">Package Automations:</h4>
<h4 align="left">Coffee Machine Water Refill</h4>
<p align="left">This automation is triggered by the Good Morning input_boolean state going to "off" and if the water level state of the coffee machine is "empty" it will notify me by TTS so that I don’t get half way through making my morning coffee only to run out of water.</p>
<hr --- </hr>

| Take me back to the packages thanks!| [Packages](https://github.com/JamesMcCarthy79/Home-Assistant-Config/tree/master/config/packages) | 
| --- | --- |

<hr --- </hr>
