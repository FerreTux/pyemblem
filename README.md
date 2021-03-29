# PyEmblem@Dev
[![badbge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/FerreTux/761627e5ad10843ebc983328034a8e3f/raw/ferretuxLogo)]() 

#### Checks:
![status](https://github.com/FerreTux/PyEmblem/actions/workflows/create_badges.yml/badge.svg)
![status](https://github.com/FerreTux/PyEmblem/actions/workflows/linting.yml/badge.svg)


## Descriptions
Create dynamic badges using json file payloads. 
Currently, only JSON is being leveraged but there are plans to expand to more payload types in the future.

### This is currently in testing for all Shields.io fields. 
**Working**
- label
- message
- color
- namedLogo
- style
- logoColor
- labelColor
- isError

**Untested**

- logoSvg
- logoWidth
- logoPosition
- cacheSeconds

### Usage Potential
- Need to create multiple badges all at once from a single github workflow job
- Reading repository files in supported formats such as goals status / version data ect.

## How To
### Badge Json Structure
1. **Create your Badge JSON file in your repo**
   - This can be dynamically created from other processes or statically driven with a file in your repo
   - The fields below each badge are all the fields supported by ![Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/FerreTux/761627e5ad10843ebc983328034a8e3f/raw/ShieldsBadge) 
   - It should look something like ( PyEmblem will try to validate these and provide feedback if they do not match pattern )
```json
  
{
  "<BadgeName>": {
    "content": {
      "label": "A Foot",
      "message": "At the Circle K",
      "color": "orange"
    }
  },
  "<BadgeName2>": {
    "content": {
      "label": "hello",
      "message": "world",
      "color": "orange"
    }
  }
}
```

### Getting your GistID
**Create a new gist for the output** [![badbge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/FerreTux/761627e5ad10843ebc983328034a8e3f/raw/GistBadge)](https://gist.github.com/) 
  - Recommend naming the new gist based on the project & just adding something generic to the content 
  - In the URL you should see something like 
     - ```https://gist.github.com/FerreTux/761627e5ad10843ebc983328034a8e3f#file-pyemblembadges```
     - Your Gist Id is the long string in the middle: **761627e5ad10843ebc983328034a8e3f**
     - Save this you will need this for later steps
  ![image](https://i.imgur.com/0mFh5Kf.png)
       
### Getting/Creating your Github Secret
1. **Create a new secret** 
  - Profile Settings - > Developer Settings - > Personal Access Token
  - Make sure to give this new secret gist scope  
  - Once created it will display a long alphanumeric.  Copy this you will need it in next step
2. **Create a local repository secret variable** 
  - Repository - > Settings -> Secrets
  - Name it something like ``` GIST_SECRET ```
  - Paste your secret token into it,  That long Alphanumeric from last step

### Setting up your workflow
1. Create a new workflow in your repository and add the below with your gist id from previous steps and your secret name
```yaml
# Reads a json file of statuses for badges

name: get_goal_status

# Controls when the action will run. 
on:
  # Triggers the workflow on push or pull request events but only for the master branch
  push:
    branches: [ master ]
jobs:
 job3:
  runs-on: ubuntu-latest
  steps:
  - uses: actions/checkout@v2
    env:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  - id: pyemblem
    uses: FerreTux/pyemblem@Dev
    with:
      payloads_file: "<Your File>.json"
      token: "${{ secrets.<YOUR SECRET NAME>> }}"
      gist_id: "<YOUR GIST ID>"
      commit_message: "<What ever generic commit message you want, can be nonsense>"
  - id: echo
    run: |
      echo "Badges Created... We Hope? otherwise something is a foot at the Circle K"
```


### Extracting and using your badges
- Linked Badge
```md
[![Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/<UserName>/<GistID>/raw/<BadgeName>)](httpe://place.tolink.to)
```
- Unlinked Badge
```md
![Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/<UserName>/<GistID>/raw/<BadgeName>)
```

- Recommend adding this to your readme somewhere as well
```md
Badge Creation: ![](https://github.com/FerreTux/PyEmblem/actions/workflows/your_workflow.yaml/badge.svg)
```


## MVP Details

###  Goals  

| Goal | Status |
| - | - |
| Create multiple Gist posts from a single JSON payload ensuring required attributes are present | ![](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/FerreTux/761627e5ad10843ebc983328034a8e3f/raw/GoalBadge1) |
| Validated Gists posts contain / must contain shield.io compatible json for use with /endpoint | ![](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/FerreTux/761627e5ad10843ebc983328034a8e3f/raw/GoalBadge2) |
| Runs as a Github Composite workflow | ![](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/FerreTux/761627e5ad10843ebc983328034a8e3f/raw/GoalBadge3) |
| Detailed training materials for using with your projects | ![](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/FerreTux/761627e5ad10843ebc983328034a8e3f/raw/GoalBadge4) |

### Non-Goals
- Support for more than just shield.io
- Support for more than just json payloads
- Branding / Logo generation

### User Stories
- Create multiple shields.io dynamic badges with a single payload request
- Composite this workflow with other workflows to create all of your badge needs

### Expected Subsystems
- **Main**
  - Validating payload structure
  - Posting to Gist
  
    
## Future Goals/ideas
- Support more stringable file types
  - xml
  - csv 
  - etc.
- Toggleable composite output such that you can also use the workflow to output proper shields.io JSON to your workflow
- Sends Email notification of results or errors