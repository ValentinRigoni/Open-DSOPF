"""
#### OPF for unbalance three-phase network from OpenDSS ####
#### Valentin Rigoni and Andrew Keane ######################
#### University College Dublin, Ireland ####################

Contributions:
    This model available for anyone to use.
    If you use the model, get in touch and let us know about your work.

Citation:
    When using this model and any of the provided functions and modified network models, please cite our paper which describes them: 
    V. Rigoni and A. Keane, "Open-DSOPF: an open-source optimal power flow formulation integrated with OpenDSS", 2020 IEEE Power & Energy Society General Meeting, 2020.

Comments:
    - The solver does not use per unit values
    - Neutral is not explicitly modelled
    
Prior to run:
    - Make sure that you have pyomo library in Python and have installed OpenDSS
    - Check TUTORIALS folder
"""

""" INPUTS """
# Study feeders - Including all feeders will simulate the complete LV Network - IMPORTANT: this must match the model in 'OPF_model' folder
Feeder_names = ['Feeder2'] # ['Feeder1','Feeder2','Feeder3'] - can use all three or 1 or 2
voltagebases = [10,0.4] # in kV line to line

# Simulation time
Time_sim_interval = 60 # [5-1440] - Provided profiles have a 5 min resolution
Time_start = 60         # First time step >=5
Time_end = 1440      # Last time step <=1440

# Voltage limits in pu
V_statutory_lim = [0.9,1.1]

# Thermal limits
security_margin_current= 0.9 # ratio: limit/rating
security_margin_Transformer_S= 0.9

# PV characteristics
PV_penetration = 1 # [0-1] number_of_customers/customers_with_PV 
min_Cosphi = 0.95 # minimum power factor - either lagging or leading
Inverter_S_oversized = 1.1 # Inverter rating compared to PV kW rating (e.g. 1.1 means a +10%)

# Buses and lines to plot
Feeder_bus_validation = {'Feeder1':'feeder1_3155',
                         'Feeder2':'feeder2_1818',
                         'Feeder3':'feeder3_1377'}   
Feeder_Lines_validation = {'Feeder1':'feeder1_line1',
                           'Feeder2':'feeder2_line1',
                           'Feeder3':'feeder3_line1'}         
# Plots
show_plots = 'y' # - 'y' or 'n'  

""" Call modules """
# Import all the python and OpenDSS libraries needed for the script
import os
import pandas as pd # High level data manipulation
import numpy as np 
import win32com.client # To access the OpenDSS COM module
from win32com.client import makepy
import sys
import random
import math
import matplotlib.pyplot as plt
import pyomo.environ as pyo 
# Packages
from Main_packages.Extract_OpenDSS_data import Extract_data_OpenDSS  
from Main_packages.Plots import Validation_Plots,Operation_Plots
from Main_packages.Voltage_initialization import Voltage_initialization
from Main_packages.Extract_DSSmonitors_data import Extract_DSSmonitors_data
from OPF_model.Main_OpenDSS_to_OPF import OpenDSS_to_OPF
from Main_packages.OPF_model_creator_v01 import OPF_model_creator


""" FOLDERS """
# Get directory path
Main_path = os.path.dirname(os.path.realpath(__file__))
Network_model_path = Main_path + '/Network_data/Network_model'
Profiles_path = Main_path + '/Network_data/Profiles'
OPF_model_path = Main_path + '/OPF_model'
Pyomo_data_path = OPF_model_path + '/Pyomo_OPF_data'
Main_Results_path = Main_path + '/Main_Results'

""" Aux functions """
def range1(start, end, step): # like range but inlcuding the ending value
    return range(start, end+1, step)

"""################ SCRIPT ##################"""
# Create time set
Time_sim = np.array(range1(Time_start,Time_end,Time_sim_interval)) # Time set for simulations

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
if len(voltagebases)==1:   
    dssText.Command ='set voltagebases=[' +str(voltagebases[0])+ ']' # IMPORTANT - to definde nominal voltages
elif len(voltagebases)==2:  
    dssText.Command ='set voltagebases=[' +str(voltagebases[0])+ ',' + str(voltagebases[1]) +']'
elif len(voltagebases)==3:  
    dssText.Command ='set voltagebases=[' +str(voltagebases[0])+ ',' + str(voltagebases[1]) + ',' + str(voltagebases[2]) +']'  
else:
    raise ValueError('Too many voltage levels, modifiy this and ensure that OpenDSS properly capture voltage bases')
    
