import os

files = os.listdir("reports/radar_charts")

print("Charts:", len(files))

print(files[:10])