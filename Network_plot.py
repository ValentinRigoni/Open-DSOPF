"""
#### OPF for unbalance three-phase network from OpenDSS ####
#### Valentin Rigoni and Andrew Keane ######################
#### University College Dublin, Ireland ####################
#### email: valentinrigoni09@gmail.com #####################
####        andrew.keane@ucd.ie        #####################

Contributions:
    This model available for anyone to use.
    If you use the model, get in touch and let us know about your work.

Citation:
    When using this model and any of the provided functions and modified network models, please cite our paper which describes them: 
    V. Rigoni and A. Keane, "Open-DSOPF: an open-source optimal power flow formulation integrated with OpenDSS", 2020 IEEE Power & Energy Society General Meeting, 2020.
"""

## IMPORTANT ##
"""
    If using the provided feeders, remember that branches have been simplified to reduce the number of nodes (eliminating unnecesary branches and merging those that have the same cable data and no load in between)
    Therefore, some lines may go straight to the location of a customer instead of following a realistic geographical path
"""


## Input data ##
Feeder_names= ['Feeder1','Feeder2','Feeder3']
Feeder_colors = 'c'

## Import all the python and OpenDSS libraries needed for the script
import os
import pandas as pd # High level data manipulation
import matplotlib.pyplot as plt
import win32com.client # To access the OpenDSS COM module
from win32com.client import makepy
import sys
import numpy as np 
import math
from Main_packages.Extract_OpenDSS_data import Extract_data_OpenDSS  

""" FOLDERS """
# Get directory path
Main_path = os.path.dirname(os.path.realpath(__file__))

""" 
CREATE THE OpenDSS CIRCUIT
This will be handy for getting some extra network data
Applicaitons:
        Using OPF as benchmark for a ANM solution implemented in OpenDSS
"""
# Create OpenDSS object
# The COM module has a variety of interfaces, and creating variables to access them directly is handy.
sys.argv = ["makepy", "OpenDSSEngine.DSS"]
makepy.main()
dssObj = win32com.client.Dispatch("OpenDSSEngine.DSS")
dssText = dssObj.Text # to excecute OpenDSS text commands
dssCircuit = dssObj.ActiveCircuit # Use it to access the elements in the circuit (e.g., capacitors, buses, etc.)
dssSolution = dssCircuit.Solution
dssElem = dssCircuit.ActiveCktElement
dssBus = dssCircuit.ActiveBus 

# This is the datapath were the dss file is. Results will also be saved here.
dssText.Command = 'set datapath=' + Main_path
dssText.Command = 'Clear' # clear any existing circuit in the engine
dssText.Command ='Set DefaultBaseFrequency=50'

# Vsource
dssText.Command = 'Redirect ' + Main_path + '/Network_data/Network_model/OpenDSS_NewCircuit.txt' 
# Transformer
dssText.Command = 'Redirect ' + Main_path + '/Network_data/Network_model/OpenDSS_Transformer.txt'  
# Line codes
dssText.Command = 'Redirect ' + Main_path + '/Network_data/Network_model/Cable_data/OpenDSS_line_types.txt' 
# Lines and loads
for i_feeder in Feeder_names:
    # Compile OpenDSS codes for lines, loads and monitors
    dssText.Command = 'Redirect ' + Main_path + '/Network_data/Network_model/' + i_feeder + '/OpenDSS_Lines.txt' 
    dssText.Command = 'Redirect ' + Main_path + '/Network_data/Network_model/' + i_feeder + '/OpenDSS_Loads.txt' 
    dssText.Command = 'Redirect ' + Main_path + '/Network_data/Network_model/' + i_feeder + '/OpenDSS_monitors.txt'

dssText.Command = 'set datapath=' + Main_path

# Solve options 
dssText.Command = 'set controlmode=static'
dssText.Command = 'set mode=snapshot'
dssSolution.Solve()
if dssSolution.Converged:
    print('Solution Converged')
else:
    raise ValueError('Solution did not Converge')

# Data sets are available in the csv files in 'Network model'. However, it can also be extracted from OpenDSS - be carefull with naming, OpenDSS only works with all lower case
[Lines_set,Line_data_DSS,Bus_set,Bus_Vnom,Nodes_set,Loads_set,Load_phase,Load_bus,Load_Vnom,Transformer_rating] = Extract_data_OpenDSS(math,np,pd,dssCircuit)
Bus_set_no_slack = np.delete(Bus_set, np.where(Bus_set == 'slack')[0][0])


## plot script ##
dir_path = os.path.dirname(os.path.realpath(__file__))

fig, ax = plt.subplots(1, figsize=(12, 7), tight_layout=False)
count=-1
XY_coordinates = pd.DataFrame()
for Feeder_name in Feeder_names:
    count+=1
    # Get bus coordinates
    XY_coordinates_aux = pd.read_excel(dir_path + '\\Network_data\\Network_model\\' + Feeder_name + '\\' + 'XY_Position.xls',index_col=0) # XY coordiantes
    XY_coordinates_aux.index=[x.lower() for x in XY_coordinates_aux.index]
    XY_coordinates = XY_coordinates.append(XY_coordinates_aux)
XY_coordinates = XY_coordinates.loc[~XY_coordinates.index.duplicated(keep='first')]

# Plot lines
for i_line in Lines_set: # Loop thought all lines
    i_bus=Line_data_DSS.loc[i_line,'Sending bus']
    j_bus=Line_data_DSS.loc[i_line,'Receiving bus']
    x=[XY_coordinates.loc[i_bus,'X'],XY_coordinates.loc[j_bus,'X']]
    y=[XY_coordinates.loc[i_bus,'Y'],XY_coordinates.loc[j_bus,'Y']]
    ax.plot(x, y, Feeder_colors, linestyle='-',linewidth=1)
    
# Plot Loads
for i_loads in Loads_set: # Loop thought all loads  
    x=XY_coordinates.loc[Load_bus.loc[i_loads,'Bus'],'X'] # loads node coord
    y=XY_coordinates.loc[Load_bus.loc[i_loads,'Bus'],'Y']
    ax.scatter(x, y, s=30 , c='k')
    
# Plot distribution transformer
x=XY_coordinates.loc['secondary','X'] # loads node coord
y=XY_coordinates.loc['secondary','Y']
ax.scatter(x, y, s=500 , c='r', marker='^')    
        
ax.set(ylabel='Y coord [km]', xlabel= 'X coord [km]')
plt.title('LV Network')  
plt.show()

#fig.savefig(r'Network_plot.svg') 