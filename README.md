# WSV3 Canadian Weather Alerts Fileserver

This project takes Canadian weather alerts, converts them to a format usable by WSV3 (`https://wsv3.com`), and then hosts the files on a GitHub Pages fileserver for easy importing into the program.

## Usage

1. Fork the repo
2. If it's not already set up in your fork, set up GitHub Pages for the main branch in settings ([https://pages.github.com](https://pages.github.com))
3. Clone the forked repo locally on your machine
4. Load alerts using one of the two options below
5. Push to the repo using `git add .` then `git commit -m "Updated Alerts"` then `git push`
6. Check that GitHub pages deployed by locating your newly generated warning files at `https://YOUR_USERNAME.github.io/WSV3-Canadian-Weather-Alerts/` (ex. [https://dawsonmacphee.github.io/WSV3-Canadian-Weather-Alerts/](https://dawsonmacphee.github.io/WSV3-Canadian-Weather-Alerts/)) NOTE: It may take a couple minutes for the updates to deploy
7. Launch WSV3 and set up `Severe Warnings` -> `Data` to import via the `Custom severe warnings server` option using the url `https://YOUR_USERNAME.github.io/WSV3-Canadian-Weather-Alerts/resources/` (ex. [https://dawsonmacphee.github.io/WSV3-Canadian-Weather-Alerts/resources/](https://dawsonmacphee.github.io/WSV3-Canadian-Weather-Alerts/resources/))

### To Load Current Alerts Automatically
1. Run the python script using `python3 ./parse_alerts.py`

### To Load Alert Files Manually
1. Download the most recent alert CAP files from [https://dd.weather.gc.ca/alerts/cap/](https://dd.weather.gc.ca/alerts/cap/)
2. Place the downloaded files into the `./cap` directory and remove the old CAP files
3. Run the python script using `python3 ./parse_alerts.py --CAP`

## Cronjob Execution
If prefered, the given cronjob.sh file can be used to automate updates. Instructions to start a cronjob on linux can be found here: https://linuxhint.com/schedule_crontab_job_every_hour/. Please note that in order for a cronjob to execute, the computer it's running on must be turned on.

## Help

- If the program errors out for any reason, please raise a ticket stating what the error is and attach the CAP files you have in the `./cap` directory. 
- WSV3 loads data hourly - meaning that you'll need to run the python script once an hour, at the turn of the hour, with the most up to date CAP files in order to generate the correct warning file name.
- À l'heure actuelle, les données chargées sont en anglais. Il existe cependant des fichiers CAP français, donc s'il y a une demande pour publier une version française, il suffit de créer un ticket et je peux modifier le programme sans trop de difficulté.
