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


def parse_json(json_string: str) -> dict:
    """
    Parse json parses the presumed json string or throws error
    :param json_string:
        a presumed string of json
    :return:
        parsed json object
    """
    print(f"Parsing Payload...", end="")
    print(payloads_type + "...", end=" ")
    try:
        payloads = json.loads(json_string)
    except ValueError:
        print_err(Severity.fatal, f"failed to parse payloads "
                                  f"\n{json_string}")
        print_exit(es="Bad JSON given, this commonly occurs with bad quotes\n"
                      "       or other characters requiring escape")
        pass
    if DEBUG:
        print(f"\nReceived:"
              f"\n{ansi_blue} {payloads_type} {payloads}){ansi_blue}")
    print_done()
    return payloads


def validate_payloads(json_string: str) -> dict:
    """
    Validates the json has all required attributes in the proper structure

    :param json_string:
       Payloads objected i.e. the parsed object from first step
    :return:
        json object
    """
    control_dict = parse_json(json_string)

    if not json_string:
        raise RuntimeError("json_string cannot be null")

    print("Validating Payloads data...", end="")
    try:
        gist_id = control_dict["gist_id"]
        token = control_dict["token"]
        payloads = control_dict["payloads"]["files"]
        commit_message = control_dict["payloads"]["description"]
        if DEBUG:
            print(f"gist_id: {gist_id} token: {token}"
                  f"\ncommit_message:{commit_message}"
                  f"\npayloads:{payloads}\n")
        # add the rest of the needs for checking the keys
    except KeyError:
        print_err(Severity.fatal, f"Failed to validate payloads"
                                  f"{json_string}")
        print_exit(es="Required control attributes not present in json")
    for payload in payloads:
        validate_payload(payloads[payload])
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
        if DEBUG:
            print(f"payload: {payload}")
    except KeyError:
        print_err(Severity.fatal, f"Failed to validate payload"
                                  f"{pl}")
        print_exit(es="Required payload attributes not present in json")


def send_payloads(control_dict: dict) -> ...:
    """
    Sends the payloads to gist
    :param control_dict: The dictionary with all necessary data
    :return:
    """
    try:
        params = {"scope": "gist"}
        payload = control_dict["payloads"]
        payload["public"] = True
        headers = {'Authorization': f'token {control_dict["token"]}'}
        r = requests.post('https://api.github.com/gists/'
                          + control_dict["gist_id"], data=json.dumps(payload),
                          headers=headers, params=params)

        if r.status_code == 200:
            pass
        elif r.status_code == 401:
            raise RuntimeError("invalid authentication credentials")
        elif r.status_code == 404:
            raise \
                ValueError("Gist Not Found")
        else:
            raise NotImplementedError("Unknown Error")
    except ValueError:
        print_err(Severity.fatal, "Requests failed see traceback")
        print_exit(es="\n1. Bad Gist ID"
                      "\n2. No Internet"
                      "\n3. Gremlins?"
                      "\n4. I a terrible program and failed to handle this")
    except RuntimeError:
        print_err(Severity.fatal, "Remote rejected the request")
        print_exit(es="\n1. Please check to ensure you have a gist scope secret"
                      "\n2. Double check you have copied the secret correctly")
    except NotImplementedError:
        print_err(Severity.fatal, "Its Foobar")
        print_exit(es="Yup .... still foobar")


# Output color correction for windows during testing
if platform.system() == "Windows":
    test = os.system("color 0")

# Get and parse payloads
try:
    payloads_type = sys.argv[2]
except IndexError:
    print_err(Severity.fatal, "Argument 2 not found")
    print_exit(es="\n1. Poorly escaped characters in terminal execution?"
                  "\n2. Second argument not provided")
try:
    if payloads_type == "JSON":
        data = validate_payloads(sys.argv[1])
        send_payloads(data)
    else:
        sys.exit(f"{ansi_red}FATAL:{ansi_yellow}"
                 f"Unsupported Payload type ({payloads_type}), terminating")
finally:
    os.system("outs='email?'")
# https://script.google.com/home/projects/1Lj1AVb5E9__ArUuvzQOrg3iNQtqufYT97MkCEo0MDzXRf7r7ZLPrfb-c/edit