dssText.Command = 'CalcVoltageBase'
dssText.Command = 'set controlmode=static'
dssText.Command = 'set mode=snapshot'
dssSolution.Solve()
if dssSolution.Converged:
    print('Solution Converged')
else:
    raise ValueError('Solution did not Converge')
dssMonitors=dssCircuit.Monitors

# Data sets are available in the csv files in 'Network model'. However, it can also be extracted from OpenDSS - be carefull with naming, OpenDSS only works with all lower case
[Lines_set,Line_data_DSS,Bus_set,Bus_Vnom,Nodes_set,Loads_set,Load_phase,Load_bus,Load_Vnom,Transformer_rating] = Extract_data_OpenDSS(math,np,pd,dssCircuit)
Bus_set_no_slack = np.delete(Bus_set, np.where(Bus_set == 'slack')[0][0])

# Cable type data
Cable_data = pd.read_excel(Main_path + '/Network_data/Network_model/Cable_data/Cable_data.xlsx',index_col=0 )
Cable_data.index = Cable_data.index.str.lower()

"""
CREATE THE DATA FOR THE OPF
"""
OpenDSS_to_OPF(os,np,pd,OPF_model_path,Pyomo_data_path,dssCircuit,dssText,Bus_set,Lines_set,Line_data_DSS,Loads_set,Load_phase,Load_bus,Load_Vnom)

""" 
PARAMETERS FOR VOLTAGE INITIALIZATION
"""
dssText.Command ='Reset Monitors'
dssSolution.Solve()
dssMonitors.SampleAll() 
dssMonitors.SaveAll()
[DSSMon_Bus_Vmag,DSSMon_Bus_Vdeg,DSSMon_Imag_line,DSSMon_P_line,DSSMon_Q_line] = Extract_DSSmonitors_data(np,dssCircuit,dssMonitors,Bus_set_no_slack,Line_data_DSS,Lines_set)


## Initialization for voltages in OPF
V_init_pu = Voltage_initialization(math,pd,np,Bus_set,Bus_set_no_slack,dssCircuit,DSSMon_Bus_Vmag,DSSMon_Bus_Vdeg)

""" 
DEMAND AND PV ALLOCATION PROFILES
As written, the script randomly allocates demand and PV active power profiles to the network using the profiles provided in Network_data/Profiles
"""
## Demand
np.random.seed(0) # for repeatability
House_Dem_data = {} # defined as dictionary
h_profiles = np.random.randint(1,100,size=Loads_set.size) # define which random profiles will be allocated to each customer
for i_house in range(Loads_set.size): 
    csv_data = pd.read_csv(Profiles_path + '/Load_profiles/Profile_' +str(h_profiles[i_house])+ '_PZIP_QZIP.csv',index_col =0)    
    House_Dem_data[Loads_set[i_house],'P_Profile']= csv_data['P'] # Active power profile [W]
    House_Dem_data[Loads_set[i_house],'Q_Profile']= csv_data['Q'] # Reactive power profile [var] - here, assumed a PF of
    House_Dem_data[Loads_set[i_house],'ZIP_P'] = csv_data[['P_Z','P_I','P_P']]
    House_Dem_data[Loads_set[i_house],'ZIP_Q'] = csv_data[['Q_Z','Q_I','Q_P']]    
    House_Dem_data[Loads_set[i_house],'ZIP_P'].columns = ['Z','I','P']
    House_Dem_data[Loads_set[i_house],'ZIP_Q'].columns = ['Z','I','P']
    
## PV generation
np.random.seed(1) # for repeatability
random.seed(1)
PV_Gen_data = {} # defined as dictionary
PV_set = np.array(random.sample(list(Loads_set), int(np.rint(len(Loads_set) * PV_penetration))))
PV_profiles = np.random.randint(1,100,size=PV_set.size) 
PV_profiles_data = pd.read_excel(Profiles_path + '/PV_profiles/Summer_PV_Profiles.xlsx',header=0,index_col=0) # load all profiles - data in kW
PV_rating_data = pd.read_csv(Profiles_path + '/PV_profiles/PV_rating.csv')
for i_PV in range(PV_set.size): 
    PV_Gen_data[PV_set[i_PV],'Profile']=PV_profiles_data[PV_profiles[i_PV]]*1000 # Active power output for this PV [W]
    PV_Gen_data[PV_set[i_PV],'Rating']=PV_rating_data.loc[PV_profiles[i_PV],'Rating [kW]'] # PV rating in kW

