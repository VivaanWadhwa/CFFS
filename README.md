# Climate-Friendly Food Systems (CFFS) Labelling Project

UBC Institute for Resources, Environment and Sustainability (IRES)

![Linting](https://img.shields.io/badge/linting-pylint-yellowgreen)

## Objective
To implement the Climate-Friendly Food Systems (CFFS) definition at the UBC Campus by producing the weighted metric that informs the choice of icon for each menu item served by UBC Food Services. Currently, this framework conducts the evaluation of greenhouse gas (GHG) emissions, nitrogen loss, freshwater withdrawals, Land use, and stress-weighted water withdrawals of recipes per serving and 100 grams.

## Scope

The Climate-Friendly Food Sustainability (CFFS) labelling is carried out on five sites, three of which are for UBC Food Services and the two for AMS. 
- UBC Food Services: Open Kitchen, Gather, Feast
- AMS: The Gallery, Blue Chip

The `src` folder is structured into two main parts to accommodate the use of different languages in the `frontend` and `backend`.

### Backend
The `backend` folder contains scripts responsible for the logic behind the various pages. Additionally, the `lib` folder within the `backend` houses foundational classes that support the development of these scripts. Each class serves a specific purpose, and further details can be found in their respective files.

### Frontend
For the frontend, we are utilizing `Electron`. The `main.js` file is responsible for rendering the various HTML pages. 

- Each page, except the homepage, is organized in its own folder. These folders include the page-specific `index.html`, `styles.css`, and `renderer.js` files.
- Additional JavaScript files are included to handle specific functionalities, and their respective files provide more detailed explanations.

This structure ensures a clear separation of concerns and enhances maintainability.

## Instructions

### Backend Setup:

1. Set up your virtual environment using the following commands:

   ```bash
   python3 -m venv cffs
   source cffs/bin/activate
   pip install -r requirements.txt
   ```

2. To create an executable from your script, use the `./create-exe.sh` file, passing the path to your script as an argument. For example:

   ```bash
   ./create-exe.sh path/to/your_script.py
   ```

   All executables created this way will be stored in the `dist` folder.

**Note:** Ensure that your scripts are generalized and accept arguments for flexibility, as the frontend executes these scripts by spawning child processes.

---

### Frontend Setup:

1. **Electron Version**: 2.0.2

2. Start the application using the `./run_frontend.sh` bash script:

   ```bash
   ./run_frontend.sh
   ```


