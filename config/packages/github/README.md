<p align="center">
  <img src="https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/www/lovelace/home/git.png" width="600"/>
</p>
<h1 align="center">Github Status Package</h1>
<p align="center">Be sure to :star: my repo!</p>
<hr *** </hr>
<p align="center">This package pulls the statisitics from my Github Repo and creates sensors for stars, issues, subscribers & forks. I then use these sensors to get notifications through Node-RED if any of them changes state.</p>
<hr --- </hr> 

<h4 align="left">Package Credits:</h4>

Adam - [SilvrrGIT](https://github.com/SilvrrGIT/HomeAssistant)

<hr --- </hr>

<h4 align="left">Package Dependencies:</h4>

- Github Repo :wink:

<h4 align="left">Package Automations:</h4>
<h4 align="left">Notifications</h4>

I am monitoring each of the sensors created in the package with Node-RED and if any of them changes state they will send me a notification depending on my home presence. If I'm at home it will announce over TTS and flash my coloured bulbs blue, if I'm away if will notify me via pushbullet.

I am also monitoring "milestones" for each of them, if this target is met it will do the same as above but play/send a different message.
<hr --- </hr>

| Automations! | [Node-RED-Flow](https://github.com/JamesMcCarthy79/Home-Assistant-Config/tree/master/config/packages/github/Node-RED-Flow) | [YAML](https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/config/packages/github/github.yaml) |
| --- | --- | --- |

| Take me back to the packages thanks!| [Packages](https://github.com/JamesMcCarthy79/Home-Assistant-Config/tree/master/config/packages) | 
| --- | --- |

<hr --- </hr>
