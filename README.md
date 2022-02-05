# DSC180 Capstone Project

### Build instructions

In the home directory, running `python run.py --targets` builds the requisite files.

#### Targets:

1. `test-data`: loads test-data files from `test/testdata', cleans and saves them in `data/clean`.
2. `features`: reads clean data files from `data/clean`, builds features, joins the files, and stores the columns of resulting dataframe in different files under `data/out`.
3. `model`: trains the model and saves it under `results/` directory. **RUNNING THIS TAKES A WHILE FOR THE FIRST TIME BECAUSE OF THE IMPORT STATEMENT. AFTER THAT IT'S INSTANTANEOUS.**
4. `test`: provides the functionality of above 3 targets combined.

### Directory Map

1. `config/`: contains the configuration `.json` files.

    a. `create-test-data-params.json`: config file to build test-data.
    
    b. `data-params.json`: config file for cleaning data in the future.
    
    c. `eda-params.json`: config file for any EDA figures that will be generated.
    
    d. `features-params.json`: config file for building features from clean data.
    
    e. `model-params.json`: config file for model parameters.
    
    f. `test-data-params.json`: config file for cleaning current data.

2. `data/`: contains the various data files after initial ETL. Populated by running the script.
    a. `clean/`: contains the clean data after ETL. 
    b. `out/`: contains the data after feature generation.
    
3. `notebooks/`: notebooks with some EDA and experimentation. This will later contain nicely formatted plots and associated analyses.
4. `references/`: this will contain acknowledgement for any models or results that we use to build our project off of.
5. `results/`: running the build script populates this directory with the trained model (`.pkl`) and a `.txt` file which outlines the model performance.
6. `src/`: contains all the script `.py` files.

    a. `data/`: `create_test_data.py` creates test-data in the `test/testdata` directory; `etl.py` cleans data and loads them into `data/clean` directory.
    
    b. `features/`: `build_features.py` performs feature engineering on clean data and populates `data/out` with files that can be used to train and test the models.
    
    c. `models/`: `train_model.py` trains the model and saves it in a `.pkl` file ; `test_model.py` makes predictions using the saved model and saves the performance metric in a `.txt` file. Both files are stored in `results/` directory.
    
    d. `helper_functions.py`: library of functions that are used to perform common tasks.
    
7. `test/`: contains `testdata/` which can be populated by running the `create_test_data.py`.
8. `dockerfile`: creates a container with the necessary libraries and packages to run all the scripts.
9. `run.py`: running this script builds the requisite files.
10. `submission.json`: contains the dockerhub-id for building the container and build-script command to build the targets.
