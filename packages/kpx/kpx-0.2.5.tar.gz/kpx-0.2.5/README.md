[![pipeline status](https://gitlab.com/kisphp/python-cli-tool/badges/main/pipeline.svg)](https://gitlab.com/kisphp/python-cli-tool/-/commits/main)
[![coverage report](https://gitlab.com/kisphp/python-cli-tool/badges/main/coverage.svg)](https://gitlab.com/kisphp/python-cli-tool/-/commits/main)
[![Latest Release](https://gitlab.com/kisphp/python-cli-tool/-/badges/release.svg)](https://gitlab.com/kisphp/python-cli-tool/-/releases)

## Install

```bash
# Install or update it from pip
pip install -U kpx

# Install or update it from gitlab
pip install -U kpx --index-url https://gitlab.com/api/v4/projects/24038501/packages/pypi/simple
```


## Usage

```bash
# Configure profile region and output type
kpx conf [profile-name] [aws-zone] [output-type]

# Configure profile credentials
kpx cred [profile-name] [access-key-id] [secret-access-key]

# List route53 hosted zones
kpx r53

# List records in a hosted zone
kpx r53 [zone-id]

# List ec2 instances (without pagination)
kpx ec2
```
