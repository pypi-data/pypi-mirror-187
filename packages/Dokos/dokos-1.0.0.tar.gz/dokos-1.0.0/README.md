# Dokos

[![pipeline status](https://gitlab.cylab.be/cylab/dokos/badges/main/pipeline.svg)](https://gitlab.cylab.be/cylab/dokos/-/commits/main)
[![Latest Release](https://gitlab.cylab.be/cylab/dokos/-/badges/release.svg)](https://gitlab.cylab.be/cylab/dokos/-/releases)

A simple Python brute-force login cracker. Basically, a simplified Python version of Hydra [https://github.com/vanhauser-thc/thc-hydra].


## Installation

Easiest way to install is using pip:

```bash
python3 -m pip install dokos
```

## Usage

You can now use with 

```bash
dokos -l <login> -P <passwords list> -f <failed login message> <url>
```

The **failed login message** is required so dokos can recognize when a login attempt has failed, and hence to detect
when login is sucessfull.

For example:

```bash
dokos -l jane.doe@example.com -P 10-million-password-list.txt -f "Bad combination of e-mail and password" https://example.com/login
```
