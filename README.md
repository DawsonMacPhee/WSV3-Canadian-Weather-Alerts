## WSV3 Canadian Weather Alerts Fileserver

This project takes Canadian weather alerts, converts them to a format usable by WSV3, and then hosts the files on a GitHub Pages fileserver for easy importing into the program.

### Usage

- Fork the repo
- If it's not already set up in your fork, set up GitHub Pages for the main branch in settings (`https://pages.github.com`)
- Clone the forked repo locally on your machine
- Download the most recent alert CAP files from `https://dd.weather.gc.ca/alerts/cap/`
- Place the downloaded files into the `./cap` directory and remove the old CAP files
- Run the python script using `python3 ./parse_alerts.py`
- Push to the repo using `git add .` then `git commit -m "Updated Alerts"` then `git push`
- Check that GitHub pages deployed by locating your newly generated warning files at `https://YOUR_USERNAME.github.io/WSV3-Canadian-Weather-Alerts/` (ex. `https://dawsonmacphee.github.io/WSV3-Canadian-Weather-Alerts/`) NOTE: It may take a couple minutes for the updates to deploy
- Launch WSV3 and set up `Severe Warnings` -> `Data` to import via the `Custom severe warnings server` option using the url `https://YOUR_USERNAME.github.io/WSV3-Canadian-Weather-Alerts/resources/` (ex. `https://dawsonmacphee.github.io/WSV3-Canadian-Weather-Alerts/resources/`)

### Help

If the program errors out for any reason, please raise a ticket stating what the error is and attach the CAP files you have in the `./cap` directory. NOTE: WSV3 loads data hourly - meaning that you'll need to run the python script once an hour with the most up to date CAP files in order to generate the correct warning file name.
