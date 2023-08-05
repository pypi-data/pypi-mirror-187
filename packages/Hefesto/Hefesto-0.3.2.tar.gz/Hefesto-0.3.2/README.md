# Hefesto

**Preprocessing datatable toolkit for CDE semantic model data source requirements**


## Install:
```bash
pip install Hefesto
```


## Usage:
**Requirements:**

- YAML configuration file to define which CDE do you want to execute and which columns contains the information
- CSV datatable with your CDE data

**Exemplar config file:**

This configuration file helps to fit with the requirements of [CDE implementation docs](https://github.com/ejp-rd-vp/CDE-semantic-model-implementations/tree/master/YARRRML_Transform_Templates) 

```yaml
Diagnosis:
  cde: Diagnosis # Model tagname to identify the proper CDE
  columns: # columns based on the requirements:
    pid: pat_id # pid is the tagname for patient identifier based on CDE implementations docs
                # pat_id is the name of the column in your datatable 
    valueAttributeIRI: diagnosis
    valueOutput_string: diagnosis_label # same for any column required
    startdate: diagnosis_date
    enddate: diagnosis_date

# you can add all model tagname you want as a new YAMl object
```
exemplar YAML file [here](https://github.com/pabloalarconm/hefesto/blob/main/data/CDEconfig.yaml) 

**Test:**

```py
from Hefesto.main import Hefesto
import yaml

# Import YAML configuration file with all parameters:
with open("data/config.yaml") as file:
    configuration = yaml.load(file, Loader=yaml.FullLoader)

test = Hefesto(datainput = "../data/OFFICIAL_DATA_INPUT.csv")
transform = test.transform_shape(configuration=configuration, clean_blanks = True) #, clean_blanks=False
# label = test.get_label("outputURI")
# url_from_label= test.get_uri("outputURI_label","ncit")
# repl= test.replacement("outputURI_label", "Date","DateXXX", duplicate=False)
transform.to_csv ("../data/result6.csv", index = False, header=True)
```

