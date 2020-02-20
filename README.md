![](/Logo.png)

## An unbalance three-phase OPF integrated with OpenDSS - version beta 0.1
### Valentin Rigoni and Andrew Keane 
### University College Dublin, Ireland 
### [Open-DSPF FORUM](https://groups.google.com/forum/#!forum/open-dsopf)


It has been widely demonstrated that active network management (ANM) strategies will be required to avoid the violation of network      operational limits in distribution networks with a rich presence of distributed energy resources (DERs). With the characteristics of     different ANM strategies been varied, e.g. centralized or decentralized, a platform where the benefits and drawbacks of multiple approaches can be easily quantified and benchmarked is required. This work introduces an open-source python-based package with a three-phase unbalanced OPF model (written in Pyomo) that is automatically created by extracting the data available from any network modelled in OpenDSS. The proposed platform provides the following benefits:

1.	Both OpenDSS and OPF models can be integrated into the same Python script, opening a wide range of simulation opportunities.
2.	It can facilitate the benchmark of decentralized solutions, implemented in OpenDSS, with OPF solutions.
3.	The OPF formulation is flexible and can include any DER model. The objective function and constraints can be modified to explore more decentralized formulations.
4.	With many publicly available OpenDSS distribution networks models, it can expedite the validation of ANM solutions under multiple network topologies.

A real British low voltage (LV) network with domestic-scale photovoltaics is used as a test case. 

## License:
This model is open source software and publicly available. It is published under GNU General Public License 3          (http://www.gnu.org/licenses/). The license guarantees you the freedoms to use, study, share (copy), and modify the software. It is a copyleft license, which means that you can distribute derived works only under the same license terms.

## Citation:
When using this model and any of the provided functions and modified network models, please cite our paper which describes them: 
##### V. Rigoni and A. Keane, "Open-DSOPF: an open-source optimal power flow formulation integrated with OpenDSS", 2020 IEEE Power and Energy Society General Meeting, Montreal, 2020, *Accepted Paper*

IEEE Copyright Notice. According to current IEEE regulation (see [here](https://www.ieee.org/publications/rights/index.html#sect1)) only accepted paper versions are being made available.
[RESEARCH GATE](https://www.researchgate.net/publication/339377517_Open-DSOPF_an_open-source_optimal_power_flow_formulation_integrated_with_OpenDSS)
    
## Prior to run:
Make sure that you have the Pyomo library in Python and have installed OpenDSS

Check TUTORIALS folder

MAIN_Unbalanced_OPF_RUN runs the main script

forum: https://groups.google.com/forum/#!forum/open-dsopf

### OpenDSS (from website)
The OpenDSS is a comprehensive electrical power system simulation tool primarly for electric utility power distribution systems. It supports nearly all frequency domain (sinusoidal steady‐state) analyses commonly performed on electric utility power distribution systems. In addition, it supports many new types of analyses that are designed to meet future needs related to smart grid, grid modernization, and renewable energy research. The OpenDSS tool has been used since 1997 in support of various research and consulting projects requiring distribution system analysis. Many of the features found in the program were originally intended to support the analysis of distributed generation interconnected to utility distribution systems and that continues to be a common use. Other features support analysis of such things as energy efficiency in power delivery and harmonic current flow. The OpenDSS is designed to be indefinitely expandable so that it can be easily modified to meet future needs.

### Pyomo (from Wikipedia)
Pyomo allows users to formulate optimization problems in Python in a manner that is similar to the notation commonly used in mathematical optimization. Pyomo supports an object-oriented style of formulating optimization models, which are defined with a variety of modeling components: sets, scalar and multidimensional parameters, decision variables, objectives, constraints, equations, disjunctions and more. Optimization models can be initialized with python data, and external data sources can be defined using spreadsheets, databases, various formats of text files. Pyomo supports both abstract models, which are defined without data, and concrete models, which are defined with data. In both cases, Pyomo allows for the separation of model and data.
Pyomo supports dozens of solvers, both open source and commercial, including many solvers supported by AMPL, PICO, CBC, CPLEX, IPOPT, Gurobi and GLPK. 
