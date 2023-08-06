# HDMapConverter (hdmc)
A tool for converting from Lanelet2 maps to Apollo OpenDRIVE maps

## Apollo OpenDrive
Apollo is an architecture for autonomous driving developed by Baidu. They have made a modified version of the OpenDrive standard to suit their needs better. 

This project aims to create a tool for generating maps in the Apollo version of the OpenDrive specification using data from Lanelet2 maps.

## Installation from source to system
In the ```converter/``` folder (containing ```setup.py```):
```
pip install -e ./
```

## Usage
```
usage: python3 -m hdmc [-h] input_file output_file

positional arguments:
  input_file                  Input filename
  output_file                 Output filename

optional arguments:
  -h, --help            show this help message and exit
```

## Output
``base_map.txt`` is received as result. To use it in Apollo architecture, ``bin_map_generator`` and ``generate_routing_topo_graph`` scripts should be used.