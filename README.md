# Climate-Friendly Food Systems (CFFS) Labelling Project

UBC Institute for Resources, Environment and Sustainability (IRES)

![Linting](https://img.shields.io/badge/linting-pylint-yellowgreen)

## Objective
To implement the Climate-Friendly Food Systems (CFFS) definition at the UBC Campus by producing the weighted metric that informs the choice of icon for each menu item served by UBC Food Services. Currently, this framework conducts the evaluation of greenhouse gas (GHG) emissions, nitrogen loss, freshwater withdrawals, Land use, and stress-weighted water withdrawals of recipes per serving and 100 grams.

## Scope

The Climate-Friendly Food Sustainability (CFFS) labelling is carried out on four sites, three of which are for UBC Food Services and the last one for AMS. 
- UBC Food Services: Open Kitchen, Gather, Feast
- AMS: The Gallery

## Repository Structure

    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── archive        <- Previous year's data    
    │   ├── cleaning       <- Cleaned datasets
    │   ├── external       <- External dataset for support
    │   ├── final          <- Final calculation results
    │   ├── mapping        <- Dataset with all factors mapped
    │   ├── Misc           <- Miscellanous
    │   ├── New Items      <- New Items in Current Calculation               
    │   ├── preprocessed   <- Preprocessed datasets
    │   └── raw            <- Raw recipes data from Optimal Control
    │
    ├── Misc_Notebooks     <- Miscellaneous Notebooks
    ├── Archived_Notebooks <- Archived Notebooks
    │
    ├── Label_Baseline_Calculation <- Notebooks for Baseline Calculation
    │ 
    ├── Notebooks_UBCFS
    │   └── 1_data_preprocessing.ipynb
    │   └── 2_data_cleaning.ipynb
    │   └── 3_update_info_and_mapping.ipynb
    │   └── 4_data_analysis.ipynb
    │   └── 5_Recipes_Labelling.ipynb
    │
    ├── Notebooks_AMS
    │   └── 1_data_preprocessing.ipynb
    │   └── 2_data_cleaning.ipynb
    │   └── 3_update_info_and_mapping.ipynb
    │   └── 4_data_analysis.ipynb
    │   └── 5_Recipes_Labelling.ipynb
    │
    └── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
        └── figures        <- Generated graphics and figures to be used in reporting

## Instructions

### Baseline Calculation

All baseline calculations are done in ```Label_Baseline_Calculation/baseline_OK.ipynb```. If baseline is updated or a new parameter is added, then please run the file again with updated data files store in ```data/Misc/data_for_calculating_baseline```. 

### Label Calculation Process

Although the labelling process is similar between UBCFS and AMS, there are some differences due to different input sources. The detailed explanation for UBCFS and AMS are written in their respective notebooks.

Instructions for running the analysis processes:
1. To complete analysis for UBC Food Services Products navigate to the **UBCFS/RECIPE_PROCESSES_2023_2024** directory where you will see 5 files that each complete one step of the analysis proceedure. More information on the particular inputs and files required are provided as comments in all code cells.
2. To complete anaylsis for UBC AMS navigate to the **AMS_2023_2024_Current_Version/RECIPE_PROCESSES_2023_2024** directory where you will see 5 files that each complete one step of the analysis proceedure. More information on the particular inputs and files required are provided as comments in all code cells.
3. NLP Model Google Colab Workbook: https://colab.research.google.com/drive/1pckGYAkNr7-rkkefSF6GWSJlBQZN9T--?usp=sharing
4. To automate the manual work of assigning GHG categories to the ingredients list, look at the files inside the **Misc_Notebooks/Categorizing_IDs_to_GHG_IDs** directory.
