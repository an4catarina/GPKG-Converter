import geopandas as gpd
import numpy as np
from shapely.ops import substring
from shapely.geometry import LineString
import contextily as cx
import pandas as pd


gdf = gpd.read_file('src/challenge.gpkg')

# Transforms to the coordinate system based on meters
gdf = gdf.to_crs('EPSG:31978')

line = LineString(gdf.geometry.tolist())  # Converts from points to LineString
length = line.length

width = 12
step_distance = 12

polygons = []
data = []

# Every 12m along the line, segments are created.
# For each segment, a 6m buffer is created on each side,
# resulting in polygons along the entire length.
for distance in np.arange(0, length, step_distance):
    segment = substring(line, distance, distance + width)
    segment_buffer = segment.buffer(width / 2, cap_style='flat')
    polygons.append(segment_buffer)

    # Filters points inside the current segment
    points_buffer = gdf[gdf.geometry.within(segment_buffer)]
    if not points_buffer.empty:
        # Calculates the average of numeric columns
        mean = (
            points_buffer
            .drop(columns="geometry")
            .mean(numeric_only=True)
        )

        timestamp = points_buffer["Time"].iloc[0]
        formatted_date = pd.to_datetime(timestamp).strftime("%Y%m%d%H%M%S")

        row = {"Time": formatted_date}

        # Formats the data
        for key in mean.index:
            if key in ["latitude", "longitude"]:
                row[key] = round(mean[key], 5)
            elif key == "speed":
                row[key] = round(mean[key], 2)
            elif key in ["moisture", "swath_width"]:
                row[key] = round(mean[key], 1)
            else:
                row[key] = mean[key]

        data.append(row)

# Generates the new GeoDataFrame with its attributes
gdf_poly = gpd.GeoDataFrame(data, geometry=polygons, crs=gdf.crs)
gdf_poly = gdf_poly.to_crs('EPSG:4326')
gdf_poly.to_file("src/output.gpkg", layer="buffers", driver="GPKG")

# Generates the image
gdf_img = gdf_poly.to_crs(epsg=3857)
plot = gdf_img.plot(
    figsize=(20, 20),
    edgecolor="black",
    facecolor="purple"
    )
cx.add_basemap(plot, source=cx.providers.Esri.WorldImagery)
fig = plot.get_figure()
fig.savefig("src/polygons_map.png", dpi=300, bbox_inches="tight")
