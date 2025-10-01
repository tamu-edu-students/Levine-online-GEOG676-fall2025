# -*- coding: utf-8 -*-
import time
import arcpy


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [GraduatedColorsRenderer]


class GraduatedColorsRenderer(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "graduatedcolor"
        self.description = "create a graduated colored map based on a specific attribute of a layer"
        self.canRunInBackground = False
        self.category = "MapTools"

    def getParameterInfo(self):
        """Define the tool parameters."""
        #the original project name
        param0 = arcpy.Parameter(
            displayName ="Input ArcGIS Pro Project Name",
            name="aprxInputName",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )

        #which layer to classify to create a color map
        param1 = arcpy.Parameter(
            displayName="Layer to Classify",
            name="LayertoClassify",
            datatype="GPLayer",
            parameterType="Required",
            direction="Input"
        )

        #output folder location
        param2 = arcpy.Parameter(
            displayName="Output Location",
            name="OutputLocation",
            datatype="DEFolder",
            direction="Input"
        )

        #output project name
        param3 = arcpy.Parameter(
            displayName="Output Project Name",
            name="OutputProjectName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        params = [param0, param1, param2, param3]
        return params

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        #Define progressor variables
        readTime = 3 #the time for users to read the progress
        start = 0 # beginning position of the progressor (starts at 0%)
        max = 100 # end position (ends at 100%)
        step = 33 # The progress interval to move the progressor along (divides the entire process into 3 parts)

         # setup progressor
        arcpy.SetProgressor("step", "Validating Project File...", start, max, step)
        time.sleep(readTime) # Pause the execution for 3 seconds (gives user 3 seconds to read message)
        # add message to the results pane
        arcpy.AddMessage("Validating Project File...")
        
         # project file
        project = arcpy.mp.ArcGISProject(parameters[0].valueAsText) # Param 0 is the input project file

        # grab the first instance of a map from the .aprx
        campus = project.listMaps('Map')[0] #access to the first map

        #increment progressor 
        arcpy.SetProgressorPosition(start + step) #now is 33% completed
        arcpy.SetProgressorLabel("Finding your map layer...")
        time.sleep(readTime)
        arcpy.AddMessage("Finding your map layer...")

        #Loop through  the layers of the map
        for layer in campus.listLayers():
            #check if the layer is a feature layer
            if layer.isFeatureLayer:
                #copy the layer's symbology
                symbology = layer.symbology
                #make sure the symbology has renderer attribute
                if hasattr(symbology, 'renderer'):
                    #Check layer name
                    if layer.name == parameters[1].valueAsText: #check if the layer name matches the input layer

                        #increment progressor
                        arcpy.SetProgressorPosition(start + step*2) #now is 66% completed
                        arcpy.SetProgressorLabel("Calculating and classifying...")
                        time.sleep(readTime)
                        arcpy.AddMessage("Calculating and classifying...")

                        #update the copy's renderer to "graduated colors renderer"
                        symbology.updateRenderer('GraduatedColorsRenderer')

                        #tell arcpy which field we want to base our chloropleth off of 
                        symbology.renderer.classificationField = "Shape_Area"

                         #set how many classes we'll have for the map
                        symbology.renderer.breakCount = 5

                        #set color ramp
                        symbology.renderer.colorRamp = project.listColorRamps('Oranges (5 Classes)')[0]

                        #set the layer's actual symbology equal to the copy's
                        layer.symbology = symbology

                        arcpy.AddMessage("Finish Generating Layer...")
                    else:
                        print("No layers found")

        #Increment Progressor
        arcpy.SetProgressorPosition(start + step*3) #now is 99% completed
        arcpy.SetProgressorLabel("Saving...")
        time.sleep(readTime)
        arcpy.AddMessage("Saving...")

        project.saveACopy(parameters[2].valueAsText + "\\" + parameters[3].valueAsText + ".aprx")
        #param 2 is the folder location and param 3 is the name of the new project
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
