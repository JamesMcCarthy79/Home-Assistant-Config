<p align="center">
  <img src="https://github.com/JamesMcCarthy79/Home-Assistant-Config/blob/master/HA%20Pics/Snapshots.jpg" width="350"/>
</p>
<h1 align="center">Snapshots Package</h1>
<p align="center">Be sure to :star: my repo!</p>
<hr *** </hr>
<p align="center">This package utilises the HA snapshots component to automatically create a daily snapshot of my HA. I then use the Dropbox Sync Addon for HASSIO to store those backups away from my limited Raspberry Pi internal storage.</p>
<hr --- </hr> 

<h4 align="left">Package Credits:</h4>
<p align="left">danielwelch - https://github.com/danielwelch/hassio-dropbox-sync</br>

<hr --- </hr>

<h4 align="left">Package Dependencies:</h4>
<p align="left">- Dropbox Sync HASSIO Addon Installed</br>
<h4 align="left">Package Automations:</h4>
<h4 align="left">Daily Backup at 3am</h4>
<p align="left">This automation triggers an automated snapshot to be generated at 3am daily. I do it daily as I am always messing around with my config you can extend this to weekly if you dont want so many snapshots. Each one of my snapshots are 400mb so I will be added an auto cleanup of my backups folder in Hassio.</p>
<h4 align="left">Upload Dropbox at 4am</h4>
<p align="left">This automation triggers an automated snapshot to be synced with my dropbox folder in order to save space on my Pi SD Card. You could essentially backup to anywhere you want I like the convenience of it being rolled up into an addon I only need to call the service from my automation.</p>
<hr --- </hr>

| Take me back to the packages thanks!| [Packages](https://github.com/JamesMcCarthy79/Home-Assistant-Config/tree/master/config/packages) | 
| --- | --- |

<hr --- </hr>
