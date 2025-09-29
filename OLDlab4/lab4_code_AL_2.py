## create a .gdb and a garage feature
import arcpy

arcpy.env.workspace = r"C:\Ansley\Levine-online-GEOG676-fall2025\lab4"
folder_path = r"C:\Ansley\Levine-online-GEOG676-fall2025\lab4"
gdb_name = 'Test.gdb'
gdb_path = folder_path + '\\' + gdb_name
arcpy.CreateFileGDB_management(folder_path, gdb_name)

csv_path = r"C:\Ansley\Levine-online-GEOG676-fall2025\lab4\garages_2.csv"
garage_layer_name = 'Garage_Points'
garages = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)

input_layer = garages
arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
garage_points = gdb_path + '\\' + garage_layer_name

#open campus .gdb, copy building feature to the gdb
campus = r"C:\Ansley\Levine-online-GEOG676-fall2025\lab4\Campus_2.gdb"
buildings_campus = campus + '\Structures'
buildings = gdb_path + '\\' + 'Buildings'

arcpy.Copy_management(buildings_campus, buildings)

#Re-projection
spatial_ref = arcpy.Describe(buildings).spatialReference
arcpy.Project_management(garage_points, gdb_path + '\Garage_Points_reprojected', spatial_ref)

#buffer the garages
garageBuffered = arcpy.Buffer_analysis(gdb_path + '\Garage_Points_reprojected', gdb_path + '\Garage_Points_buffered', 150)

#Intersect our buffer with the buildings
arcpy.Intersect_analysis([garageBuffered, buildings], gdb_path + '\Garage_Building_Intersection', 'ALL')

arcpy.TableToTable_conversion(gdb_path + '\Garage_Building_Intersection.dbf', 'C:\Ansley\Levine-online-GEOG676-fall2025\lab4', 'nearbyBuildings.csv')


