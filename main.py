import requests
import json
import sys
import os
import platform

# ansi color definitions
ansi_yellow = "\u001b[33m"
ansi_blue = "\u001b[34m"
ansi_red = "\u001b[31m"
ansi_white = "\u001b[0m"

# Output color correction for windows during testing
if platform.system() == "Windows":
    test = os.system("color 0")

print(f"Parsing Payload...", end="")

# Get and parse payloads
payloads = sys.argv[1]
payloads_type = sys.argv[2]
if payloads_type == "JSON":
    try:
        payloads = json.loads(payloads)
    except:
        raise Exception(f"failed to parse payloads, {payloads}")
else:
    sys.exit(f"{ansi_red}FATAL:{ansi_white}"
             "Unsupported Payload type, terminating")

print(f"{ansi_blue}Done{ansi_white}")


print(f"Payloads Received:{ansi_blue} {payloads_type} {payloads})")



# token='06856f710fe5506761846cdea53512c184703cac'
# payloadfile="test2-json"
# filename="test.json"
# gist_id="6893c0f3525f80df7f47f2134e72c412"

# params={'scope':'gist'}
# payload={"description":"GIST a by python code","public":True,"files":{"test":{"content":"Python a has 3 parameters: 1)Request URL\n 2)Header Fields\n 3)Parameter \n4)Request body"}}}

# content=open(filename, 'r').read()
# headers = {'Authorization': f'token {token}'}
# r = requests.post('https://api.github.com/gists/'+gist_id, data=json.dumps(payload),headers=headers, params=params)
# @r = requests.post('https://api.github.com/gists/'+gist_id+"#file-test.json", data=json.dumps({'files':{filename:{"content":content}}}),headers=headers, params=params)
# print(r.status_code)
# print(r.json())
# if file doesn't exist create it
