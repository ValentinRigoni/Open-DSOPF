![](/Logo.png)

## An unbalance three-phase OPF integrated with OpenDSS - version beta 0.1
### Valentin Rigoni and Andrew Keane 
### University College Dublin, Ireland 
### [Open-DSPF FORUM](https://groups.google.com/forum/#!forum/open-dsopf)

####It has been widely demonstrated that active network management (ANM) strategies will be required to avoid the violation of network      operational limits in distribution networks with a rich presence of distributed energy resources (DERs). With the characteristics of     different ANM strategies been varied, e.g. centralized or decentralized, a platform where the benefits and drawbacks of multiple approaches can be easily quantified and benchmarked is required. This work introduces an open-source python-based package with a three-phase unbalanced OPF model (written in Pyomo) that is automatically created by extracting the data available from any network modelled in OpenDSS. The proposed platform provides the following benefits:

1.	Both OpenDSS and OPF models can be integrated into the same Python script, opening a wide range of simulation opportunities.
2.	It can facilitate the benchmark of decentralized solutions, implemented in OpenDSS, with OPF solutions.
3.	The OPF formulation is flexible and can include any DER model. The objective function and constraints can be modified to explore more decentralized formulations.
4.	With many publicly available OpenDSS distribution networks models, it can expedite the validation of ANM solutions under multiple network topologies.

A real British low voltage (LV) network with domestic-scale photovoltaics is used as a test case. 

## Paper citation:
When using this model and any of the provided functions and modified network models, please cite our paper which describes them: 
##### V. Rigoni and A. Keane, "Open-DSOPF: an open-source optimal power flow formulation integrated with OpenDSS", 2020 IEEE Power and Energy Society General Meeting, Montreal, 2020, *Accepted Paper*

IEEE Copyright Notice. According to current IEEE regulation (see [here](https://www.ieee.org/publications/rights/index.html#sect1)) only accepted paper versions are being made available: [RESEARCH GATE](https://www.researchgate.net/publication/339377517_Open-DSOPF_an_open-source_optimal_power_flow_formulation_integrated_with_OpenDSS)

## License:
This model is open source software and publicly available. It is published under [GNU General Public License 3](http://www.gnu.org/licenses/). The license guarantees you the freedoms to use, study, share (copy), and modify the software. It is a copyleft license, which means that you can distribute derived works only under the same license terms.
    
## Prior to run:
Make sure that you have the Pyomo library in Python and have installed OpenDSS

Check TUTORIALS folder

MAIN_Unbalanced_OPF_RUN runs the main script

forum: https://groups.google.com/forum/#!forum/open-dsopf

### [What is OpenDSS?](https://www.epri.com/#/pages/sa/opendss?lang=en)
### [What is Pyomo?](http://www.pyomo.org/about)
