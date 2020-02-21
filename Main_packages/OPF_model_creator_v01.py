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
    V. Rigoni and A. Keane, "Open-DSOPF: an open-source optimal power flow formulation integrated with OpenDSS", 2020 IEEE Power and Energy Society General Meeting, 2020.

Comments:
    - The solver does not use per unit values
    - Neutral is not explicitly modelled
    - Formulation uses the current injection method from: P. Garcia, J. Pereira, S. Carneiro Jr., V. M. da Costa and N. Martins, "Three-Phase Power Flow Calculations Using the Current Injection Method", IEEE Transactions on Power Systems, vol. 15, no. 2, 2000.
"""

def OPF_model_creator(pd,pyo,math,Time_sim,V_init_pu,House_Dem_data,PV_set,PV_Gen_data,Bus_Vnom,V_statutory_lim,min_Cosphi,Inverter_S_oversized,Cable_data,Transformer_rating,security_margin_current,security_margin_Transformer_S):
   
    model = pyo.AbstractModel() # Defines an abstract model which data can be imported

    ## Core sets definition ## 
    # Loaded from csv in OPF_model\Pyomo_OPF_data\
    model.Buses = pyo.Set(dimen=1)
    model.Phases_abc = pyo.Set(dimen=1)
    model.Lines = pyo.Set(dimen=1)
    model.Loads = pyo.Set(dimen=1)
    
    # Defined here
    model.time = pyo.Set(initialize=Time_sim)
    model.PVs = pyo.Set(initialize=PV_set)
        
    ## Parameters ##
    if 1==1:
        ## Loaded from csv in OPF_model\Pyomo_OPF_data\
        # Network parameters
        model.Bus_G = pyo.Param(model.Buses,model.Buses,model.Phases_abc,model.Phases_abc) # Network conductivity matrix
        model.Bus_B = pyo.Param(model.Buses,model.Buses,model.Phases_abc,model.Phases_abc) # Network susceptance matrix
        model.Connectivity = pyo.Param(model.Buses,model.Buses) # Connectivity matrix 1 if bus k and bus i are connected (zero otherwise)
        model.Lines_k= pyo.Param(model.Lines) # Lines sending buses
        model.Lines_i= pyo.Param(model.Lines) # Lines receiving buses
        model.Lines_cable= pyo.Param(model.Lines) # Lines cable data       
        
        # Load characteristics
        model.Load_bus_conn= pyo.Param(model.Loads)
        model.Load_phase_conn = pyo.Param(model.Loads)
        model.Load_Vnom = pyo.Param(model.Loads)

        ## From main script
        # Variables initialization values - V_init_pu
        # Network loads demand - House_Dem_data
        # Network PV PQ injections - PV_Gen_data        
     
    ## Variables ## 
    if 1==1:
        # PV Control variables
        if 1==1:
            model.P_control = pyo.Var(model.PVs, model.time, within=pyo.NonNegativeReals, bounds=(0.0,1.0), initialize=0.001)
            model.Thanphi_control = pyo.Var(model.PVs, model.time, bounds=(0.0,math.tan(math.acos(min_Cosphi))), initialize=0.001)
    
        # Voltages - Real and Imaginary part - in V
        if 1==1:
            # Initialization rules
            def init_Vre_rule(model, k, s, t):
                bus_check = V_init_pu['Bus_k']==k
                phase_check = V_init_pu['Phase_k']==str(s)
                return float(V_init_pu.loc[bus_check & phase_check,'Vinitre_pu'].values[0]) * float(V_init_pu.loc[bus_check & phase_check,'Vinit'].values[0])
            def init_Vim_rule(model, k, s, t):
                bus_check = V_init_pu['Bus_k']==k
                phase_check = V_init_pu['Phase_k']==str(s)
                return float(V_init_pu.loc[bus_check & phase_check,'Vinitim_pu'].values[0]) * float(V_init_pu.loc[bus_check & phase_check,'Vinit'].values[0])
            # Variables definition
            model.Vre = pyo.Var(model.Buses,model.Phases_abc,model.time, initialize=init_Vre_rule)  # Real and imaginary phase voltages
            model.Vim = pyo.Var(model.Buses,model.Phases_abc,model.time, initialize=init_Vim_rule) 
        # Auxiliary variables for power flow
        if 1==1:
            # Real and imaginary specified current injections for the current missmatch
            model.Isp_re = pyo.Var(model.Buses,model.Phases_abc,model.time, initialize=0.0)
            model.Isp_im = pyo.Var(model.Buses,model.Phases_abc,model.time, initialize=0.0)     
        # Dummy variables
        model.Dummy = pyo.Var(initialize=0.0, within=pyo.NonNegativeReals) # Dummy variable just to have something to put in the objective function
    
    ## Expressions ##
    if 1==1:     
        # Voltage magnitude
        def V_mag_2_rule(model, k, s, t):
            return model.Vre[k,s,t]**2+model.Vim[k,s,t]**2
        model.V_mag_2 = pyo.Expression(model.Buses, model.Phases_abc, model.time, rule=V_mag_2_rule)
        
        # PV generation - PVs are constant power here
        if 1==1:
            def PV_P_rule(model, pv, t):
                return PV_Gen_data[pv,'Profile'].loc[t] * model.P_control[pv,t]
            model.PV_P= pyo.Expression(model.PVs,model.time, rule=PV_P_rule) # Active power generation at each bus from PVs
            def PV_Q_rule(model, pv, t): 
                return model.PV_P[pv,t] * -model.Thanphi_control[pv,t]
            model.PV_Q= pyo.Expression(model.PVs,model.time, rule=PV_Q_rule) # Reactive power generation at each bus from PVs
            
        # Power injection per node
        if 1==1:
            # Active Power demand ZIP
            def ZIP_P_rule(model, k, s, t):
                return sum(House_Dem_data[h,'P_Profile'].loc[t] * (House_Dem_data[h,'ZIP_P'].loc[t,'P'] + House_Dem_data[h,'ZIP_P'].loc[t,'I'] * ((pyo.sqrt(model.V_mag_2[k,s,t]))/model.Load_Vnom[h]) + House_Dem_data[h,'ZIP_P'].loc[t,'Z'] * (model.V_mag_2[k,s,t])/(model.Load_Vnom[h]**2)) for h in model.Loads if (model.Load_bus_conn[h]==k and model.Load_phase_conn[h]==s))            
            model.PDem_ZIP = pyo.Expression(model.Buses,model.Phases_abc,model.time,  rule=ZIP_P_rule)
            # Reactive Power demand ZIP
            def ZIP_Q_rule(model, k, s, t):
                 return sum(House_Dem_data[h,'Q_Profile'].loc[t] * (House_Dem_data[h,'ZIP_Q'].loc[t,'P'] + House_Dem_data[h,'ZIP_Q'].loc[t,'I'] * ((pyo.sqrt(model.V_mag_2[k,s,t]))/model.Load_Vnom[h]) + House_Dem_data[h,'ZIP_Q'].loc[t,'Z'] * (model.V_mag_2[k,s,t])/(model.Load_Vnom[h]**2)) for h in model.Loads if (model.Load_bus_conn[h]==k and model.Load_phase_conn[h]==s)) 
            model.QDem_ZIP = pyo.Expression(model.Buses,model.Phases_abc,model.time,  rule=ZIP_Q_rule)
            # Active power generation
            def PGen_rule(model, k, s, t):
                return sum(model.PV_P[pv,t] for pv in model.PVs if (model.Load_bus_conn[pv]==k and model.Load_phase_conn[pv]==s))            
            model.PGen = pyo.Expression(model.Buses,model.Phases_abc,model.time,  rule=PGen_rule)
            def QGen_rule(model, k, s, t):
                return sum(model.PV_Q[pv,t] for pv in model.PVs if (model.Load_bus_conn[pv]==k and model.Load_phase_conn[pv]==s))            
            model.QGen = pyo.Expression(model.Buses,model.Phases_abc,model.time,  rule=QGen_rule)
            # Power injections per node (generation - demand)
            def Psp_rule(model, k, s, t):
                return model.PGen[k,s,t] - model.PDem_ZIP[k,s,t]
            model.Psp = pyo.Expression(model.Buses,model.Phases_abc,model.time, rule=Psp_rule)
            def Qsp_rule(model, k, s, t):
                return model.QGen[k,s,t] - model.QDem_ZIP[k,s,t]
            model.Qsp = pyo.Expression(model.Buses,model.Phases_abc,model.time, rule=Qsp_rule)
        # Current injections
        if 1==1:
            # Specified current injection (from specified PQ injections)
            if 1==1:
                # They are specified as a constraint to as to avoid more complex expressions (simpler to solve.. don't need to divide by the voltage)
                def I_sp_re_rule(model, k, s, t): # Real specified current injection per node and phase
                    return model.Psp[k,s,t] == model.Vre[k,s,t] * model.Isp_re[k,s,t] + model.Vim[k,s,t] * model.Isp_im[k,s,t]
                model.Isp_re_con = pyo.Constraint(model.Buses,model.Phases_abc,model.time, rule=I_sp_re_rule) 
                def I_sp_im_rule(model, k, s, t): # Imaginary specified current injection per node and phase
                    return model.Qsp[k,s,t] == model.Vim[k,s,t] * model.Isp_re[k,s,t] - model.Vre[k,s,t] * model.Isp_im[k,s,t]
                model.Isp_im_con = pyo.Constraint(model.Buses,model.Phases_abc,model.time, rule=I_sp_im_rule)
            # Calculated current injection (from voltages and admittances)
            if 1==1:
                # Expressions for currents
                def I_calc_re_rule(model, k, s, t): # Real calculated current injection   
                    return sum(sum( model.Bus_G[k,i,s,a]*model.Vre[i,a,t] - model.Bus_B[k,i,s,a]*model.Vim[i,a,t] for a in model.Phases_abc) for i in model.Buses if model.Connectivity[k,i] == 1)
                model.Icalc_re = pyo.Expression(model.Buses,model.Phases_abc,model.time, rule=I_calc_re_rule) 
                def I_calc_im_rule(model, k, s, t): # Imaginary calculated current injection   
                    return sum(sum( model.Bus_G[k,i,s,a]*model.Vim[i,a,t] + model.Bus_B[k,i,s,a]*model.Vre[i,a,t] for a in model.Phases_abc) for i in model.Buses if model.Connectivity[k,i] == 1)
                model.Icalc_im = pyo.Expression(model.Buses,model.Phases_abc,model.time, rule=I_calc_im_rule) 
        
        # Current line flows
        if 1==1:
            def I_flow_re_rule(model, l, s, t): # Real line flows
                return sum(model.Bus_G[model.Lines_k[l],model.Lines_i[l],s,a]*(model.Vre[model.Lines_i[l],a,t]-model.Vre[model.Lines_k[l],a,t]) - model.Bus_B[model.Lines_k[l],model.Lines_i[l],s,a]*(model.Vim[model.Lines_i[l],a,t]-model.Vim[model.Lines_k[l],a,t]) for a in model.Phases_abc)
            model.Iflow_re = pyo.Expression(model.Lines,model.Phases_abc,model.time, rule=I_flow_re_rule) 
            def I_flow_im_rule(model, l, s, t): # Imaginary line flows
                return sum(model.Bus_B[model.Lines_k[l],model.Lines_i[l],s,a]*(model.Vre[model.Lines_i[l],a,t]-model.Vre[model.Lines_k[l],a,t]) + model.Bus_G[model.Lines_k[l],model.Lines_i[l],s,a]*(model.Vim[model.Lines_i[l],a,t]-model.Vim[model.Lines_k[l],a,t]) for a in model.Phases_abc)
            model.Iflow_im = pyo.Expression(model.Lines,model.Phases_abc,model.time, rule=I_flow_im_rule) 
        # PQ line flows
        if 1==1:
            def P_flow_sending_rule(model, l, s, t): # P sending flow
                return model.Vre[model.Lines_k[l],s,t] * model.Iflow_re[l,s,t] + model.Vim[model.Lines_k[l],s,t] * model.Iflow_im[l,s,t]
            model.P_flow_sending = pyo.Expression(model.Lines,model.Phases_abc,model.time, rule=P_flow_sending_rule)    
            def P_flow_receiving_rule(model, l, s, t): # P receiving flow
                return -1.0 *(model.Vre[model.Lines_i[l],s,t] * model.Iflow_re[l,s,t] + model.Vim[model.Lines_i[l],s,t] * model.Iflow_im[l,s,t])  
            model.P_flow_receiving = pyo.Expression(model.Lines,model.Phases_abc,model.time, rule=P_flow_receiving_rule)
            def Q_flow_sending_rule(model, l, s, t): # Q sending flow
                return model.Vim[model.Lines_k[l],s,t] * model.Iflow_re[l,s,t] - model.Vre[model.Lines_k[l],s,t] * model.Iflow_im[l,s,t]
            model.Q_flow_sending = pyo.Expression(model.Lines,model.Phases_abc,model.time, rule=Q_flow_sending_rule)    
            def Q_flow_receiving_rule(model, l, s, t): # Q receiving flow
                return -1.0 *(model.Vim[model.Lines_i[l],s,t] * model.Iflow_re[l,s,t] - model.Vre[model.Lines_i[l],s,t] * model.Iflow_im[l,s,t])  
            model.Q_flow_receiving = pyo.Expression(model.Lines,model.Phases_abc,model.time, rule=Q_flow_receiving_rule)
        # Losses
        if 1==1:
            # Losses for this time step per line and phase
            def P_losses_rule(model, l, s, t): # Active power losses Watts!
                return model.P_flow_sending[l,s,t] + model.P_flow_receiving[l,s,t]
            model.P_losses = pyo.Expression(model.Lines,model.Phases_abc,model.time, rule=P_losses_rule)   
            # Total losses for this time step
            def P_losses_total_rule(model, s, t): # Total active power losses Watts!
                return sum(model.P_losses[l,s,t] for l in model.Lines)
            model.P_losses_total = pyo.Expression(model.Phases_abc,model.time, rule=P_losses_total_rule)
        
    ## Constraints ##
    # Power flow constraints - REQUIRED!
    if 1==1:
        # Current mismatch
        def I_delta_re_rule(model, k, s, t): # Real part
            if k=='slack':
                return pyo.Constraint.Skip
            else:
                return model.Isp_re[k,s,t] - model.Icalc_re[k,s,t] == 0.0
        model.Idelta_re_con = pyo.Constraint(model.Buses,model.Phases_abc,model.time, rule=I_delta_re_rule)
        def I_delta_im_rule(model, k, s, t): # Imaginary part
            if k=='slack':
                return pyo.Constraint.Skip
            else:
                return model.Isp_im[k,s,t] - model.Icalc_im[k,s,t] == 0.0
        model.Idelta_im_con = pyo.Constraint(model.Buses,model.Phases_abc,model.time, rule=I_delta_im_rule)
        # Slack constraint
        def Slack_re_rule(model, k, s, t): # Real part
            if k=='slack':
                bus_check = V_init_pu['Bus_k']==k
                phase_check = V_init_pu['Phase_k']==str(s)
                return model.Vre[k,s,t]==float(V_init_pu.loc[bus_check & phase_check,'Vinitre_pu'].values[0]) * float(V_init_pu.loc[bus_check & phase_check,'Vinit'].values[0])
            else:
                return pyo.Constraint.Skip
        def Slack_im_rule(model, k, s, t): # Imaginary part
            if k=='slack':
                bus_check = V_init_pu['Bus_k']==k
                phase_check = V_init_pu['Phase_k']==str(s)
                return model.Vim[k,s,t]==float(V_init_pu.loc[bus_check & phase_check,'Vinitim_pu'].values[0]) * float(V_init_pu.loc[bus_check & phase_check,'Vinit'].values[0])
            else:
                return pyo.Constraint.Skip
        model.Slack_re_con = pyo.Constraint(model.Buses,model.Phases_abc,model.time, rule=Slack_re_rule) # Real part
        model.Slack_im_con = pyo.Constraint(model.Buses,model.Phases_abc,model.time, rule=Slack_im_rule) # Imaginary part
    
    # Network operational constraints - TIP: Try always to test the OPF with no constraints and start adding them one at the time
    if 1==1: 
        # Votlage limits
        if 1==1:
            def V_limits_rule(model, k, s, t):
                if k=='slack':
                    return pyo.Constraint.Skip
                else:
                    V_nom = Bus_Vnom.loc[k,'Vnom_pn']
                    return ((V_nom*V_statutory_lim[0])**2,model.V_mag_2[k,s,t],(V_nom*V_statutory_lim[1])**2)
            model.V_limits_con = pyo.Constraint(model.Buses,model.Phases_abc,model.time, rule=V_limits_rule)
        # Current limits for cable sections
        if 1==1:
            def Line_I_limits_rule(model, l, s, t):
                return model.Iflow_re[l,s,t]**2+model.Iflow_im[l,s,t]**2 <= (security_margin_current * Cable_data.loc[model.Lines_cable[l],'Current rating [A]'])**2
            model.Line_I_limits_con = pyo.Constraint(model.Lines,model.Phases_abc,model.time, rule=Line_I_limits_rule)  
        # Transformer power limit
        if 1==1:
            def Transformer_limit_rule(model, t):
                return sum(sum((model.P_flow_sending[l,s,t]**2+model.Q_flow_sending[l,s,t]**2) for s in model.Phases_abc) for l in model.Lines if model.Lines_k[l] == 'secondary') <= (security_margin_Transformer_S*Transformer_rating*1000)**2
            model.Transformer_limit_con = pyo.Constraint(model.time, rule=Transformer_limit_rule)  
    
    # PV operational limits
    if 1==1: # I recommend using a different NLP solver than IPOPT if incorporating this constraint (e.g. knitro or modifiying IPOPT options) - otherwise, relax the constraint
        def PV_inverter_limit_rule(model, pv, t):
            max_P =  PV_Gen_data[pv,'Profile'].loc[t]
            max_S = (max_P**2+ (max_P*math.tan(math.acos(min_Cosphi)))**2)**0.5
            if  max_S > PV_Gen_data[pv,'Rating']*1000*Inverter_S_oversized: 
                return (model.PV_P[pv,t]**2 + model.PV_Q[pv,t]**2) <= (PV_Gen_data[pv,'Rating']*1000*Inverter_S_oversized)**2
            else:
                return pyo.Constraint.Skip   
        model.PV_inverter_limit_con = pyo.Constraint(model.PVs, model.time, rule=PV_inverter_limit_rule)         
        
    """ Objective function """
    # Dummy objective function
    if 1==0: # Dummy objective function just for testing errors (it's always one or another)
        model.obj = pyo.Objective(expr=model.Dummy)
    if 1==1:
        def Objective_rule(model):
            return  sum(sum((-1e3 * model.P_control[pv,t] + model.Thanphi_control[pv,t] ) for pv in model.PVs) for t in model.time)
        model.obj = pyo.Objective(rule=Objective_rule)

    return model # the problem is solved at the main script
