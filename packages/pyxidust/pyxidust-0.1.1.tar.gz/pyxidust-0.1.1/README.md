# 🧚‍♀️Pyxidust
### Unleash the magic of Python with the Pyxidust general-purpose library!
### Pyxidust contains many tools for working with ESRI ArcGIS Pro software,
### and basic utilities that improve your quality of life!
<br>

### [1. Dependencies](#dependencies)
### [2. Arc Module](#arc-module)
### [3. Utils Module](#utils-module)
### [4. Change Log](#change-log)
<br>

# ⚗️Dependencies
### Python 3.7+, Pandas, Microsoft Windows, ESRI ArcGIS Pro license
<br>

# 🌍️ Arc Module
### **Create Index Function**
### Joins file metadata (name/path/modified) with layers/layouts/maps via a
### global ID for each .aprx file in the specified directory.
```py
# create_index(directory)
from pyxidust.arc import create_index
create_index(directory=r'\\folder')
```
<br>

### **CSV To GDB Function**
### Converts a .csv file to a geodatabase table.
```py
# csv_to_gdb(csv, gdb, table)
from pyxidust.arc import csv_to_gdb
csv_to_gdb(csv=r'\\.csv', gdb=r'\\.gdb', table='Output')
```
<br>

### **Cubic Volume Function**
### Calculates volume in cubic yards using a cut/fill operation on two input
### rasters with the same cell size and coordinate system.
```py
# cubic_volume(original, current, gdb, polygons)
from pyxidust.arc import cubic_volume
cubic_volume(original=r'\\', current=r'\\', gdb=r'\\.gdb', polygons='poly')
```
<br>

### **Excel To GDB Function**
### Converts a Microsoft Excel workbook sheet to an ArcGIS geodatabase table.
```py
# excel_to_gdb(workbook, gdb, table, sheet=None)
from pyxidust.arc import excel_to_gdb
excel_to_gdb(workbook=r'\\.xlsx', gdb=r'\\.gdb', table='Output', sheet='Sheet 1')
```
<br>

### **Place Anno Function**
### Sets reference scale from a layer in an ArcGIS PRO project and creates
### annotation feature classes for all layers with visible labels.
```py
# place_anno(pro_obj, map_name, lay_name, fra_name, lyr_idx, adjust, gdb, suffix)
import arcpy
from pyxidust.arc import place_anno
project = arcpy.mp.ArcGISProject(r'\\.aprx')

# returns extent, scale; unpack or call without variables
extent, scale = place_anno(pro_obj=project, map_name='Map', lay_name='Layout',
    fra_name='Map Frame', lyr_idx=0, adjust=1.1, gdb=r'\\.gdb', suffix='A')
```
<br>

### **Plot CSV Function**
### Converts X/Y/Z coordinates in a .csv file to a shapefile and adds it to
### a map in an ArcGIS PRO project.
```py
# plot_csv(pro_obj, map_name, csv, crs, output, x_name, y_name, z_name=None)
import arcpy
from pyxidust.arc import plot_csv
project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
# z-values are optional
plot_csv(pro_obj=project_, map_name='Map', csv=r'\\.csv', crs=r'\\.prj',
    output=r'\\.shp', x_name='X', y_name='Y', z_name=None='Z')
```
<br>

### **Plot Excel Function**
### Converts X/Y/Z coordinates in a spreadsheet workbook to a shapefile and
### adds it to a map in an ArcGIS PRO project.
```py
# plot_excel(workbook, pro_obj, map_name, crs, output, x_name, y_name, z_name=None, sheet=None)
import arcpy
from pyxidust.arc import plot_excel
project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
# z-values and sheet name are optional
plot_excel(workbook=r'\\.xlsx', pro_obj=project_, map_name='Map', crs=r'\\.prj',
    output=r'\\.shp', x_name='X', y_name='Y', z_name='Z', sheet='Sheet1')
```
<br>

### **Print Info Function**
### Prints map/layout/layer names and data sources in an ArcGIS PRO project.
### Useful for troublesome projects that will not open due to memory issues.
```py
# print_info(pro_obj)
import arcpy
from pyxidust.arc import print_info
project = arcpy.mp.ArcGISProject(r'\\.aprx')
print_info(pro_obj=project)
```
<br>

### **Print Layers Function**
### Prints the properties of all layers in a map in an ArcGIS PRO project.
```py
# print_layers(pro_obj, map_name)
import arcpy
from pyxidust.arc import print_layers
project = arcpy.mp.ArcGISProject(r'\\.aprx')
print_layers(pro_obj=project, map_name='Map')
```
<br>

### **Set Default Function**
### Updates home folder/default geodatabase/toolbox in an ArcGIS PRO project.
```py
# set_default(pro_obj, home, gdb, toolbox)
import arcpy
from pyxidust.arc import set_default
project = arcpy.mp.ArcGISProject(r'\\.aprx')
set_default(pro_obj=project, home=r'\\folder', gdb=r'\\.gdb',
    toolbox=r'\\.tbx')
```
<br>

### **Turn Off Function**
### Turns off layers in a map in an ArcGIS PRO project if the layer index
### position is found in the input list.
```py
# turn_off(pro_obj, map_name, lyr_idx)
import arcpy
from pyxidust.arc import turn_off
project = arcpy.mp.ArcGISProject(r'\\.aprx')
turn_off(pro_obj=project, map_name='Map', lyr_idx=[0,1,2])
```
<br>

### **Zoom To Function**
### Sets reference scale from a layer in an ArcGIS PRO project and zooms the
### layout to the layer extent.
```py
# zoom_to(pro_obj, map_name, lay_name, fra_name, lyr_idx, adjust)
import arcpy
from pyxidust.arc import zoom_to
project = arcpy.mp.ArcGISProject(r'\\.aprx')
zoom_to(pro_obj=project, map_name='Map', lay_name='Layout', fra_name='Map Frame',
    lyr_idx=0, adjust=1.1)
```
<br>

# 🛸 Utils Module
### **Change Name Function**
### Renames files in a folder via incremental serial numbers per a certain
### file extension.
```py
# change_name(extension, directory, serials)
from pyxidust.utils import change_name
change_name(extension='.jpg', directory=r'\\folder', serials=r'\\Serials.txt')
```
<br>

### **Get Metadata Function**
### Crawls a directory and returns metadata per a certain file extension.
```py
# get_metadata(extension, directory)
from pyxidust.utils import get_metadata
get_metadata(extension='.jpg', directory=r'\\folder')
```
<br>

# 🧪Change Log

**0.1.0** (1/23/2023):
- Added the 'Arc' module with the following functions:
create_index, csv_to_gdb, cubic_volume, excel_to_gdb, place_anno, plot_csv,
plot_excel, print_info, print_layers, set_default, turn_off, zoom_to

- Added the get_metadata function to the 'Utils' module

- The file_rename function in the 'Utils' module has become the change_name
function with the same arguments

**0.0.1** (11/10/2022):
- Initial release and birth of Pyxidust!
<br>
