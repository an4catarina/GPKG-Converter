# GPKG Converter

This project gets the points from a GeoPackage file and converts them into a map with polygons.  
Each polygon covers 12 meters along the path of the points.  
The code calculates the average values inside each polygon and saves the result as a new .gpkg file and a map image.

## Requirements

- **Python version:** 3.11.4

To install the dependencies, run:

```bash
pip install -r requirements.txt
```

The project uses the following libraries:

- geopandas
- shapely
- numpy
- pandas
- contextily

## Running the Script

From the root folder of the project, execute:

```bash
python src/main.py
```

## Output

`src/output.gpkg`: GeoPackage file with polygons and their average values.

`src/polygons_map.png`: Image with the polygons over a satellite map.
