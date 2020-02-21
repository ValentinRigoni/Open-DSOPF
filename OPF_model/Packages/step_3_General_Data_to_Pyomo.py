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

def Sets_and_others(pd,Bus_set,Pyomo_data_path,Lines_set,Line_data_DSS,Loads_set,Load_phase,Load_bus,Load_Vnom):

    ## Retrieve necessary data
    Buses = Bus_set
    
    ## Phases set
    open(Pyomo_data_path + '/Phases_Pyomo.csv', 'w').close()
    with open(Pyomo_data_path + '/Phases_Pyomo.csv', 'a') as open_file:
        Headers= 'Phases_abc'
        open_file.write(Headers + '\n')
        for phase in ['1','2','3']:
            open_file.write(phase + '\n')
    
    ## Bus set
    open(Pyomo_data_path + '/Buses_Pyomo.csv', 'w').close()
    with open(Pyomo_data_path + '/Buses_Pyomo.csv', 'a') as open_file:
        Headers= 'Buses'
        open_file.write(Headers + '\n')
        for bus in Buses:
            open_file.write(bus + '\n')
                
    ## Lines data        
    # This needs to be modified if you include any new line in the system, e.g. MV line     
    Lines_set = pd.DataFrame(columns=['Lines'])     
    Lines_buses = pd.DataFrame(columns=['Lines','Lines_k','Lines_i','Lines_cable'])
    Lines_buses['Lines'] = Line_data_DSS.index
    Lines_buses[['Lines_k','Lines_i','Lines_cable']] = Line_data_DSS[['Sending bus','Receiving bus','Cable code']].values
    Lines_set['Lines'] = Line_data_DSS.index
    Lines_set.to_csv(Pyomo_data_path + '/Lines_Pyomo.csv',index=False)
    Lines_buses.to_csv(Pyomo_data_path + '/Lines_data_Pyomo.csv',index=False)    

    
    ## Loads data
    Loads_set = pd.DataFrame(columns=['Loads'])
    Loads_data = pd.DataFrame(columns=['Loads','Load_bus_conn','Load_phase_conn','Load_Vnom'])
    Loads_set['Loads'] = Load_bus.index
    Loads_data['Loads'] = Load_bus.index
    Loads_data['Load_bus_conn'] = Load_bus['Bus'].values
    Loads_data['Load_phase_conn'] = Load_phase['phase'].values
    Loads_data['Load_Vnom'] = Load_Vnom['Vnom [V]'].values   
    Loads_set.to_csv(Pyomo_data_path + '/Loads_Pyomo.csv',index=False)
    Loads_data.to_csv(Pyomo_data_path + '/Loads_data_Pyomo.csv',index=False)
    
    
    
        
        