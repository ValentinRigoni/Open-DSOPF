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

def Export_Y_bus(np,pd,OPF_model_path,Pyomo_data_path,Bus_set):
    
    # Read Ybus data exported from OpenDSS - NOTE: values are in ohms (not un pu)
    Buses = Bus_set
    Y_matrix = pd.read_csv(OPF_model_path + '/AuxData/LV_Network_EXP_Y.CSV',header=None,skiprows=[0],index_col=0).values
    Y_matrix=Y_matrix[:len(Buses)*3,:len(Buses)*3*2] 
    
    ## G matrix
    G_matrix = np.zeros([Y_matrix.shape[0],int(Y_matrix.shape[1]/2)])
    col_count=0
    for i in range(0,Y_matrix.shape[1],2):
        col = Y_matrix[:,i]
        G_matrix[:,col_count]= col
        col_count+=1
    ## B matrix
    B_matrix = np.zeros([Y_matrix.shape[0],int(Y_matrix.shape[1]/2)]) # Need to transform text into number
    col_count=0
    for i in range(1,Y_matrix.shape[1],2):
        for j in range(0,Y_matrix.shape[0],1):
            B_matrix[j,col_count] = float(Y_matrix[j,i][4:])
        col_count+=1
      
    ## Create Y matrix for Pyomo     
    open(Pyomo_data_path + '/Y_bus_Pyomo.csv', 'w').close()
    with open(Pyomo_data_path + '/Y_bus_Pyomo.csv', 'a') as open_file:
        Headers= 'Bus_k,Bus_j,Phase_k,Phase_j,Bus_G,Bus_B'
        open_file.write(Headers + '\n')
        row_count=0
        for bus_k in Buses:
            for phase_k in ['1','2','3']:
                col_count=0
                for bus_j in Buses:
                    for phase_j in ['1','2','3']:
                        row_data_text = bus_k + ',' + bus_j + ',' + phase_k + ',' + phase_j + ',' + str(G_matrix[row_count,col_count]) + ',' + str(B_matrix[row_count,col_count])
                        open_file.write(row_data_text + '\n')
                        col_count+=1
                row_count+=1
                
    ## Create and export connectivity matrix
    open(Pyomo_data_path + '/Connectivity_Pyomo.csv', 'w').close()
    with open(Pyomo_data_path + '/Connectivity_Pyomo.csv', 'a') as open_file:
        Headers= 'Bus_k,Bus_j,Connectivity'
        open_file.write(Headers + '\n')
        row_count=0
        for i_bus_k in range(len(Buses)):
            for i_bus_j in range(len(Buses)):
                connected=0
                for phase_k in range(3):
                    for phase_j in range(3):
                        row=(i_bus_k*3)+phase_k
                        col=(i_bus_j*3)+phase_j
                        if G_matrix[row,col]!=0 or B_matrix[row,col]!=0:
                            connected=1
                row_data_text = Buses[i_bus_k] + ',' + Buses[i_bus_j] + ',' + str(connected)
                open_file.write(row_data_text + '\n')
    
    
    
    
    
    
    