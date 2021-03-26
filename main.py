import requests
import json
import sys
import os
import platform
import traceback as tb
from enum import Enum


# ansi color definitions
ansi_yellow = "\u001b[33m"
ansi_blue = "\u001b[34m"
ansi_red = "\u001b[31m"
ansi_white = "\u001b[0m"
ansi_cyan = "\u001b[36m"


# exit printer enum
class Severity(Enum):
    fatal = 1
    warning = 2


# Exception Printer
def print_err(severity: Severity, text: str) -> ...:
    if severity == Severity.fatal:
        color = ansi_red
        ctx = "FATAL"
    elif severity == Severity.warning:
        color = ansi_yellow
        ctx = "WARNING"
    else:
        color = ansi_blue
        ctx = "GENERAL"
    print(f"{color}\n{ctx}: {ansi_cyan}{text}"
          f"{color}{tb.format_exc()}{ansi_white}")


def print_exit(es: str = ""):
    sys.exit(f"Debug: {es}\nPlease see official documentation "
             "@ https://github.com/FerreTux/pyemblem")


def parse_json(json_string: str) -> object:
    """
    Parse json parses the presumed json string or throws error
    :param json_string:
        a presumed string of json
    :return:
        parsed json object
    """
    try:
        payloads = json.loads(json_string)
        return payloads
    except RuntimeError as err:
        error = True
        pass
    finally:
        print_err(Severity.fatal, f"failed to parse payloads "
                                  f"\n{json_string}\n")
        print_exit(es="Bad JSON given, this commonly occurs with bad quotes\n"
                      "       or other characters requiring escape")
        pass



def validate_payloads(pls: str):
    """
    Validates the json has all required attributes in the proper structure

    :param pls:
       Payloads objected i.e. the parsed object from first step
    :return:
    """
    if not pls:
        raise RuntimeError("pls cannot be null")

    print(f"Payloads Received:{ansi_blue} {payloads_type} {payloads}){ansi_blue} ")

    print("Validating Payloads data...", end="")
    try:
        token = pls["token"]
        file = pls["file"]
        name = pls["token"]
        description = pls["description"]
    except RuntimeError:
        pass
    finally:
        print_err(Severity.fatal, f"Failed to validate payloads"
                                  f"{pls}\n")
        print_exit(es="Required JSON attributes not added")


def validate_payload(pl):
    """
        Validates the json if each payload in the json
        has all required attributes in the proper structure for shield.io

        # Params
          pl = A single Payload objected within the payloads object
    """
    if not pl:
        raise RuntimeError()
    print(pl)
    return True


# Output color correction for windows during testing
if platform.system() == "Windows":
    test = os.system("color 0")

# Get and parse payloads
payloads_type = sys.argv[2]

print(f"Parsing Payload...", end="")
if payloads_type == "JSON":
    print(payloads_type + "...", end=" ")
    parse_json(sys.argv[1])
else:
    sys.exit(f"{ansi_red}FATAL:{ansi_yellow}"
             f"Unsupported Payload type ({payloads_type}), terminating")

print(f"{ansi_blue}Done{ansi_white}")


# token='06856f710fe5506761846cdea53512c184703cac'
# payloadfile="test2-json"
# filename="test.json"
# gist_id="6893c0f3525f80df7f47f2134e72c412"

# params={'scope':'gist'}
# payload={
    # "description":"GIST a by python code",
    # "public":True,
    # "files":{
    #   "test":{"content":"Python a has 3 parameters: 1)Request URL\n 2)Header Fields\n 3)Parameter \n4)Request body"}
    #   }}

# content=open(filename, 'r').read()
# headers = {'Authorization': f'token {token}'}
# r = requests.post('https://api.github.com/gists/'+gist_id, data=json.dumps(payload),headers=headers, params=params)
# @r = requests.post('https://api.github.com/gists/'+gist_id+"#file-test.json", data=json.dumps({'files':{filename:{"content":content}}}),headers=headers, params=params)
# print(r.status_code)
# print(r.json())
# if file doesn't exist create it
