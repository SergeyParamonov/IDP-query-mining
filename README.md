Declarative Relational Query Mining
================
###by Sergey Paramonov, Matthijs van Leeuwen, Marc Denecker and Luc De Raedt


The code and the data presented here are supplementary material for the paper. 

For the questions related to this work please contact Sergey Paramonov by email: <sergey.paramonov@cs.kuleuven.be>

The structure of the repository is the following:

* **idp_datasets** contains all the dataset in IDP format, each dataset as a single file, these datasets are used for top-one experiment
* **decomposed_datasets** contains all the datasets but with a separate file for each graph, these datasets are used for decomposed model experiment
* **make\_decomposed\_experiment.sh** and **make\_top_one\_experiment.sh** start the experiments described in the paper by calling **decomposed\_single\_run.sh** and **top\_one\_single\_run.sh** appropriate number of times with the right parameters on all datasets.
* **logs** contain raw output of the programs including errors 
* **results** contain processed output of the computations
* **scripts** contain all auxiliary scripts for text-processing, visualization and IO
* **figure\_enumeration\_experiment.pdf** and **figure\_top\_one\_experiment.pdf** are visual summary of the computations
* **base\_top\_one.idp** is the core of the theory in top-one experiment, **isomorphism_breaker.idp** was not used in this experiment but potentially can be used to exclude isomorphic graphs top-k mining task
* **candidate\_generation.idp** is the theory to generate a candidate subgraph from the template in decomposed model experiment, **homo_check** is the homomorphism check theory in the decomposed model experiment, **isomorphism.idp** is the theory for finding isomorphic subgraphs in the template itself

To process the raw output, call **python scripts/logs\_parser.py**, to visualize the output use R-scripts **visualize\_enumeration.R** and **visualize\_top.R**

The experiments were done in the environment specified below. It has not been tested on any other operation systems and in any other environment.
## Software
* Ubuntu 14.04 64 bit.  
* IDP 3.2.1
* python 2.7.6
* bash 4.3.11
* R 3.1.1 (only for visualization)
