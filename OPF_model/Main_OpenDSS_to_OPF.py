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

### DESCRIPTION ###
"""
This script creates all the data required for the Pyomo OPF

"""

""" INPUTS """
Feeder_names= ['Feeder2'] # Create the model only for the feeders under interest - ['Feeder1','Feeder2','Feeder3']

def OpenDSS_to_OPF(os,np,pd,OPF_model_path,Pyomo_data_path,dssCircuit,dssText,Bus_set,Lines_set,Line_data_DSS,Loads_set,Load_phase,Load_bus,Load_Vnom):
    
    from OPF_model.Packages.step_1_Export_admittance_matrix import Get_addmittance_matrix
    from OPF_model.Packages.step_2_Y_Bus import Export_Y_bus
    from OPF_model.Packages.step_3_General_Data_to_Pyomo import Sets_and_others

    
    ## Get OPF model for Pyomo
    # 1 - Export admittance matrix calculated in OpenDSS
    Get_addmittance_matrix(dssCircuit,dssText,OPF_model_path)
    dssText.Command = 'set datapath=' + OPF_model_path

    # 2 - Export Y matrix in Pyomo format (indexed) and connectivity matrix
    Export_Y_bus(np,pd,OPF_model_path,Pyomo_data_path,Bus_set)
    dssText.Command = 'set datapath=' + OPF_model_path
    
    # 3 - Export: Loads, Phases, Line sets, bus sets, etc.
    Sets_and_others(pd,Bus_set,Pyomo_data_path,Lines_set,Line_data_DSS,Loads_set,Load_phase,Load_bus,Load_Vnom)
    dssText.Command = 'set datapath=' + OPF_model_path
       
    # Delete all Aux data
    if 1==1:
        os.remove(OPF_model_path + '/AuxData/LV_Network_EXP_Y.CSV')
        os.remove(OPF_model_path + '/AuxData/LV_Network_EXP_YPRIM.CSV')
        