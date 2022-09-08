import argparse
import pandas as pd 

parser = argparse.ArgumentParser(description="flownet anomaly detection")
parser.add_argument('--input_file', type=str, default="", help='Excel file')
parser.add_argument('--output_file', type=str, default="output.txt", help='txt output file')
args = parser.parse_args()

EDIT_COMMAND       = """edit "%s" """
SET_MEMBERS_COMMAND    = """    set member %s"""

def get_members_list(data):
    rule = ""
    for src in data.split(","):
        rule = rule + "\"" + src.split("(")[0][:-1] + "\" "
    return rule

if __name__ == '__main__':
    excel_data = pd.read_excel(args.input_file)
    data = pd.DataFrame(excel_data)
    total_command_str = ""
    for i in range(len(data)):
        command_string = EDIT_COMMAND % (data.iloc[i]["network.name"].split("(")[0][:-1])  + "\n"
        members = get_members_list(data.iloc[i]["network.members"]) 
        command_string = command_string + SET_MEMBERS_COMMAND % (members)  + "\n"
        command_string = command_string + "next\n"
        total_command_str = total_command_str + command_string

    with open(args.output_file, 'w') as f:
        f.write(total_command_str)