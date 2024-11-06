import os
import sys
import json
try:
    from src.backend.core.lib.outlet import Outlet
except ModuleNotFoundError as e:
    sys.path.insert(0,os.getcwd())
    from src.backend.core.lib.outlet import Outlet
except Exception as e:
    print(json.dumps({"status": "error", "message": str(e)}, indent=4))
    print(e)



if __name__ == "__main__":
    # Create an outlet 

    try:
        outlet_name = sys.argv[1]
        owner = sys.argv[2]
        filepath = sys.argv[3]
    except IndexError as e:
        error_message = {"status": "error", "message": str(e)}
        print(json.dumps(error_message, indent=4))
        sys.exit(1)
    
    myOutlet = Outlet(outlet_name, owner, [])
    myOutlet.add_products(filepath)
    output = myOutlet.to_dict()
    output["status"] = "success"
    json_output = json.dumps(output, indent=4)
    print(json_output)



    
