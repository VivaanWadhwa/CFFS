import calculator
import labeller
import os
import glob

def checkFunc(filepath):
    labeller_obj = labeller.Labeller(filepath)
    calculator_obj = calculator.Calculator(labeller_obj)


filepath_list = glob.glob(os.path.join(os.getcwd(), "data", "raw", "Gather", "*.oc"))
checkFunc()