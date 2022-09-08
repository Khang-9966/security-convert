import argparse
import pandas as pd 

parser = argparse.ArgumentParser(description="flownet anomaly detection")
parser.add_argument('--input_file', type=str, default="", help='Excel file')
parser.add_argument('--output_file', type=str, default="output.txt", help='txt output file')
args = parser.parse_args()

EDIT_COMMAND                 = """edit "%s" """
SET_INTERFACENAME_COMMAND    = """    set associated-interface "%s" """
SET_ADDRESSES_COMMAND        = """    set subnet %s"""


if __name__ == '__main__':
    excel_data = pd.read_excel(args.input_file)
    data = pd.DataFrame(excel_data)
    total_command_str = ""
    for i in range(len(data)):
        command_string = EDIT_COMMAND % (data.iloc[i]["network.name"].split("(")[0][:-1])  + "\n" 
        command_string = command_string + SET_INTERFACENAME_COMMAND % (data.iloc[i]["interface.name"])  + "\n"
        command_string = command_string + SET_ADDRESSES_COMMAND % (data.iloc[i]["network.addresses"])  + "\n"
        command_string = command_string + "next\n"
        total_command_str = total_command_str + command_string

    with open(args.output_file, 'w') as f:
        f.write(total_command_str)