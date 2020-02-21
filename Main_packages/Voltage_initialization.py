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


def Voltage_initialization(math,pd,np,Bus_set,Bus_set_no_slack,dssCircuit,DSSMon_Bus_Vmag,DSSMon_Bus_Vdeg):
    V_init_pu = pd.DataFrame(columns=['Bus_k','Phase_k','Vinit','Vinitre_pu','Vinitim_pu'])
    
    # Sort out the slack first
    Slack_kV = dssCircuit.Vsources.BasekV
    phase_slack = np.zeros([3,1])
    phase_slack[0] = dssCircuit.Vsources.AngleDeg
    phase_slack[1] = phase_slack[0] - 120
    phase_slack[2] = phase_slack[1] - 120
    
    for phase_k in [1,2,3]:
        bus_k = 'slack'
        Vinit = 1000*Slack_kV/math.sqrt(3)
        Vinitre_pu = math.cos(math.radians(phase_slack[phase_k-1]))
        Vinitim_pu = math.sin(math.radians(phase_slack[phase_k-1]))
        
        df = pd.DataFrame(np.array([[bus_k],[phase_k],[Vinit],[Vinitre_pu],[Vinitim_pu]]).T,columns=['Bus_k','Phase_k','Vinit','Vinitre_pu','Vinitim_pu'])
        V_init_pu=V_init_pu.append(df)

    # Remaining buses
    for i_bus in range(len(Bus_set_no_slack)):
        for phase_k in [1,2,3]:
            bus_k = Bus_set_no_slack[i_bus]
            Vinit = DSSMon_Bus_Vmag[i_bus,phase_k-1]
            angle = DSSMon_Bus_Vdeg[i_bus,phase_k-1]
            Vinitre_pu = math.cos(math.radians(angle))
            Vinitim_pu = math.sin(math.radians(angle))
            
            df = pd.DataFrame(np.array([[bus_k],[phase_k],[Vinit],[Vinitre_pu],[Vinitim_pu]]).T,columns=['Bus_k','Phase_k','Vinit','Vinitre_pu','Vinitim_pu'])
            V_init_pu=V_init_pu.append(df)
            
    V_init_pu.index = range(len(V_init_pu.index))
    return V_init_pu