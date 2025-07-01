# mapper.py
import sys

for line in sys.stdin:
    if 'Crop' in line:
        continue  # skip header

    parts = line.strip().split(',')
    if len(parts) >= 12:
        crop = parts[0].strip()
        state = parts[3].strip()
        area = parts[4].strip()
        yield_val = parts[9].strip()
        total_agri_land = parts[10].strip()
        barren = parts[11].strip()
        rainfall = parts[6].strip()
        fertilizer = parts[7].strip()
        pesticide = parts[8].strip()

        if area and yield_val and total_agri_land and barren and rainfall and fertilizer and pesticide:
            print(f"{state},{crop}\t{area},{yield_val},{total_agri_land},{barren},{rainfall},{fertilizer},{pesticide}")
