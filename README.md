# mdt_dcs_offline

## First Time Run
When running for the first time
```
python -m virtualenv myvenv
```
Once a virtual environment is created, some libraries may need to be downloaded before running.  
## Run 
First, to setup spark and the virtual environment: 
```
source setup.sh
```
### DCS Offload (Spark)
In order for analysis to be completed on a specific run, dcs data must be offloaded. The arguments required for this are a current run and the previous run. The dcs data from the current run will be offloaded, but some data is needed from the previous run. 

To offload dcs data for a single run:
```
python ./analysis/src/spark/runOffload.py -r 451295 -p 451140
```
To offload a group of runs, specify a year and a starting run:
```
python ./analysis/src/spark/runOffload_all.py -y 2022 -r 430702
```
### Python analysis
To generate the plots and figures needed for the webpage, the dcs offloaded data, a current run, and the previous run are needed.
To generate the graphics from a specific run:
```
python ./analysis/src/python_analysis/runAnalysis.py -r 451295 -p 451140
```
To generate graphics a group of runs, specify a year and a starting run:
```
python ./analysis/src/python_analysis/runAnalysis_all.py -y 2022 -r 430702
```
### Web 
To generate the web server with Flask:
```
python ./web/app.py
```


