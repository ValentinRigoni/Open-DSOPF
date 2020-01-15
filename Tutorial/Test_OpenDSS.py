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

Comments:
    - The solver does not use per unit values
    - Neutral is not explicitly modelled
    - Formulation uses the current injection method from: P. Garcia, J. Pereira, S. Carneiro Jr., V. M. da Costa and N. Martins, "Three-Phase Power Flow Calculations Using the Current Injection Method", IEEE Transactions on Power Systems, vol. 15, no. 2, 2000.
"""

""" Call modules """
# Import all the python and OpenDSS libraries needed for the script
import os
import win32com.client # To access the OpenDSS COM module
from win32com.client import makepy
import sys

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
dssText.Command = 'set datapath=' + os.path.dirname(os.path.realpath(__file__))
dssText.Command = 'Clear' # clear any existing circuit in the engine
dssText.Command ='Set DefaultBaseFrequency=50'

# Vsource
dssText.Command = 'New circuit.LV_Network bus1=slack BasekV=10 pu=1.00 Angle=0 phases=3 ISC3=99999999999 Isc1=99999999999' 

dssText.Command = 'set controlmode=static'
dssText.Command = 'set mode=snapshot'
dssSolution.Solve()
if dssSolution.Converged:
    print('Solution Converged - OpenDSS should be working fine')