cd ./resources
rm *.txt
cd ..
python3.10 ./parse_alerts.py
git add .
git commit -m "Updating Weather Alerts (Cronjob update)"
git push