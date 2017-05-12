# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 10:34:36 2015

@author: Rdebbout
"""

import arcpy
import pandas as pd
import pysal as ps
from datetime import datetime

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

# List to iterate thru for table names of our existing StreamCat dataset
metricTableNames = ['AgMidHiSlopes_Region','CanalDensity_Region','Dams_Region','Elevation_Region',\
                    'EPA_FRS_Region','ImperviousSurfaces2006_Region','Lithology_Region','Mines_Region',\
                    'NLCD2006_Region','NLCD2006LnBf100_Region','NLCD2011_Region','PRISMPrecip_Region',\
                    'RoadDensity_Region','RoadStreamCrossings_Region','Runoff_Region','STATSGO_Set1_Region',\
                    'STATSGO_Set2_Region','USCensus2010_Region']   
                    
# DataFrame created to link together data to dig into NHD folder structure and be iterated thru
lookup= pd.DataFrame({ 
  'hydro.rgns':["01","02","03S","03N","03W","04","05","06","07","08","09","10L","10U","11","12","13","14","15","16","17","18"],
  'rgns':["NE","MA","SA","SA","SA","GL","MS","MS","MS","MS","SR","MS","MS","MS","TX","RG","CO","CO","GB","PN","CA"]})

#--------------------------------------------------------
# !!!DIRECTORIES TO WRITE INFO TO!!!
# directory for resulting metric tables madeup of on-network catchments
output_dir = 'D:\\Projects\\lakesAnalysis\\Output\\on_network2'
# Shapefile or gdb feature layer to store on and off-network lakes
outfeature = 'D:/Projects/lakesAnalysis/IsolatedLakes_RD.gdb/NetworkLakes'
outfeature2 = 'D:/Projects/lakesAnalysis/IsolatedLakes_RD.gdb/IsolatedLakes'
#--------------------------------------------------------
# directory where StreamCat tables are located
metricTable_dir = 'L:\\Priv\\CORFiles\\Geospatial_Library\\Data\\Project\\SSWR1.1B\\FTP_Staging\\StreamCat\\HydroRegions'
# !!!CHANGE NHDdir below to your NHD directory also and the rest is good to go!!!
#--------------------------------------------------------

# count is used when iterating to use arcpy.CopyFeatures_management() tool first pass thru
# and then arcpy.Append_management() the remaining iterations to add selected lakes to the files
count = 0
startTime = datetime.now()
for i, hr in lookup.iterrows():
    print 'on region ' + hr[1] + ' and hydro number ' + hr[0]
    # create directories to NHD data
    NHDdir = "C:/Users/Rdebbout/temp/NHDPlusV21/NHDPlus%s/NHDPlus%s"%(hr[1],hr[0])
    NHDWaterbody = "%s/NHDSnapshot/Hydrography/NHDWaterbody.shp"%(NHDdir)
    NHDWaterbodyDBF = "%s/NHDSnapshot/Hydrography/NHDWaterbody.dbf"%(NHDdir)
    NHDFlowlineDBF = "%s/NHDSnapshot/Hydrography/NHDFlowline.dbf"%(NHDdir)
    NHDPlusFlowlinVAADBF = '%s\\NHDPlusAttributes\\PlusFlowlineVAA.dbf'%(NHDdir)
    NHDCatchmentDBF = '%s\\NHDPlusCatchment\\Catchment.dbf'%(NHDdir)     
    # get waterbodies and select out by FTYPE
    #--------------------------------------------------------
    db = ps.open(NHDWaterbodyDBF)
    wb = pd.DataFrame(db[:]) 
    wb.columns = map(str.upper, db.header)
    db.close()
    wb = wb.loc[wb['FTYPE'].isin(['LakePond','Reservoir'])]
    #--------------------------------------------------------
    # get flowline table into pandas data frame 
    db = ps.open(NHDFlowlineDBF)
    fl = pd.DataFrame(db[:])
    fl.columns = map(str.upper, db.header) 
    db.close()
    #--------------------------------------------------------
    # get catchment table into pandas data frame 
    db = ps.open(NHDCatchmentDBF)
    cat = pd.DataFrame(db[:])
    cat.columns = map(str.upper, db.header)
    db.close()
    #--------------------------------------------------------
    flowcat = pd.merge(cat,fl,left_on='FEATUREID',right_on='COMID', how='inner') 
    join = pd.merge(wb,flowcat,left_on='COMID', right_on='WBAREACOMI', how='left')
    #--------------------------------------------------------
    # get NHDPlusFlowlineVAA table into pandas data frame
    db = ps.open(NHDPlusFlowlinVAADBF)
    vaa = pd.DataFrame(db[:])
    vaa.columns = map(str.upper, db.header)
    db.close()  
    #--------------------------------------------------------
    # Merge VAA table on to joined table of catchment, waterbody, and flowline tables
    joinVAA = pd.merge(join,vaa,left_on='COMID_y',right_on='COMID', how='left')
    # create data frame to link catchment COMID to waterbody COMID
    df = pd.DataFrame(columns=('catCOMID', 'wbCOMID'))
    # iterate through table while grouping by the waterbody COMID to select out associated catchments
    for name, group in joinVAA.groupby('COMID_x'):
        if not pd.isnull(group.FEATUREID).any():
            hydro = pd.Series.min(group.HYDROSEQ)
            group = group[group.HYDROSEQ == hydro]           
            s = pd.DataFrame({'catCOMID':pd.Series([int(group.COMID_y.values[0])]),'wbCOMID':pd.Series([int(group.COMID_x.values[0])])})
            df = df.append(s)
    df.to_csv('D:\\Projects\\lakesAnalysis\\On_Network_LakeCOMs\\LakeCOMs' + hr[0] + '.csv', index=False)
    del df, joinVAA, vaa, cat, fl, wb
    
