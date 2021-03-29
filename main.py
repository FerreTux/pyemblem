from io import TextIOWrapper

import requests
import json
import sys
import os
import platform
import traceback as tb
from enum import Enum
import re

# ansi color definitions
ansi_yellow = "\u001b[33m"
ansi_blue = "\u001b[34m"
ansi_red = "\u001b[31m"
ansi_white = "\u001b[0m"
ansi_cyan = "\u001b[36m"

# Debug control
DEBUG = True


class Severity(Enum):
    """
    Enum class to define console severitys for print functions
    """
    fatal = 1
    warning = 2


def print_done():
    """
    print done all pretty like
    :return:
    """
    print(f"{ansi_blue}Done{ansi_white}")


def print_err(severity: Severity, text: str) -> ...:
    """
    Print Exceptions the way I like them with Context and pretty
    :param severity: Enum from class definition above
    :param text: Additional conext you want printed
    :return:
    """
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
          f"{color}\n{tb.format_exc()}{ansi_white}")


def print_exit(es: str = ""):
    """
    print exit and override default tracebacks outputs + debug recommendation
    :param es: The exit string for debug output pass \n in from more lines
    :return:
    """
    sys.exit(f"Debug: {es}\nPlease see official documentation "
             "@ https://github.com/FerreTux/pyemblem")


def parse_json(file: TextIOWrapper) -> dict:
    """
    Parse json parses the presumed json string or throws error
    :param file:
        A file with the json
    :return:
        parsed json object
    """
    print(f"Parsing Payload...", end="")
    try:
        payloads = json.load(file)
    except FileNotFoundError:
        print_err(Severity.fatal, f"File Not found "
                                  f"\n{file}")
        print_exit(es="1. Bad filename\n"
                      "2. Directory issues")
        pass
    except ValueError:
        print_err(Severity.fatal, f"failed to parse payloads "
                                  f"\n{file}")
        print_exit(es="Bad JSON given, this commonly occurs with bad quotes\n"
                      "       or other characters requiring escape")
        pass

    if DEBUG:
        print(f"\nReceived:"
              f"\n{ansi_blue} {json.dumps(payloads)} {ansi_blue}")
    print_done()
    return payloads


def validate_payloads(json_file: str) -> dict:
    """
    Validates the json has all required attributes in the proper structure

    :param json_file:
       The file containing your json
    :return:
        json object
    """
    control_dict = {}
    with open(json_file) as file:
        badge_dict = parse_json(file)

    print("Validating Payloads data...", end="")
    try:
        control_dict["files"] = badge_dict
        control_dict["description"] = commit_message
        for payload in badge_dict:
            validate_payload(badge_dict[payload])
            badge_dict[payload]["content"] = f"""{badge_dict[payload]["content"]}"""
        # add the rest of the needs for checking the keys
    except KeyError:
        print_err(Severity.fatal, f"Failed to validate payloads see TB")
        print_exit(es="Required control attributes not present in json")

    print_done()
    return control_dict


def validate_payload(pl: dict):
    """
        Validates the json if each payload in the json
        has all required attributes in the proper structure for shield.io

        # Params
          pl = A single Payload objected within the payloads object
    """

    if DEBUG:
        print(f"\nReviewing payload: {pl} {type(pl)} {repr(pl)}")
    if not pl:
        raise RuntimeError()
    try:
        payload = pl["content"]

        # Ensure required fields exist in the dictionary
        try:
            for field in valid_dict:
                if valid_dict[field]["required"]:
                    val = payload[field]
        except ValueError:
            print_err(Severity.fatal,
                      f"Failed to find 'required' from the valid dictionary")
            print_exit(es="1. a required field was not supplied in the payload"
                          "2. This is a bug on PyEmblems End if it appears")
        # Ensure required fields follow format rules
        try:
            for field in payload:
                if valid_dict[field]["format_rule"]:
                    regex = re.compile(valid_dict[field]["format_rule"])
                    if not regex.match(payload[field]):
                        raise ValueError(f"Invalid Schema for {field}")
        except ValueError:
            print_err(Severity.fatal, f"Invalid Schema found"
                                      f"{pl}")
            print_exit(es="The field data failed to adhere to regex rules")
        if DEBUG:
            print(f"payload: {payload}")
    except KeyError:
        print_err(Severity.fatal, f"Failed to validate payload"
                                  f"{pl}")
        print_exit(es="Required payload attributes not present in json")
    payload["schemaVersion"] = 1



def send_payloads(payload: dict) -> ...:
    """
    Sends the payloads to gist
    :param control_dict: The dictionary with all necessary data
    :return:
    """
    try:
        params = {"scope": "gist"}
        payload["public"] = True
        if DEBUG:
            print(f"The payload to gist is: \n {payload}")
        headers = {'Authorization': f'token {token}'}
        r = requests.post('https://api.github.com/gists/'
                          + gist_id, data=json.dumps(payload),
                          headers=headers, params=params)
        if r.status_code == 200:
            pass
        elif r.status_code == 401:
            raise RuntimeError("invalid authentication credentials")
        elif r.status_code == 422:
            raise RuntimeError("Unprocessable Entity")
        elif r.status_code == 404:
            raise \
                ValueError("Gist Not Found")
        else:
            raise NotImplementedError(f"Unknown Error :{r.status_code}")
    except ValueError:
        print_err(Severity.fatal, "Requests failed see traceback")
        print_exit(es="\n1. Bad Gist ID"
                      "\n2. No Internet"
                      "\n3. Gremlins?"
                      "\n4. I a terrible program and failed to handle this")
    except RuntimeError:
        print_err(Severity.fatal, f"Remote rejected request {r.status_code}")
        print_exit(es="\n401: Please ensure you have a gist scope secret"
                      "\n401: Double check you have copied the secret correctly"
                      "\n422: Malformed request semantically erroneous")
    except NotImplementedError:
        print_err(Severity.fatal, "Its Foobar")
        print_exit(es="Yup .... still foobar")


print(sys.argv)
# Output color correction for windows during testing
if platform.system() == "Windows":
    foo = os.system("color 0")
    WINDOWS = True

"""
inputs:
  payloads_file:
    description: 'The file name to read'
    required: true
  token:
    description: 'Your github token with gist scope'
    required: true
  gist_id:
    description: 'Your github token with gist scope'
    required: true
  commit_message:
    description: 'Your github token with gist scope'
    required: true

"""


# Get and parse payloads
try:
    payloads_file = sys.argv[1]
    token = sys.argv[2]
    gist_id = sys.argv[3]
    commit_message = sys.argv[4]
    action_path = sys.argv[5]
except IndexError:
    print_err(Severity.fatal, "Argument/s not found")
    print_exit(es="\n1. Poorly escaped characters in terminal execution?")

try:
    lint_file_path = action_path + "\\valid_keys.json"
    if DEBUG:
        print(lint_file_path)
    with open(lint_file_path) as valid_keys_file:
        valid_dict = parse_json(valid_keys_file)
except RuntimeError:
    print_err(Severity.fatal, "Failed to load valid dictionary file")
    print_exit(es="\nThis is a bug on PyEmblems end if it appears")

data = validate_payloads(payloads_file)
send_payloads(data)


