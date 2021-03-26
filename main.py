import requests
import json
import sys

term_green = f"\N{ESC}[33m"
term_white = f"\N{ESC}[0m"


# get and parse payloads
payloads = sys.argv[0]
payloads_type = sys.argv[1]
if payloads_type == "JSON":
    payloads = json.loads(payloads)

print(f"{term_white} payload:{term_green}")


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
