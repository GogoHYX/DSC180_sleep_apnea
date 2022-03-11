# DSC180 Capstone Project
## [Project Website](https://gogohyx.github.io/DSC180_sleep_apnea/)
### Build instructions

In the home directory, running `python run.py --targets` builds the requisite files.

#### Targets:

1. `features`: reads raw data files, builds features, joins the files, and stores the columns of resulting dataframe in different files under `data/out`.
2. `model`: trains the voting models and saves them under `results/` directory. **RUNNING THIS TAKES A WHILE FOR THE FIRST TIME BECAUSE OF THE IMPORT STATEMENT. AFTER THAT IT'S INSTANTANEOUS.**
3. `predict`: loads the saved models, makes predictions, stores them under `results/` directory, and also stores the model recall values in a `.txt` file.
4. `test`: provides the functionality of `1` `2` and `3` targets combined, on the test raw data.
5. `all`: provides the functionality of `1` `2` and `3` targets combined, on the real raw data

### Directory Map

1. `config/`: contains the configuration `.json` files.

    a. `create-test-data-params.json`: config file to build test-data.
    
    b. `data-params.json`: config file for cleaning data in the future.
    
    c. `eda-params.json`: config file for any EDA figures that will be generated.
    
    d. `features-params.json`: config file for building features from raw data.

    e. `test-features-params.json`: config file for building features from test raw data.
    
    f. `model-params.json`: config file for model parameters.

    g. `test-model-params.json`: config file for test model parameters.
    
    h. `data-params.json`: config file for cleaning current data.

2. `data/`: contains the raw data files and data files after feature engineering. 

    a. `raw/`: contains the raw data files downloaded from source. _Does not include anything in the repo because raw data is confidential_. 
    
    b. `out/`: contains the data after feature generation.
    
3. `notebooks/`: notebooks with some EDA and experimentation. This will later contain nicely formatted plots and associated analyses.
4. `references/`: this will contain acknowledgement for any models or results that we use to build our project off of.
5. `results/`: running the build script populates this directory with the trained models (`.pkl`) and a `.txt` file which outlines the model performance.
6. `src/`: contains all the script `.py` files.
    
    a. `features/`: `build_features.py` performs feature engineering on clean data and populates `data/out` with files that can be used to train and test the models.
    
    b. `models/`: `train_model.py` trains the voting models and saves them in a `.pkl` file ; `test_model.py` makes predictions using the saved models and saves the performance metric in a `.txt` file. Both files are stored in `results/` directory.
    
    c. `helper_functions.py`: library of functions that are used to perform common tasks.
    
7. `test/`: contains `testdata/` which has the artificially generated test data.
8. `dockerfile`: creates a container with the necessary libraries and packages to run all the scripts.
9. `run.py`: running this script builds the requisite files.
10. `submission.json`: contains the dockerhub-id for building the container and build-script command to build the targets.
