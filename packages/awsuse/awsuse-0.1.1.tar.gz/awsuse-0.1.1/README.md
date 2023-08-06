# awsuse

A CLI tool to easily switch the AWS CLI active `default` profile by changing directly the `~/.aws/config` and the `~/.aws/credentials` file.

## Instalation
pip install git+https://github.com/aflopes/awsuse.git

## Usage
```
awsuse --help
Usage: awsuse [OPTIONS] SOURCE_PROFILE

Options:
  --credentials-file PATH     Path to aws cli credentials file
  --config-file PATH          Path to aws cli config file
  --token-code TEXT           MFA token code (applicable on MFA based
                              profiles)
  --session-duration INTEGER  Session duration in seconds (applicable on MFA
                              based profiles)
  --help                      Show this message and exit.
```

## Supported profile types

* Simple profiles
* MFA Profiles
* SSO profiles


### Simple profiles

These are simple profiles that define only the `aws_access_key_id` and `aws_secret_access_key` credentials.

For these, it just copies the profile values defined in both `credentials` and  `config` file into those files `[default]` section


### MFA profiles

These are profiles that contain the key `mfa_serial` defined in the `config` file. 

It uses the `SOURCE_PROFILE` definition, the token code (`--token-code`) to get a new session token with credentials from AWS STS and writes them into the `[default]` section of the `credentials` file. It also copies the profile configs into the `config` file `[default]` section


### SSO profiles

These are profiles that contain the key `sso_session` defined in the `config` file.

For these profiles this CLI ony copies the profile `config` settings into the `[default]` section.

If the specified `sso_session` is expired, this CLI will not try to refresh it automaticaly.