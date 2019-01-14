<p align="center">
  <img src="https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/HA%20Pics/Lighting.jpg" width="650"/>
</p>
<h1 align="center">Lighting Package</h1>
<p align="center">Be sure to :star: my repo!</p>
<hr *** </hr>
<p align="center">This package utilises my in wall sonoff switches and selection of smar4t bulbs to automate lighting around my house.</p>
<hr --- </hr> 

<h4 align="left">Package Credits:</h4>
<p align="left">If you have any ideas for improvement then your name will go here :+1:</br>

<hr --- </hr>

<h4 align="left">Package Dependencies:</h4>

- Smart Lighting Switches/Bulbs

- Motion Sensors already added into HA

- Humidity Sensor (Bathroom Automations)

- Noise Sensor (Bathroom Automations)

- Node-RED for Automations

<h4 align="left">Package Automations:</h4>
The lighting automations in my house are triggered by 3 main events either Time, Motion or the Physical Switch being flicked. After sunset must motion automations kick in and will turn a light on if we walk past a motion sensor.
These will then turn off after "No Motion Since" attribute of my motion sensor is at 5 mins, seeing as this works if the wall switch is flicked also.

The only place I have found this to be a problem is the bathroom where the motion isn't triggered when we are in the shower and the light turns off.
To combat this I looked at my available data from the bathroom and wondered how I could stop this and I noticed that the humidity would spike whilst we were in the shower.
I set the condition that humidity must be below a certain threshold in order to complete the lights off command. This has worked without fail whilst someone has been in the shower.

The only other time we have to contend with is when the kids are having a bath, it doesn't raise the humidity in the same way as the shower but when they are in the bath the noise level is huge.
I use a noise level sensor as the condition must be below a certain level to complete the off command. That my friends is how you reach the wife approval factor for bathroom lighting automations.
<hr --- </hr>

| Automations! | [Node-RED-Flow](https://github.com/JamesMcCarthy79/Home-Assistant-Config/tree/master/config/packages/lighting/Node-RED-Flow) | [YAML](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/lighting/lighting.yaml) |
| --- | --- | --- |

| Take me back to the packages thanks!| [Packages](https://github.com/JamesMcCarthy79/Home-Assistant-Config/tree/master/config/packages) | 
| --- | --- |

<hr --- </hr>
