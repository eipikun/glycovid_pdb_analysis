# Program of analyzing difference between PDBe and PDBj
## Analysis Steps
### Step 0(optional)
You are required to install those module to execute analysis.py in advance.
- beautifulsoup4==4.10.0
- certifi==2021.5.30
- charset-normalizer==2.0.6
- idna==3.2
- numpy==1.21.2
- pandas==1.3.3
- python-dateutil==2.8.2
- pytz==2021.1
- requests==2.26.0
- six==1.16.0
- soupsieve==2.2.1
- urllib3==1.26.7

version information is stored in requirements.txt
to make virtual enviroment with those module above, please execute the commands below.
```
python3 -m venv venv
```
```
. venv/bin/activate
```
```
pip3 install -r requirements.txt
```

### Step 1
- Visit PDBe COVID-19 featured protein list [page](https://www.ebi.ac.uk/pdbe/covid-19)
- Visit each protein page, and scroll to 'Structures and Domains' section
- Select 'CSV' format to download data

※Collections of csv file should be stored in 'data' folder without changing its name
### Step 2
- To scarape PDBj registered structures, uncomment line 124 of analysis.py
- You would be able to find ```pdbj_registered_covid19_structures.csv``` at top directory

### Step 3
- To get a list of COVID19 related structures registered in PDBe, uncomment line 125 of analysis.py
- You would be able to find ```pdbe_registered_covid19_structures.csv``` at top directory

### Step 4
- Confirm there are both ```pdbe_registered_covid19_structures.csv``` and ```pdbj_registered_covid19_structures.csv``` at top directory
- To analyze structure inclusion between PDBj and PDBe, uncomment line 126 of analysis.py
- You would be able to find ```pdbj_pdbe_relation.csv```

### Step5 (optional)
- To see the statics of ```pdbj_pdbe_relation.csv```, uncomment line 127 of analysis.py
