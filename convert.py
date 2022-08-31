import argparse
import pandas as pd 

parser = argparse.ArgumentParser(description="flownet anomaly detection")
parser.add_argument('--input_file', type=str, default="", help='Excel file')
parser.add_argument('--output_file', type=str, default="output.txt", help='txt output file')
parser.add_argument('--start_index', type=int, default=1016, help='edit start index')
args = parser.parse_args()

SET_NAME_COMMAND       = """set name "%s" """
SET_SRCINTF_COMMAND    = """set srcintf "%s" """
SET_DSTINTF_COMMAND    = """set dstintf "%s" """
SET_SRCADDR_COMMAND    = """set srcaddr %s"""
SET_DSTADDR_COMMAND    = """set dstaddr %s"""
SET_ACTION_COMMAND     = """set action %s"""
SET_SCHEDULE_COMMAND   = """set schedule "%s" """
SET_SERVICE_COMMAND    = """set service "%s" """
SET_LOGTRAFFIC_COMMAND = """set logtraffic all"""
SET_FSSO_COMMAND       = """set fsso disable"""
SET_COMMENTS_COMMAND   = """set comments "%s" """

def get_list_src_des(data):
    rule = ""
    for src in data.split(","):
        rule = rule + "\"" + src.split("(")[0][:-1] + "\" "
    return rule

if __name__ == '__main__':
    excel_data = pd.read_excel(args.input_file)
    data = pd.DataFrame(excel_data)
    start_index = args.start_index
    total_command_str = ""
    for i in range(len(data)):
        command_string = "edit " + str(start_index+i) + "\n"
        command_string = command_string + SET_NAME_COMMAND % (data.iloc[i]["rule.name"])  + "\n"
        command_string = command_string + SET_SRCINTF_COMMAND % (data.iloc[i]["rule.sourceZone"])  + "\n"
        command_string = command_string + SET_DSTINTF_COMMAND % (data.iloc[i]["rule.destinationZone"])  + "\n"
        rule_source = get_list_src_des(data.iloc[i]["rule.source"])
        rule_des = get_list_src_des(data.iloc[i]["rule.destination"])
        command_string = command_string + SET_SRCADDR_COMMAND % (rule_source)  + "\n"
        command_string = command_string + SET_DSTADDR_COMMAND % (rule_des)  + "\n"
        command_string = command_string + SET_ACTION_COMMAND % (data.iloc[i]["rule.action"].lower())  + "\n"
        command_string = command_string + SET_SCHEDULE_COMMAND % (data.iloc[i]["rule.schedule"])  + "\n"
        command_string = command_string + SET_SERVICE_COMMAND % (data.iloc[i]["rule.service"].replace(",","""\" \""""))  + "\n"
        command_string = command_string + SET_LOGTRAFFIC_COMMAND + "\n"
        command_string = command_string + SET_FSSO_COMMAND  + "\n"
        command_string = command_string + SET_COMMENTS_COMMAND % (data.iloc[i]["rule.comment"])  + "\n"    
        command_string = command_string + "next\n"
        total_command_str = total_command_str + command_string

    with open(args.output_file, 'w') as f:
        f.write(total_command_str)