""" 
UNBALANCED 3p OPTIMAL POWER FLOW MODEL
"""
# Create abstract OPF model
OPF_model = OPF_model_creator(pd,pyo,math,Time_sim,V_init_pu,House_Dem_data,PV_set,PV_Gen_data,Bus_Vnom,V_statutory_lim,min_Cosphi,Inverter_S_oversized,Cable_data,Transformer_rating,security_margin_current,security_margin_Transformer_S)

# Create instance with model in OPF_model\Pyomo_OPF_data\
os.chdir(Pyomo_data_path)
print('Initializing OPF model...')
instance = OPF_model.create_instance(Pyomo_data_path + '/Model_data.dat')
os.chdir(Main_path)

#### Choose a NLP solver  - make sure its installed - some solvers won't be able to find a feasible or optimal solution - NOTE: with IPOPT as default, I've disabled "PV operational limits" constraint... you need another solver when including that
# IPOPT
#optimizer = pyo.SolverFactory('ipopt') 
#optimizer.options["max_iter"] = 100000
#optimizer.options["linear_solver"] = 'mumps'

# KNITRO
optimizer = pyo.SolverFactory('knitroampl')
optimizer.options["par_numthreads"] = 1
optimizer.options["algorithm"] = 0 # Indicates which algorithm to use to solve the problem - 0 is auto [0-5]
optimizer.options["presolve"] = 1 # Determine whether or not to use the Knitro presolver to try to simplify the model by removing variables or constraints.

print('Solving OPF model...')
Problem = optimizer.solve(instance,tee=True)

"""
RETRIEVE VALUES FROM OPF
"""
print('Extracting data')
OPF_Bus_Vmag=np.zeros([Bus_set_no_slack.size,3,Time_sim.size])
OPF_P_line=np.zeros([Lines_set.size,3,Time_sim.size]) # Sending values
OPF_Q_line=np.zeros([Lines_set.size,3,Time_sim.size])
OPF_Ire_line=np.zeros([Lines_set.size,3,Time_sim.size])
OPF_Iim_line=np.zeros([Lines_set.size,3,Time_sim.size])
OPF_Imag_line=np.zeros([Lines_set.size,3,Time_sim.size])
OPF_Losses_line=np.zeros([Lines_set.size,3,Time_sim.size])
OPF_Losses_sign_line=np.zeros([Lines_set.size,3,Time_sim.size])
OPF_PV_P=np.zeros([PV_set.size,Time_sim.size])
OPF_PV_Q=np.zeros([PV_set.size,Time_sim.size])

# To get sets: e.g. instance.PVs.value_list 

count_t=0
for t in Time_sim:
    # Nodal voltages
    for i_bus in range(len(Bus_set_no_slack)):
        for phase in range(3):
            OPF_Bus_Vmag[i_bus,phase,count_t] = math.sqrt(instance.Vre[Bus_set_no_slack[i_bus],phase+1,t].value**2 + instance.Vim[Bus_set_no_slack[i_bus],phase+1,t].value**2)
    # Other variables
    for i_line in range(len(Lines_set)):
        for phase in range(3):
            OPF_P_line[i_line,phase,count_t] = instance.P_flow_sending[Lines_set[i_line],phase+1,t].expr()/1000.0 # kW
            OPF_Q_line[i_line,phase,count_t] = instance.Q_flow_sending[Lines_set[i_line],phase+1,t].expr()/1000.0
            OPF_Ire_line[i_line,phase,count_t] = instance.Iflow_re[Lines_set[i_line],phase+1,t].expr()
            OPF_Iim_line[i_line,phase,count_t] = instance.Iflow_im[Lines_set[i_line],phase+1,t].expr()
            OPF_Imag_line[i_line,phase,count_t] = math.sqrt(OPF_Ire_line[i_line,phase,count_t]**2+OPF_Iim_line[i_line,phase,count_t]**2)
            OPF_Losses_sign_line[i_line,phase,count_t] = instance.P_losses[Lines_set[i_line],phase+1,t].expr()/1000.0
            OPF_Losses_line[i_line,phase,count_t] = np.absolute(instance.P_losses[Lines_set[i_line],phase+1,t].expr()/1000.0)
    # PV outputs
    for i_pv in range(len(PV_set)):
        OPF_PV_P[i_pv,count_t] = instance.PV_P[PV_set[i_pv],t].expr()
        OPF_PV_Q[i_pv,count_t] = instance.PV_Q[PV_set[i_pv],t].expr()
    count_t+=1

