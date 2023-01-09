cd ./resources
rm *.txt
cd ..
python3 ./parse_alerts.py
git add .
git commit -m "Updating Weather Alerts (AWS update)"
git push