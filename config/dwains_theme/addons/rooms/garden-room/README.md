<p align="center">
  <img src="https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/HA%20Pics/Addon%20Screens/Garden%20Room.png" width="800"/>
  <img src="https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/HA%20Pics/Addon%20Screens/dwains%20-%20plant%20addon.png" width="800"/>
</p>
<h1 align="center">Dwains Theme - Addon Mi Flora</h1>
<p align="center">Be sure to :star: my repo!</br>
<hr --- </hr>

These addons are designed to work with this wonderful Lovelace Theme - [DWAINS THEME](https://github.com/dwainscheeren/lovelace-dwains-theme) You will first need to follow his instructions to install this theme for the below addons to work as pictured.

Each **Room** and **Addon** is explained below in how to implement it and what dependencies it has. All of my addons are made using my own sensors alot of which are not created from standard HA supported features. Some features of these addons my not show for your own setup without advanced configuration.
<hr --- </hr> 

<h4 align="left">Addon Credits:</h4>

[Dwains Theme](https://github.com/dwainscheeren/lovelace-dwains-theme)

<hr --- </hr> 

<h4 align="left">Prerequisites:</h4>

[Mi Flora Plant Sensor](https://gadget-freakz.com/product/xiaomi-mi-flora-plant-sensor/) - Buy some of these guys<br>
[Mi Flora Integration](https://www.home-assistant.io/integrations/miflora/) - This will get you the main sensors<br>
[Plant Sensor](https://www.home-assistant.io/integrations/plant/) - This will montior the plants preferred envirnmental conditions<br>
[Mi Flora Python Script](https://github.com/ThomDietrich/miflora-mqtt-daemon) - An alternative way to retrieve Mi Flora Sensor information<br>

<hr --- </hr> 

<h4 align="left">Mi Flora Sensors:</h4>

I prefer to use the Mi Flora Python Script mentioned above to retrieve the sensor data as opposed to the bult in integration as I can poll the sensors at intervals I like and also at specific times like after I do an irrigation or fertiliser run. 
With this script I am also able to extract the Sensors Firmware Version.<br> 

All of these sensors are feed into your HA via your preferred MQTT Broker. 
I run them through Node-Red first so I can extract the sensor data I want and forward that to HA rather then let HA do all the hardwork of extracting which sensors to read.<br>

You can view my [Node-RED flow & HA Config Here](https://github.com/JamesMcCarthy79/Home-Assistant-Config/tree/master/config/packages/garden)

<hr --- </hr> 

<h4 align="left">Dwains Theme - Room Config:</h4>

_This section assumes you have already installed Dwains Theme_<br>

Once you have setup the sensors you can you will need to add the following code to your rooms.yaml located at ```\config\dwains-theme\configs\rooms.yaml```<br>
```
  - name: Garden
    icon: mdi:sprout
    page_entities:
      columns: 1 #optional
      entities:
    addons:
      - name: Dracaena
        icon: mdi:sprout
        path: 'dwains-theme/addons/rooms/garden-room/dracaena.yaml'
        button_path: 'dwains-theme/addons/rooms/garden-room/button.yaml'
        data:
          firmware: 'Firmware: {{states.sensor.dracaena_firmware.state}}'
          last_update: 'Last Update: {{relative_time(states.sensor.dracaena_last_report.last_updated)}}'
          entity: plant.lounge_plant
````

Config | Description |
| :--- | :--- |
path | This will the location of your addon file |
button_path | This will be the location of the button config file |
firmware | If you used the python script this will be the HA sensor state for you plants firmware |
last_update | this is also something you can extract from any of the sensors for the plant I use one I created with Node-RED but you can replace this with the moisture sensor for example |

Next we need to create a folder called garden-room here ```\config\dwains-theme\addons\rooms``` and inside this folder copy the button.yaml from ```\config\dwains-theme\addons\rooms\hello-room.```<br>
I changed the button.yaml to this
```
# dwains_theme
# Custom button for room addon: garden room

type: custom:button-card
entity: {{ (data | fromjson)['entity'] }}
template: room_more_entity
name: {{ name }}
icon: {{ icon|default('fas:puzzle-piece') }}
tap_action: 
  action: navigate
  navigation_path: {{ navigation_path }}   
label: >
  [[[ 
    if(entity){
      return entity.state;
    } else {
      return 'Entity error!';
    }
  ]]]
  ```
  Next you will need to create the room addon file called ```my_plant_name.yaml``` this will match the one you used in the path location above in the ```rooms.yaml```.<br>
  Inside this file place the following code
  ```
# dwains_theme

#################################################################
#                                                               #
#                      Addons/Garden/Plants                     #
#                                                               #
#################################################################

#################################################################
#                                                               #
#                          Plant Row 1                          #
#                                                               #
#################################################################

- type: horizontal-stack
  cards:

#################################################################
#                                                               #
#                    Plant Lounge Golden Cane                   #
#                                                               #
#################################################################

    - type: custom:stack-in-card
      cards: 

#################################################################
#                                                               #
#                   Golden Cane Image Banner                    #
#                                                               #
#################################################################


        - type: picture
          image: "https://treeloppingpros.com.au/wp-content/uploads/2018/07/golden-cane-palm-tree-brisbane-southside.jpg"
          style: |
            ha-card {
              height: 85px;
            }

#################################################################
#                                                               #
#                    Mi Flora Sensor Details                    #
#                                                               #
#################################################################

        - type: vertical-stack
          cards:
            - type: markdown
              content: >
                <center>
                <h3>
                Mi Flora - Lounge Golden Cane
                </h3>
                </center>
              style: |
                ha-card {
                color: teal;
                margin-top: -20px;
                }
            
            - type: custom:bar-card
              name: ' '
              positions:
                value: 'outside'
                indicator: 'off'
              unit_of_measurement: '%'
              height: 5px
              entities:
                - entity: sensor.dracaena_battery
                  icon: mdi:battery
              severity:
                - color: rgb(163,0,0)
                  from: 0
                  to: 15
                - color: rgb(26,204,147,0.33)
                  from: 16
                  to: 100
              style: |
                ha-card {
                  --paper-item-icon-color: rgb(47,186,229);
                  height: 40px;
                }
                ha-icon	 {
                  margin-top: -110px;
                  margin-right: -25px;
                }
                bar-card-backgroundbar  {
                  margin-top: -35px;
                  border-radius: 2.5px;
                }
                bar-card-currentbar  {
                  margin-top: -35px;
                  border-radius: 2.5px;
                }
                bar-card-value	 {
                  margin-top: -102.5px;
                  padding-left: 17.5px;
                }
            
            - type: markdown
              content: >
                <center>
                {{ (data | fromjson)['dracaenafw'] }}<br>
                {{ (data | fromjson)['dracaenalu'] }}
                </center>
              style: |
                ha-card {
                color: teal;
                margin-top: -60px;
                height: 40px;
                }
            - type: markdown
              content: >
                <img width="125" src="https://apps-cdn.athom.com/app/com.mi.flora/1/00700bec-b736-440b-9dc4-fd1b5ab8336a/drivers/flora/assets/images/large.png"/><br>
              style: |
                ha-card {
                  margin-top: -20px;
                  margin-left: -50px;
                }

#################################################################
#                                                               #
#                       Mi Flora Sensors                        #
#                                                               #
#################################################################

####################################################
#                                                  #
#               Mi Flora - Moisture                #
#                                                  #
####################################################

            - type: custom:bar-card
              name: ' '
              positions:
                value: 'outside'
                indicator: off
              target: 60
              unit_of_measurement: '%'
              height: 15px
              width: 70%
              entity: sensor.dracaena_moisture
              severity:
                - color: rgb(163,0,0)
                  from: 0
                  to: 15
                - color: rgb(26,204,147,0.33)
                  from: 16
                  to: 60
                - color: rgb(163,0,0)
                  from: 61
                  to: 100
              style: |
                ha-card {
                  --paper-item-icon-color: rgb(47,186,229);
                  border-radius: 2.5px;
                  height: 40px;
                  width: 91%;
                  margin-left: 27.5px;
                }
                ha-icon	 {
                  margin-top: -325px;
                  margin-right: -20px;
                }
                bar-card-value	 {
                  margin-top: -319px;
                  padding-left: 20px;
                }
                bar-card-backgroundbar	 {
                  margin-top: -162.5px;
                  margin-right: -25px;
                  border-radius: 2.5px;
                }
                bar-card-currentbar	 {
                  margin-top: -162.5px;
                  border-radius: 2.5px;
                }
                bar-card-targetbar  {
                  margin-top: -162.5px;
                }
                bar-card-markerbar  {
                  margin-top: -162.5px;
                } 
      

####################################################
#                                                  #
#             Mi Flora - Conductivity              #
#                                                  #
####################################################

            - type: custom:bar-card
              name: ' '
              positions:
                value: 'outside'
                indicator: 'off'
              target: 1500
              max: 2000
              unit_of_measurement: 'µS'
              height: 15px
              width: 68%
              entity: sensor.dracaena_conductivity
              severity:
                - color: rgb(163,0,0)
                  from: 0
                  to: 200
                - color: rgb(26,204,147,0.33)
                  from: 201
                  to: 1500
                - color: rgb(163,0,0)
                  from: 1501
                  to: 2000
              style: |
                ha-card {
                  --paper-item-icon-color: rgb(47,186,229);
                  border-radius: 2.5px;
                  height: 40px;
                  width: 92.5%;
                  margin-left: 28.5px;
                }
                ha-icon	 {
                  margin-top: -345px;
                  margin-right: -25px;
                  padding-right: 5px;
                }
                bar-card-value	 {
                  margin-top: -337.5px;
                  padding-left: 20px;
                }
                bar-card-backgroundbar	 {
                  margin-top: -172.5px;
                  border-radius: 2.5px;
                }
                bar-card-currentbar	 {
                  margin-top: -172.5px;
                  border-radius: 2.5px;
                }
                bar-card-targetbar  {
                  margin-top: -172.5px;
                }
                bar-card-markerbar  {
                  margin-top: -172.5px;
                }  

####################################################
#                                                  #
#             Mi Flora - Temperature               #
#                                                  #
####################################################

            - type: custom:bar-card
              name: ' '
              positions:
                value: 'outside'
                indicator: 'off'
              target: 35
              max: 50
              unit_of_measurement: '°C'
              height: 15px
              width: 70%
              entity: sensor.dracaena_temperature
              severity:
                - color: rgb(163,0,0)
                  from: 0
                  to: 10
                - color: rgb(26,204,147,0.33)
                  from: 11
                  to: 35
                - color: rgb(163,0,0)
                  from: 36
                  to: 50
              style: |
                ha-card {
                  --paper-item-icon-color: rgb(47,186,229);
                  border-radius: 2.5px;
                  height: 40px;
                  width: 92.5%;
                  margin-left: 28.5px;
                }
                ha-icon	 {
                  margin-top: -362.5px;
                  margin-right: -20px;
                }
                bar-card-value	 {
                  margin-top: -357.5px;
                  padding-left: 20px;
                }
                bar-card-backgroundbar	 {
                  margin-top: -182.5px;
                  border-radius: 2.5px;
                }
                bar-card-currentbar	 {
                  margin-top: -182.5px;
                  border-radius: 2.5px;
                }
                bar-card-targetbar  {
                  margin-top: -182.5px;
                }
                bar-card-markerbar  {
                  margin-top: -182.5px;
                }  

####################################################
#                                                  #
#                 Mi Flora - Light                 #
#                                                  #
####################################################

            - type: custom:bar-card
              name: ' '
              positions:
                value: 'outside'
                indicator: 'off'
              target: 50000
              max: 60000
              unit_of_measurement: 'Lx'
              height: 15px
              width: 70%
              entities:
                - entity: sensor.dracaena_light
                  icon: mdi:weather-sunny
              severity:
                - color: rgb(163,0,0)
                  from: 0
                  to: 2000
                - color: rgb(26,204,147,0.33)
                  from: 2000
                  to: 50000
                - color: rgb(163,0,0)
                  from: 50001
                  to: 100000
              style: |
                ha-card {
                  --paper-item-icon-color: rgb(47,186,229);
                  border-radius: 2.5px;
                  height: 40px;
                  width: 91.5%;
                  margin-left: 28.5px;
                }
                ha-icon	 {
                  margin-top: -384px;
                  margin-right: -20px;
                }
                bar-card-value	 {
                  margin-top: -377.5px;
                  padding-left: 20px;
                }
                bar-card-backgroundbar	 {
                  margin-top: -192.5px;
                  border-radius: 2.5px;
                }
                bar-card-currentbar	 {
                  margin-top: -192.5px;
                  border-radius: 2.5px;
                }
                bar-card-targetbar  {
                  margin-top: -192.5px;
                  border-radius: 2.5px;
                }
                bar-card-markerbar  {
                  margin-top: -192.5px;
                }  

      style: |
        ha-card  {
          border-radius: 2.5px;
          height: 317.5px;
        }
```
You will need to change the following with your specific config<br>

Line 35 - Change to image of your own plant<br>
Line 70 - Your Plant Battery Sensor<br>
Line 143 - Your Plant Moisture Sensor<br>
Line 203 - Your Plant Conductivity Sensor<br>
Line 262 - Your Plant Temperature Sensor<br>
Line 321 - Your Plant Light Sensor<br>
_If you aren't using device firmware or Last Update you can remove lines 104 & 105<br>

<hr --- </hr> 

Thanks to Dwains for creating a killing theme and inspiring me to get back into HA UI Design.<br>
You can find examples of how I have implemented this in [my own setup here](https://github.com/JamesMcCarthy79/Home-Assistant-Config/tree/master/config/dwains_theme)

