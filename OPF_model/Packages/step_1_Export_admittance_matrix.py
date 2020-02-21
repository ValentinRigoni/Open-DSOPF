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
"""

def Get_addmittance_matrix(dssCircuit,dssText,OPF_model_path):
    dssSolution = dssCircuit.Solution
        
    dssSolution.Solve()
    
    dssText.Command = 'set datapath=' + OPF_model_path + '/AuxData'
    
    filename = "LV_Network_EXP_Y.CSV"
    # opening the file with w+ mode truncates the file
    f = open(filename, "w+")
    f.close()
    filename = "LV_Network_EXP_YPRIM.CSV"
    # opening the file with w+ mode truncates the file
    f = open(filename, "w+")
    f.close()

    dssText.Command = 'Export YPrims'
    dssText.Command = 'Export Y'

