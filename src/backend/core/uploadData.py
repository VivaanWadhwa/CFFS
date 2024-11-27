import os
import sys
import json

# Attempt to import the Outlet class from the src/backend/core/lib directory.
# If the module isn't found, modify the system path to include the current working directory
# and try importing again. Handle any other unexpected exceptions gracefully.
## Done as a workaround as it was not importing otherwise.
try:
    from src.backend.core.lib.outlet import Outlet
except ModuleNotFoundError as e:
    sys.path.insert(0, os.getcwd())
    from src.backend.core.lib.outlet import Outlet
except Exception as e:
    print(json.dumps({"status": "error", "message": str(e)}, indent=4))
    print(e)

if __name__ == "__main__":
    """
    This script processes product data for an outlet and generates a preprocessed JSON file.
    It expects three command-line arguments: outlet name, owner, and a file path to the product data.
    
    Workflow:
    1. Parse command-line arguments to get the outlet name, owner, and file path.
    2. Create an instance of the `Outlet` class, passing in the outlet name and owner.
    3. Use the `add_products` method of the `Outlet` class to process the product data file.
    4. Convert the processed data into a dictionary, add a status field, and save it as a JSON file.
    5. Print the JSON output for further use.
    """

    try:
        # Parse command-line arguments.
        outlet_name = sys.argv[1]  # Name of the outlet
        owner = sys.argv[2]        # Owner of the outlet
        filepath = sys.argv[3]     # Filepath to the product data
    except IndexError as e:
        # If any argument is missing, print an error message and exit with a non-zero status.
        error_message = {"status": "error", "message": str(e)}
        print(json.dumps(error_message, indent=4))
        sys.exit(1)
    
    # Initialize an Outlet object with the provided name, owner, and an empty product list.
    myOutlet = Outlet(outlet_name, owner, [])
    
    # Add products to the Outlet object by reading and processing the file at the specified path.
    myOutlet.add_products(filepath)

    # Convert the Outlet object to a dictionary format and add a "success" status.
    output = myOutlet.to_dict()
    output["status"] = "success"
    
    # Serialize the processed data to JSON format.
    json_output = json.dumps(output, indent=4)

    # Create the output directory for preprocessed data if it doesn't already exist.
    os.makedirs("data/preprocessed", exist_ok=True)
    
    # Write the JSON data to a file named after the outlet in the preprocessed directory.
    with open(f"data/preprocessed/{outlet_name}.json", "w") as f:
        f.write(json_output)
    
    # Print the JSON output for parsing by the frontend.
    print(json_output)
