# PyEmblem 

## Descriptions
Create dynamic badges using string payloads of various types. 
Currently, only JSON is being leveraged but there are plans to expand to more payload types in the future.

### Usage Potential
- Need to create multiple badges all at once from a single github workflow job
- Reading repository files in supported formats such as goals status / version data ect.


## MVP Details

###  Goals  
| Goal | Status |
| - | - |
| Create multiple Gist posts from a single JSON payload ensuring required attributes are present |[![YourActionName Actions outputs](https://img.shields.io/badge/Status-Achieved-green)](https://github.com/ferretux/pyemblem)|
| Validated Gists posts contain / must contain shield.io compatible json for use with /endpoint |[![YourActionName Actions Status](https://img.shields.io/badge/Status-In_Progress-yellow)](https://github.com/ferretux/pyemblem)|
| Runs as a Github Composite workflow |[![YourActionName Actions Status](https://img.shields.io/badge/Status-In_Progress-yellow))](https://github.com/ferretux/pyemblem)|
| Detailed training materials for using with your projects |[![YourActionName Actions Status](https://img.shields.io/badge/Status-In_Progress-yellow))](https://github.com/ferretux/pyemblem)|


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

## How To
TBD
### Getting your GistID
TBD

### Getting/Creating your Github Secret
TBD

### Json Structure
TBD

### Json Common Issues
TBD

### Extracting and using your badges
TBD