# reducer.py
import sys

current_key = None
total_area = total_agri = total_barren = 0
total_yield = total_rainfall = 0
total_fertilizer_per_ha = 0
total_pesticide_per_ha = 0
count = 0

for line in sys.stdin:
    key, value = line.strip().split('\t')
    area_str, yield_str, agri_str, barren_str, rainfall_str, fertilizer_str, pesticide_str = value.split(',')

    try:
        area = float(area_str)
        yield_val = float(yield_str)
        agri = float(agri_str)
        barren = float(barren_str)
        rainfall = float(rainfall_str)
        fertilizer = float(fertilizer_str)
        pesticide = float(pesticide_str)
    except ValueError:
        continue

    if key != current_key:
        if current_key:
            avg_area = total_area / count if count else 0
            avg_agri = total_agri / count if count else 0
            avg_barren = total_barren / count if count else 0
            avg_yield = total_yield / count if count else 0
            avg_rainfall = total_rainfall / count if count else 0
            avg_fertilizer_per_ha = total_fertilizer_per_ha / count if count else 0
            avg_pesticide_per_ha = total_pesticide_per_ha / count if count else 0

            print(f"{current_key}\tAvg Area: {avg_area:.2f}, Avg Agri Land: {avg_agri:.2f}, "
                  f"Avg Barren Land: {avg_barren:.2f}, Avg Yield: {avg_yield:.2f}, Avg Rainfall: {avg_rainfall:.2f}, "
                  f"Fertilizer per ha: {avg_fertilizer_per_ha:.2f}, Pesticide per ha: {avg_pesticide_per_ha:.2f}")

        current_key = key
        total_area = total_agri = total_barren = 0
        total_yield = total_rainfall = 0
        total_fertilizer_per_ha = 0
        total_pesticide_per_ha = 0
        count = 0

    total_area += area
    total_agri += agri
    total_barren += barren
    total_yield += yield_val
    total_rainfall += rainfall
    total_fertilizer_per_ha += (fertilizer / area) if area > 0 else 0
    total_pesticide_per_ha += (pesticide / area) if area > 0 else 0
    count += 1

# Final key
if current_key:
    avg_area = total_area / count if count else 0
    avg_agri = total_agri / count if count else 0
    avg_barren = total_barren / count if count else 0
    avg_yield = total_yield / count if count else 0
    avg_rainfall = total_rainfall / count if count else 0
    avg_fertilizer_per_ha = total_fertilizer_per_ha / count if count else 0
    avg_pesticide_per_ha = total_pesticide_per_ha / count if count else 0

    print(f"{current_key}\tAvg Area: {avg_area:.2f}, Avg Agri Land: {avg_agri:.2f}, "
          f"Avg Barren Land: {avg_barren:.2f}, Avg Yield: {avg_yield:.2f}, Avg Rainfall: {avg_rainfall:.2f}, "
          f"Fertilizer per ha: {avg_fertilizer_per_ha:.2f}, Pesticide per ha: {avg_pesticide_per_ha:.2f}")