"""
OPENDSS VALIDATION

This would represent operating the network with the solutions from the OPF
Another application is for benchmarking the OPF solution with a strategy implemented in OpenDSS
"""
DSS_Bus_Vmag=np.zeros([Bus_set_no_slack.size,3,Time_sim.size])
DSS_Imag_line=np.zeros([Lines_set.size,3,Time_sim.size])
DSS_P_line=np.zeros([Lines_set.size,3,Time_sim.size])
DSS_Q_line=np.zeros([Lines_set.size,3,Time_sim.size])


### Create PVs in OpenDSS
for PV in PV_set:
    dssText.Command = 'New Load.PV_' + PV + ' Phases=1 Bus1=' + Load_bus.loc[PV,'Bus'] + '.' + str(Load_phase.loc[PV,'phase']) + ' kV=' + str(0.4/math.sqrt(3)) + ' kW=0 Kvar=0 Model=1 Vminpu=0.7 Vmaxpu=1.3'

count_t=-1
for t in Time_sim:
    count_t+=1

    # OpenDSS LV feeder House demand
    for i_house in Loads_set:
        dssCircuit.Loads.Name = i_house
        dssCircuit.Loads.kW = House_Dem_data[i_house,'P_Profile'].loc[t]/1000.0
        dssCircuit.Loads.kvar = House_Dem_data[i_house,'Q_Profile'].loc[t]/1000.0       
        Z_p = float(House_Dem_data[i_house,'ZIP_P'].loc[t,'Z'])
        I_p = float(House_Dem_data[i_house,'ZIP_P'].loc[t,'I'])
        Z_q = float(House_Dem_data[i_house,'ZIP_Q'].loc[t,'Z'])
        I_q = float(House_Dem_data[i_house,'ZIP_Q'].loc[t,'I'])
        dssCircuit.Loads.ZIPV = (Z_p,I_p,1-Z_p-I_p,Z_q,I_q,1-Z_q-I_q,0.8) # Last coefficient: voltage in pu from wich the load model changes to constant impedance to facilitate convergency of OpenDSS

    # OpenDSS PVs
    for PV in PV_set:
        dssCircuit.Loads.Name = 'PV_' + PV
        dssCircuit.Loads.kW = -1 * instance.PV_P[PV,t].expr()/1000.0
        dssCircuit.Loads.kvar = -1 * instance.PV_Q[PV,t].expr()/1000.0
    
    ### Solve and get the new measurements ###    
    dssText.Command ='Reset Monitors'
    dssSolution.Solve()
    if not(dssSolution.Converged):
        raise ValueError('Solution did not Converge')
    dssMonitors.SampleAll() 
    dssMonitors.SaveAll()
    # Extract monitors data
    [DSSMon_Bus_Vmag,DSSMon_Bus_Vdeg,DSSMon_Imag_line,DSSMon_P_line,DSSMon_Q_line] = Extract_DSSmonitors_data(np,dssCircuit,dssMonitors,Bus_set_no_slack,Line_data_DSS,Lines_set)
    # Voltages
    DSS_Bus_Vmag[:,:,count_t] = DSSMon_Bus_Vmag       
    ## Flows from the monitors
    DSS_Imag_line[:,:,count_t] = DSSMon_Imag_line
    DSS_P_line[:,:,count_t] = DSSMon_P_line
    DSS_Q_line[:,:,count_t] = DSSMon_Q_line
        
"""
PLOT RESULTS - Validation of OPF model against OpenDSS results
"""
filelist = [ f for f in os.listdir(Main_Results_path)]
for f in filelist:
    os.remove(os.path.join(Main_Results_path, f))
        
if show_plots=='y':
    # Plot and save
    figure_size = (17, 5.7)
    font_size = 25
    Validation_Plots(figure_size,font_size,plt,np,math,Main_Results_path,Time_sim,Feeder_names,Bus_set_no_slack,V_statutory_lim,OPF_Bus_Vmag,DSS_Bus_Vmag,Lines_set,Line_data_DSS,OPF_Imag_line,DSS_Imag_line,OPF_P_line,DSS_P_line,OPF_Q_line,DSS_Q_line,Cable_data,Feeder_bus_validation,Feeder_Lines_validation)
    Operation_Plots(figure_size,font_size,plt,np,math,Main_Results_path,Feeder_names,Time_sim,Bus_set_no_slack,V_statutory_lim,Bus_Vnom,OPF_Bus_Vmag,DSS_Bus_Vmag,Lines_set,Line_data_DSS,OPF_Imag_line,DSS_Imag_line,OPF_P_line,DSS_P_line,OPF_Q_line,DSS_Q_line,Cable_data,Transformer_rating,instance,PV_set,security_margin_current,security_margin_Transformer_S,min_Cosphi)
