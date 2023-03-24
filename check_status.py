from rachiopy import Rachio
import os, sys
import datetime

rachio = Rachio(os.getenv("API_KEY"))
_, resp = rachio.person.info()
_, person = rachio.person.get(resp.get("id"))
device = person.get("devices")[0]
device_id = device.get("id")
device_status = device["status"]
print(f"STATUS: {device_status}")
_, resp = rachio.device.get(device_id)
zones = resp.get("zones")
now = datetime.datetime.now()
max_days_ago = now - now
for zone in zones:
	if zone.get("lastWateredDate"):
		days_ago = now - datetime.datetime.fromtimestamp(zone.get("lastWateredDate")/1000)
		print(f"({zone.get('zoneNumber')}) {days_ago}")
		max_days_ago = days_ago if days_ago > max_days_ago else max_days_ago

if max_days_ago.days > 0:
	print(f"ALERT: {max_days_ago.days} DAYS WITH NO WATER")

if max_days_ago.days > 0 or device["status"] == "OFFLINE":
	sys.exit(1)
sys.exit(0)