Graph Pattern Mining using Logic Programming 
================
###by Sergey Paramonov, Matthijs van Leeuwen, Marc Denecker and Luc De Raedt

The code and the data presented here are supplementary material for the paper.


The structure of the repository is the following:

* **idp_datasets** contains all the dataset in IDP format, each dataset as a single file, these datasets are used for top-one experiment
* **decomposed_datasets** contains all the datasets but with a separate file for each graph, these datasets are used for decomposed model experiment
* **make\_decomposed\_experiment.sh** and **make\_top_one\_experiment.sh** start the experiments described in the paper by calling **decomposed\_single\_run.sh** and **top\_one\_single\_run.sh** appopriate number of times with the right parameters on all datasets.
* **logs** contain raw output of the programs including errors 
* **results** contain processed output of the computations
* **scripts** contain all auxiliary scripts for text-processing, visualization and IO
* **figure\_enumeration\_experiment.pdf** and **figure\_top\_one\_experiment.pdf** are visual summary of the computations
