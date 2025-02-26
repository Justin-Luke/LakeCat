[![DOI Badge](https://zenodo.org/badge/70847646.svg)](https://zenodo.org/record/7967447)

# LakeCat

## Description: 
The LakeCat Dataset (https://www.epa.gov/national-aquatic-resource-surveys/lakecat-dataset) provides summaries of natural and anthropogenic landscape features for ~2.65 million streams, and their associated catchments, within the conterminous USA. This repo contains code used in StreamCat to process a suite of landscape rasters to watersheds for streams and their associated catchments (local reach contributing area) within the conterminous USA using the [NHDPlus Version 2](https://www.epa.gov/waterdata/nhdplus-national-hydrography-dataset-plus) as the geospatial framework.

## Necessary Python Packages and Installation Tips
The scripts for LakeCat rely on several python modules a user will need to install such as numpy, pandas, gdal, fiona, rasterio, geopandas, shapely, pysal, and ArcPy with an ESRI license (minimal steps still using ArcPy).  We used the conda package manager to install necessary python modules. Note that package configurations and dependencies are sensitive and can change - in particular, setting up an environment with a working version of both `geopandas` and `arcpy` can be challenging. Our working version of the conda environment is contained in the StreamCat.yml file in the repository, and our essential packages and versions when code was last used are listed below - note that other configurations may work, we simply have verified this particular combination (Windows 64 and Python 3.7.10):

| Package       | Version       | 
| ------------- |--------------:|
| python        | 3.7.10        | 
| fiona         | 1.8.18        | 
| gdal          | 3.1.4=py37    | 
| geopandas     | 0.9.0         |  
| geos          | 3.8.1         |
| libgdal       | 3.1.4         |
| numpy         | 1.19.5        |
| pandas        | 1.2.3         |
| pyproj        | 2.6.1         |
| rasterio      | 1.2.1=py37    |
| shapely       | 1.7.1         |

If you are using Anaconda, creating a new, clean 'StreamCat' environment with these needed packages can be done one of several ways:

* In your conda shell, add one necessary channel and then download the streamcat environment from the Anaconda cloud:
  + conda config --add channels conda-forge
  + conda env create mweber36/StreamCat
  
* Alternatively, using the streamcat.yml file in this repository, in your conda shell cd to the directory where your streamcat.yml file is located and run:
  + conda env create -f StreamCat.yml
  
* To build environment yourself, we [followed the steps suggest here](https://www.e-education.psu.edu/geog489/node/2348) which are:
  + conda create -n StreamCat -c conda-forge python=3.7 anaconda gdal=3.1.4 vs2015_runtime=14.28.29325 numpy=1.19.5 jupyter pandas geopandas matplotlib cartopy beautifulsoup4 shapely rpy2=3.4.1 simplegeneric r-raster=3.4_5 r-dismo=1.3_3 r-maptools pyproj=2.6.1.post1 rasterio

* Activate the new environment:

  + conda activate StreamCat

* 
* To open Spyder, type the following at the conda prompt
  + activate Streamcat
  
  Then

  + Spyder

Finally, to use arcpy in this new environment, you will need to copy several ArcPro files and folders to your new environment as follows:

+ C:/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/Lib/site-packages/Arcgisscripting 

+ C:/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/Lib/site-packages/arcpy_wmx

+ C:/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/Lib/site-packages/Gapy

To your environment directory which should look something like:

+ C:/Users/mweber/AppData/Local/Continuum/anaconda3/envs/StreamCat/Lib/site-packages

Note that the exact paths may vary depending on the version of ArcGIS and Anaconda you have installed and the configuration of your computer


## How to Run Scripts 

### The scripts make use of 'control tables' to pass all the particular parameters to the two primary scripts: 

+ [LakeCat.py](https://github.com/USEPA/LakeCat/blob/master/LakeCat.py).
+ [MakeFinalTables_LakeCat.py](https://github.com/USEPA/LakeCat/blob/master/MakeFinalTables_LakeCat.py).  

In turn, these scripts rely on a set of functions in [LakeCat_functions.py](https://github.com/USEPA/LakeCat/blob/master/LakeCat_functions.py). 

A table with all required parameters is used to process landscape layers in LakeCat:
+ [ControlTable_LakeCat](https://github.com/USEPA/LakeCat/blob/master/ControlTable_LakeCat.csv)


### Running LakeCat.py to generate new LakeCat metrics

After editing the control tables to provide necessary information, such as directory paths, the following stesps will excecute processes to generate new watershed metrics for the conterminous US. All examples in the control table are for layers (e.g., STATSGO % clay content of soils) that were processed as part of the LakeCat Dataset. This example assumes run in Anaconda within Conda shell.

1. Edit [ControlTable_LakeCat](https://github.com/USEPA/LakeCat/blob/master/ControlTable_LakeCat.csv) and set desired layer's "run" column to 1. All other columns should be set to 0
2. Open a Conda shell and type "activate LakeCat" 
3. At the Conda shell type: "Python<space>"
4. Drag and drop "LakeCat.py" to the Conda shell from a file manager followed by another space
5. Drag and drop the control table to the Conda shell

Final text in Conda shell should resemble this: python C:\some_path\LakeCat.py  C:\some_other_path\ControlTable.csv


## EPA Disclaimer
The United States Environmental Protection Agency (EPA) GitHub project code is provided on an "as is" basis and the user assumes responsibility for its use.  EPA has relinquished control of the information and no longer has responsibility to protect the integrity , confidentiality, or availability of the information.  Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by EPA.  The EPA seal and logo shall not be used in any manner to imply endorsement of any commercial product or activity by EPA or the United States Government.
