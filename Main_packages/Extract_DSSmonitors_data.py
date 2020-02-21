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

def Extract_DSSmonitors_data(np,dssCircuit,dssMonitors,Bus_set_no_slack,Line_data_DSS,Lines_set):

    ## Monitor channels ##    
    # VI monitors
    # V1 deg1 V2 deg2 V3 deg3 I1 degI1 I2 degI2 I3 degI3
    # PQ monitors
    # P1 Q1 P2 Q2 P3 Q3 [kW & kvar]
    
    # Voltages
    DSSMon_Bus_Vmag = np.zeros([Bus_set_no_slack.size,3])
    DSSMon_Bus_Vdeg = np.zeros([Bus_set_no_slack.size,3])
    for i_bus in range(len(Bus_set_no_slack)): 
        if Bus_set_no_slack[i_bus]=='secondary':
            Line = Line_data_DSS.loc[Line_data_DSS['Sending bus']==Bus_set_no_slack[i_bus]].index.values[0]    
            dssMonitors.Name = Line + '_vi_sending'
        else:
            Line = Line_data_DSS.loc[Line_data_DSS['Receiving bus']==Bus_set_no_slack[i_bus]].index.values[0]   
            dssMonitors.Name = Line + '_vi_receiving'
        for phase in range(3):
            DSSMon_Bus_Vmag[i_bus,phase] = dssMonitors.Channel((phase)*2+1)[0]  
            DSSMon_Bus_Vdeg[i_bus,phase] = dssMonitors.Channel((phase)*2+2)[0]
            
    ## Flows from the monitors
    DSSMon_Imag_line = np.zeros([Lines_set.size,3])
    DSSMon_P_line = np.zeros([Lines_set.size,3])
    DSSMon_Q_line = np.zeros([Lines_set.size,3])
    
    for i_line in range(len(Lines_set)):
        # Current
        dssMonitors.Name = Lines_set[i_line] + '_vi_sending'
        for phase in range(3):
            DSSMon_Imag_line[i_line,phase] = dssMonitors.Channel((phase)*2+7)[0]
        # PQ flows
        dssMonitors.Name = Lines_set[i_line] + '_pq_sending'
        for phase in range(3):
            DSSMon_P_line[i_line,phase] = dssMonitors.Channel((phase)*2+1)[0]
            DSSMon_Q_line[i_line,phase] = dssMonitors.Channel((phase)*2+2)[0]
    
    return [DSSMon_Bus_Vmag,DSSMon_Bus_Vdeg,DSSMon_Imag_line,DSSMon_P_line,DSSMon_Q_line]