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
    V. Rigoni and A. Keane, "An Open-Source Optimal Power Flow Formulation: Integrating Pyomo & OpenDSS in Python", 2020 IEEE Power and Energy Society General Meeting, 2020.
"""

def Validation_Plots(figure_size,font_size,plt,np,math,Main_Results_path,Time_sim,Feeder_names,Bus_set_no_slack,V_statutory_lim,OPF_Bus_Vmag,DSS_Bus_Vmag,Lines_set,Line_data_DSS,OPF_Imag_line,DSS_Imag_line,OPF_P_line,DSS_P_line,OPF_Q_line,DSS_Q_line,Cable_data,Feeder_bus_validation,Feeder_Lines_validation):
    
    plt.rcParams.update({'font.size': font_size})
    plt.rcParams["font.family"] = "Times New Roman"
    color_phases = ['r','b','m']
    
    ############### Voltage ###############
    Vnom=400/math.sqrt(3)
    for i_feeder in Feeder_names:
        bus_plot = Feeder_bus_validation[i_feeder]
        fig, ax = plt.subplots(1, figsize=figure_size)
        for phase in range(3):
            # OPF
            ax.plot(Time_sim/60.0,OPF_Bus_Vmag[np.where(Bus_set_no_slack == bus_plot)[0][0],phase-1,:]/Vnom,color_phases[phase],linestyle='solid',linewidth=4,alpha=0.5)
            # OpenDSS
            ax.plot(Time_sim/60.0,DSS_Bus_Vmag[np.where(Bus_set_no_slack == bus_plot)[0][0],phase-1,:]/Vnom,'k',linestyle='--',linewidth=2,alpha=1)
        #ax.legend(('OPF phase 1','DSS phase 1','OPF phase 2','DSS phase 2','OPF phase 3','DSS phase 3'),loc='best')
        ax.set(ylabel='Bus ' + bus_plot + ' voltage [pu]', xlabel= 'Time [h]')
        ax.set_xlim(0,24)
        plt.xticks(range(0,24+2,2),range(0,24+2,2))
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        plt.show()
        fig.savefig(Main_Results_path + '/Validation_Voltages_' + bus_plot + '.svg') 
    
    ############### Current ###############   
    for i_feeder in Feeder_names:
        line_plot = Feeder_Lines_validation[i_feeder]
        fig, ax = plt.subplots(1, figsize=figure_size)
        for phase in range(3):
            # OPF
            ax.plot(Time_sim/60.0,OPF_Imag_line[np.where(Lines_set == line_plot)[0][0],phase-1,:],color_phases[phase],linestyle='solid',linewidth=4,alpha=0.5)
            # OpenDSS
            ax.plot(Time_sim/60.0,DSS_Imag_line[np.where(Lines_set == line_plot)[0][0],phase-1,:],'k',linestyle='--',linewidth=2,alpha=1)
        #ax.legend(('OPF phase 1','DSS phase 1','OPF phase 2','DSS phase 2','OPF phase 3','DSS phase 3'),loc='best')
        ax.set(ylabel='Line ' + line_plot + ' current flow [A]', xlabel= 'Time [h]')
        ax.set_xlim(0,24)
        plt.xticks(range(0,24+2,2),range(0,24+2,2))
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        plt.show()
        fig.savefig(Main_Results_path + '/Validation_Currents_' + line_plot + '.svg') 
        
    ############### P flow ###############
    for i_feeder in Feeder_names:
        line_plot = Feeder_Lines_validation[i_feeder]
        fig, ax = plt.subplots(1, figsize=figure_size)
        for phase in range(3):
            # OPF
            ax.plot(Time_sim/60.0,OPF_P_line[np.where(Lines_set == line_plot)[0][0],phase-1,:],color_phases[phase],linestyle='solid',linewidth=4,alpha=0.5)
            # OpenDSS
            ax.plot(Time_sim/60.0,DSS_P_line[np.where(Lines_set == line_plot)[0][0],phase-1,:],'k',linestyle='--',linewidth=2,alpha=1)
        #ax.legend(('OPF phase 1','DSS phase 1','OPF phase 2','DSS phase 2','OPF phase 3','DSS phase 3'),loc='best')
        ax.set(ylabel='Line ' + line_plot + ' P flow [kW]', xlabel= 'Time [h]')
        ax.set_xlim(0,24)
        plt.xticks(range(0,24+2,2),range(0,24+2,2))
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        plt.show()
        fig.savefig(Main_Results_path + '/Validation_Pflow_' + line_plot + '.svg') 
    
    
    ############### Q flow ###############
    for i_feeder in Feeder_names:
        line_plot = Feeder_Lines_validation[i_feeder]
        fig, ax = plt.subplots(1, figsize=figure_size)
        for phase in range(3):
            # OPF
            ax.plot(Time_sim/60.0,OPF_Q_line[np.where(Lines_set == line_plot)[0][0],phase-1,:],color_phases[phase],linestyle='solid',linewidth=4,alpha=0.5)
            # OpenDSS
            ax.plot(Time_sim/60.0,DSS_Q_line[np.where(Lines_set == line_plot)[0][0],phase-1,:],'k',linestyle='--',linewidth=2,alpha=1)
        #ax.legend(('OPF phase 1','DSS phase 1','OPF phase 2','DSS phase 2','OPF phase 3','DSS phase 3'),loc='best')
        ax.set(ylabel='Line ' + line_plot + ' Q flow [kvar]', xlabel= 'Time [h]')
        ax.set_xlim(0,24)
        plt.xticks(range(0,24+2,2),range(0,24+2,2))
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        plt.show()
        fig.savefig(Main_Results_path + '/Validation_Qflow_' + line_plot + '.svg')
    
def Operation_Plots(figure_size,font_size,plt,np,math,Main_Results_path,Feeder_names,Time_sim,Bus_set_no_slack,V_statutory_lim,Bus_Vnom,OPF_Bus_Vmag,DSS_Bus_Vmag,Lines_set,Line_data_DSS,OPF_Imag_line,DSS_Imag_line,OPF_P_line,DSS_P_line,OPF_Q_line,DSS_Q_line,Cable_data,Transformer_rating,instance,PV_set,security_margin_current,security_margin_Transformer_S,min_Cosphi):
    
    
    plt.rcParams.update({'font.size': font_size})
    plt.rcParams["font.family"] = "Times New Roman"
    
    ############### All Voltages ###############    
    fig, ax = plt.subplots(1, figsize=figure_size)
    for i_bus in range(len(Bus_set_no_slack)):
        for phase in range(3):
            Vnom = Bus_Vnom.loc[Bus_set_no_slack[i_bus],'Vnom_pn']
            ax.plot(Time_sim/60.0,OPF_Bus_Vmag[i_bus,phase-1,:]/Vnom,linestyle='solid',linewidth=2)
    ax.axhline(V_statutory_lim[1],color='r',linestyle=':', lw=1) 
    #ax.set_ylim(0.95,1.11)
    ax.set_xlim(0,24)
    plt.xticks(range(0,24+2,2),range(0,24+2,2))
    ax.set(ylabel='All nodal voltages [pu]', xlabel= 'Time [h]')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.show()
    fig.savefig(Main_Results_path + '/OPF_Voltages.svg')

    ############### Current ###############    
    fig, ax = plt.subplots(1, figsize=figure_size)
    for i_line in range(len(Lines_set)):
        Ilimit= Cable_data.loc[Line_data_DSS.loc[Lines_set[i_line],'Cable code'],'Current rating [A]']*security_margin_current
        for phase in range(3):
            ax.plot(Time_sim/60.0,OPF_Imag_line[i_line,phase-1,:]/float(Ilimit),linestyle='solid',linewidth=2)          
    ax.axhline(1.0,color='r',linestyle=':', lw=1) 
    ax.set_ylim(0,1.05)
    ax.set_xlim(0,24)
    plt.xticks(range(0,24+2,2),range(0,24+2,2))
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set(ylabel='All lines current flows [pu]', xlabel= 'Time [h]')
    fig.savefig(Main_Results_path + '/OPF_Currents.svg')
    plt.show()
    
    ############### Transformer ###############   
    fig, ax = plt.subplots(1, figsize=figure_size)
    Lines = Line_data_DSS.loc[Line_data_DSS['Sending bus']=='secondary'].index
    S_3p_power = np.zeros([len(Time_sim)])
    for i_line in range(len(Lines)):
        for phase in range(3):
            #S_3p_power += (OPF_P_line[i_line,phase-1,:]**2+OPF_Q_line[i_line,phase-1,:]**2)**0.5    
            for i_t in range(len(Time_sim)):
                t = Time_sim[i_t]
                S_3p_power[i_t] = ((sum(sum((instance.P_flow_sending[l,s,t].expr()**2.0+instance.Q_flow_sending[l,s,t].expr()**2.0) for s in instance.Phases_abc) for l in instance.Lines if instance.Lines_k[l] == 'secondary'))**0.5)/1000.0
    ax.plot(Time_sim/60.0,S_3p_power/(Transformer_rating*security_margin_Transformer_S),linestyle='solid',linewidth=2)
    ax.axhline(1,color='r',linestyle=':', lw=1) 
    ax.set_ylim(0,1.05)
    ax.set_xlim(0,24)
    plt.xticks(range(0,24+2,2),range(0,24+2,2))
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set(ylabel='Transformer S power [pu]', xlabel= 'Time [h]')
    plt.show()
    fig.savefig(Main_Results_path + '/OPF_Transformer_S.svg')
    
    ############### Controllable variables ############### 
    P_control = np.zeros([len(PV_set),len(Time_sim)])
    Thanphi_control = np.zeros([len(PV_set),len(Time_sim)])
    for i_pv in range(len(PV_set)):
        for i_t in range(len(Time_sim)):
            P_control[i_pv,i_t] = instance.P_control[PV_set[i_pv],Time_sim[i_t]].value
            Thanphi_control[i_pv,i_t] = instance.Thanphi_control[PV_set[i_pv],Time_sim[i_t]].value
    
    ## P control
    fig, ax = plt.subplots(1, figsize=figure_size)
    for i_pv in range(len(PV_set)):
        ax.plot(Time_sim/60.0,P_control[i_pv,:],linestyle='solid',linewidth=2)
    ax.axhline(1,color='r',linestyle=':', lw=1)
    ax.set_ylim(0,1.05)   
    ax.set(ylabel='P control', xlabel= 'Time [h]')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.show()  
    fig.savefig(Main_Results_path + '/OPF_P_control.svg')
        
    ## Tanphi control
    fig, ax = plt.subplots(1, figsize=figure_size)
    for i_pv in range(len(PV_set)):
        ax.plot(Thanphi_control[i_pv,:],linestyle='solid',linewidth=2)
    ax.axhline(-math.tan(math.acos(min_Cosphi)),color='r',linestyle=':', lw=1)
    ax.axhline(math.tan(math.acos(min_Cosphi)),color='r',linestyle=':', lw=1)
    ax.set(ylabel='Tanphi control', xlabel= 'Time [h]')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.show()  
    fig.savefig(Main_Results_path + '/OPF_Thanphi_control.svg')
    
    ## P control boxplot
    fig, ax = plt.subplots(1, figsize=figure_size)
    
    P_control_99 = np.percentile(P_control,99,axis=0)
    P_control_median = np.percentile(P_control,50,axis=0)
    P_control_1 = np.percentile(P_control,1,axis=0) 
    ax.plot(Time_sim/60.0,P_control_99,'k',linestyle='--',linewidth=2)
    ax.plot(Time_sim/60.0,P_control_median,'k',linestyle='solid',linewidth=3)
    ax.plot(Time_sim/60.0,P_control_1,'k',linestyle=':',linewidth=2)
    ax.axhline(1,color='r',linestyle=':', lw=1)
    ax.set_ylim(0,1.05)  
    ax.set_xlim(0,24)
    plt.xticks(range(0,24+2,2),range(0,24+2,2))
    ax.set(ylabel='P control', xlabel= 'Time [h]')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.show()  
    fig.savefig(Main_Results_path + '/OPF_P_control_boxplot.svg')
    
    
    ## Tanphi control boxplot
    fig, ax = plt.subplots(1, figsize=figure_size)
    
    Thanphi_control_99 = np.percentile(Thanphi_control,99,axis=0)
    Thanphi_control_median = np.percentile(Thanphi_control,50,axis=0)
    Thanphi_control_1 = np.percentile(Thanphi_control,1,axis=0) 
    ax.plot(Time_sim/60.0,Thanphi_control_99,'k',linestyle='--',linewidth=2)
    ax.plot(Time_sim/60.0,Thanphi_control_median,'k',linestyle='solid',linewidth=3)
    ax.plot(Time_sim/60.0,Thanphi_control_1,'k',linestyle=':',linewidth=2)
    ax.axhline(-math.tan(math.acos(min_Cosphi)),color='r',linestyle=':', lw=1)
    ax.axhline(math.tan(math.acos(min_Cosphi)),color='r',linestyle=':', lw=1)
    ax.set(ylabel='Tanphi control', xlabel= 'Time [h]')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_ylim(-0.05,0.5)  
    ax.set_xlim(0,24)
    plt.xticks(range(0,24+2,2),range(0,24+2,2))
    plt.show()  
    fig.savefig(Main_Results_path + '/OPF_Thanphi_control_boxplot.svg')