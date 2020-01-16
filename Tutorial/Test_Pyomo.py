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

""" INPUTS """
solver = 'ipopt' # knitroampl - ipopt - etc.

""" Call modules """
import pyomo.environ as pyo 

""" Create discrete model for testing """
# Create the model
model = pyo.ConcreteModel()

# Variables
model.x = pyo.Var(within=pyo.NonNegativeReals,bounds=(10,None),initialize=0.0) # 10<x<inf
model.y = pyo.Var(within=pyo.NonNegativeReals,initialize=0.0)

# Objective function
def obj_rule(model):                                        
    return  model.x + pyo.sin(model.y) # x + sin(y)
model.obj = pyo.Objective(rule=obj_rule)

print('Solving OPF model...')
optimizer = pyo.SolverFactory(solver)
Problem = optimizer.solve(model,tee=True)


print('x= ' + str(model.x.value))
print('y= ' + str(model.y.value))
print('Objective function= ' + str(model.obj.expr()))
