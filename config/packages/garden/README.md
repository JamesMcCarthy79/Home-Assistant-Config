<p align="center">
  <img src="https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/HA%20Pics/Smart%20Garden.jpg" width="450"/>
</p>
<h1 align="center">Garden Package</h1>
<p align="center">Be sure to :star: my repo!</p>
<hr *** </hr>
<p align="center">This package utilises the Mi Flora Plant Sensors to monitor my garden beds and potted plants to automate when my irrigation system turns to water them.</p>
<hr --- </hr> 

<h4 align="left">Package Credits:</h4>
<p align="left">Me :bowtie:</br>

<hr --- </hr>

<h4 align="left">Package Dependencies:</h4>
<p align="left">- Bluetooth Addon</br>
<p align="left">- Xiaomi Component configured in HA</br>
<p align="left">- Irrigation Parts - 12v Solenoid & Sonoff POW</br>
<h4 align="left">Package Sensors:</h4>
<h4 align="left">Mi Flora Plant Sensors</h4>
<p align="left">Due to the location of my HASSIO Server I could not get a bluetooth connection out to my garden beds. I flashed a Raspberry Pi Zero with HASSIO and installed it out in my Patio area where it can connect to all of my plant sensors. I then use the HASSIO API to get sensor states into my main HA Server.</br>
<p align="left">Each Mi Flora Sensor has the following monitored conditions :-</br>
Temperature
- Humidity
- Moisture
- Conductivity
- Lux
<h4 align="left">Irrigation</h4>
<p align="left">To control the Solenoid I use the Sonoff POW Dual, I could have easily achieved my desired outcome of Opening/Closing the Solenoid with a Sonoff Basic.</br> 
The reason I chose the POW Dual was one you can monitor Power Consumption but also I used the second switch to montior the power consuption of my Patio Entertaining areas festoon lighting and also media equipment.</br>
<h4 align="left">Package Automations:</h4>
<h4 align="left">Turn On Irrigation System</h4>
<p align="left">This automation sets the Irrigation system a simple 12V Solenoid connected to my tap fitting controlled by a Sonoff POW.</br>
It uses time of the day to trigger the automation so the watering occurs at the best time of tha day to not burn or freeze the plants.</br>
This Automation will only fire if the following conditions are met, if season is Summer run twice daily or winter run every third day.</br>
It also needs to met conditions around the Plant Sensor moisture levels if they are higher then 12% then the automation won't fire also will check the weather forecast for afternoon/evening showers and won't fire if there is a greater then 60% chance of rain. Where I live if rain is predicted it will normally be a heavy shower so there is not point watering the plants.</p>
<hr --- </hr>

| Take me back to the packages thanks!| [Packages](https://github.com/JamesMcCarthy79/Home-Assistant-Config/tree/master/config/packages) | 
| --- | --- |

<hr --- </hr>
