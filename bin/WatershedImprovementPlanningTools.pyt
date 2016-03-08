import os, sys, shutil, arcpy
import traceback, time

def log(message):
    arcpy.AddMessage(message)
    with file(sys.argv[0]+".log", 'a') as logFile:
        logFile.write("%s:\t%s\n" % (time.asctime(), message))
    
class Toolbox(object):
    def __init__(self):
        self.label = "WIP tools"
        self.alias = ""
        self.tools = [TopoHydro, ImpCov, Runoff]
        
class TopoHydro(object):
    def __init__(self):
        self.label = "Topography and Hydrology Analysis"
        self.description = "Establishes the watershed and stream network"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Input Digital Elevation Model",
            name="DEM",
            datatype="DERasterDataset",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
            
        param1 = arcpy.Parameter(
            displayName="Analysis Mask",
            name="Mask",
            datatype="DEFeatureClass",
            parameterType="Optional",
            direction="Input",
            multiValue=False)  
        
        param2 = arcpy.Parameter(
            displayName="Threshold accumulation for Stream formation (acres)",
            name="StreamFormation",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
        
        params = [ param0, param1, param2 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
        	import arcpy
		from arcpy.sa import *

		# Check out any necessary licenses
		arcpy.CheckOutExtension("spatial")
		
		# Set Geoprocessing environments
		arcpy.env.snapRaster = "DEM"
		arcpy.env.mask = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\Mask"
		arcpy.env.overwriteOutput = True
		
		# Local variables:
		AnalysisMask = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\AnalysisMask"
		DEM = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\DEM"
		Mask = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\Mask"
		Fill_DEM = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\Fill_DEM"
		FlowDir = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\FlowDir"
		Output_drop_raster = ""
		FlowAcc = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\FlowAcc"
		Drainage_area_acres = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\Drainage_area_acres"
		reclass_1200 = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\reclass_1200"
		Streams = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\Streams1"
		
		# Process: Feature to Raster
		arcpy.FeatureToRaster_conversion(AnalysisMask, "mask", Mask, "40")
		
		# Process: Fill
		arcpy.gp.Fill_sa(DEM, Fill_DEM, "")
		
		# Process: Flow Direction
		arcpy.gp.FlowDirection_sa(Fill_DEM, FlowDir, "NORMAL", Output_drop_raster)
		
		# Process: Flow Accumulation
		arcpy.gp.FlowAccumulation_sa(FlowDir, FlowAcc, "", "FLOAT")
		
		# Process: Raster Calculator
		#arcpy.gp.RasterCalculator_sa("\"%FlowAcc%\" *1600  /43560", Drainage_area_acres)
		j=arcpy.GetRasterProperties_management (FlowAcc, 'CELLSIZEX')
		size=float(j.getOutput(0))
		Drainage_area_acres=Raster(FlowAcc)*j/43560
		arcpy.gp.Reclassify_sa(Drainage_area_acres, "Value", "0 800 NODATA;800 22526.390625 1", reclass_1200, "DATA")
		arcpy.gp.StreamToFeature_sa(reclass_1200, FlowDir, Streams, "SIMPLIFY")
            	log("Parameters are %s, %s, %s" % (parameters[0].valueAsText, parameters[1].valueAsText, parameters[2].valueAsText))
            
            
        except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return

class ImpCov(object):
    def __init__(self):
        self.label = "Imperviousness Analysis"
        self.description = "Impervious area contributions"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Impervious Areas",
            name="ImperviousAreas",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
            
        param1 = arcpy.Parameter(
            displayName="Lakes",
            name="Lakes",
            datatype="DEFeatureClass",
            parameterType="Optional",
            direction="Input",
            multiValue=False)  
        
        params = [ param0, param1 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
            log("Parameters are %s, %s" % (parameters[0].valueAsText, parameters[1].valueAsText)
            import arcpy
            from arcpy.sa import *
            arcpy.CheckOutExtension("spatial")
            arcpy.env.overwriteOutput = True
            DEM = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\DEM"
            Impervious = 'C:\Users\mabailey\Desktop\GIS_Based_Modeling\Lab_6\Lab06Data.gdb\Impervious'
            Reclass_800 = 'C:\Users\mabailey\Desktop\GIS_Based_Modeling\Lab_6\Lab06Data.gdb\Reclass_800'
            Impervious__3_ = "Impervious"
            Imperv_DEM = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\Imperv_DEM"
            block_stat = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\block_stat"
            agg = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\agg"
            Flowdir = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\Flowdir"
            Flow_acc_imper = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\Flow_acc_imper"
            fillDem = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\fillDem"
            Output_drop_raster = ""
            Unweighted_Flowacc = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\Unweighted_Flowacc"
            Percent_imperv = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\Percent_imperv"
            reclass = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\reclass"
            stream_rast_imp = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\stream_rast_imp"
            Stream_imp = "C:\\Users\\mabailey\\Desktop\\GIS_Based_Modeling\\Lab_6\\Lab06Data.gdb\\Stream_imp"
            fillDem=arcpy.gp.Fill_sa(DEM, fillDem, "")
            arcpy.gp.FlowDirection_sa(fillDem, Flowdir, "NORMAL", Output_drop_raster)
            arcpy.CalculateField_management(Impervious, "LENGTH", "1", "PYTHON", "")
            arcpy.FeatureToRaster_conversion(Impervious, "LENGTH", Imperv_DEM, "4")
            arcpy.gp.BlockStatistics_sa(Imperv_DEM, block_stat, "Rectangle 10 10 CELL", "SUM", "DATA")
            arcpy.gp.Aggregate_sa(block_stat, agg, "10", "MEAN", "EXPAND", "DATA")
            arcpy.gp.FlowAccumulation_sa(Flowdir, Flow_acc_imper, agg, "INTEGER")
            arcpy.gp.FlowAccumulation_sa(Flowdir, Unweighted_Flowacc, "", "FLOAT")
            Percent_imperv=Raster(Flow_acc_imper)/Raster(Unweighted_Flowacc)
            arcpy.gp.Reclassify_sa(Percent_imperv, "Value", "0 10 10;10 20 20;20 30 30;30 40 40;40 50 50;50 60 60;60 70 70;70 80 80;80 90 90;90 100 100", reclass, "DATA")
            stream_rast_imp=Raster(reclass)*Raster(Reclass_800)
            arcpy.gp.StreamToFeature_sa(stream_rast_imp, Flowdir, Stream_imp, "SIMPLIFY")
            import arcpy,numpy
            from arcpy.sa import *
            arcpy.env.overwriteOutput = True
            drainage_area=arcpy.Raster(arcpy.GetParameterAsText(0))
            IA=arcpy.Raster(arcpy.GetParameterAsText(1))
            #drainage_area="C:\Users\mabailey\Desktop\GIS_Based_Modeling\Lab_6\Lab06Data.gdb\Drainage_area_sqmiles"
            intervals={'RI_2':[144,0.691],'RI_5':[248,0.670],'RI_10':[334,0.665],'RI_25':[467,0.655],'RI_50':[581,0.650],'RI_100':[719,0.643]}
            for key,value in intervals.iteritems():
            	exp=value[1]
            	coeff=value[0]
            	RQ=(drainage_area**exp)*coeff
            	myRaster=28.5*(drainage_area**0.390)*(RQ**0.338)*(IA**0.436)
            	output='C:/Users/mabailey/Desktop/GIS_Based_Modeling/Lab_6/Lab06Data.gdb/urban_' + key
            	myRaster.save(output)

        except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return
        
class Runoff(object):
    def __init__(self):
        self.label = "Runoff Calculations"
        self.description = "Calculation of standard storm flows via USGS regression equations"
        self.canRunInBackground = False
        
        arcpy.env.Workspace = self.Workspace = os.path.split(__file__)[0]
        log("Workspace = " + arcpy.env.Workspace)
        arcpy.env.overwriteOutput = True       

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        param0 = arcpy.Parameter(
            displayName="Curve Number",
            name="Landuse",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input",
            multiValue=False)  
        
        params = [ param0 ]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return
            
    def execute(self, parameters, messages):
        try:
            log("Parameter is %s" % (parameters[0].valueAsText))
        except Exception as err:
            log(traceback.format_exc())
            log(err)
            raise err
        return
		
