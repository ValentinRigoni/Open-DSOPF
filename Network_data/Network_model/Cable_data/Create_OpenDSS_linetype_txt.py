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
    V. Rigoni and A. Keane, "A publicly available unbalanced optimal power flow: integrating Pyomo-OpenDSS in Python", 2020 IEEE Power and Energy Society General Meeting, 2020.
"""

"""
DESCRIPTION
This script creates the OpenDSS commands for creating the different line types using the Cable_data.xlsx file
"""

import pandas as pd # High level data manipulation

Cable_data = pd.read_excel('Cable_data.xlsx',index_col=0) # XY coordiantes

open('OpenDSS_line_types.txt', 'w').close()
for i_linetype in Cable_data.index:
    string = 'New LineCode.' + i_linetype.lower() + ' nphases=3 R1=' + str(Cable_data.loc[i_linetype,'R1 [ohms]']) + ' X1=' + str(Cable_data.loc[i_linetype,'X1 [ohms]']) + ' R0=' + str(Cable_data.loc[i_linetype,'R0 [ohms]']) + ' X0=' + str(Cable_data.loc[i_linetype,'X0 [ohms]']) + ' C1=' + str(Cable_data.loc[i_linetype,'C1 [uF]']) + ' C0=' + str(Cable_data.loc[i_linetype,'C0 [uF]']) + ' Units=km'       
    with open('OpenDSS_line_types.txt', 'a') as open_file:
        open_file.write(string + '\n')

