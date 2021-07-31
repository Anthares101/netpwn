<img alt="Test suite status" src="https://img.shields.io/github/workflow/status/anthares101/netpwn/CI?style=for-the-badge"> <img alt="Version v1.0" src="https://img.shields.io/badge/version-v1.0-blue?style=for-the-badge"> <img alt="GPL-2.0 license" src="https://img.shields.io/github/license/anthares101/netpwn?style=for-the-badge">

# Netpwn - A netcat listener alternative

The idea of this Linux tool is to be an alternative to a Netcat listener but with the ability to determine if the received conection is a shell or not. If the conection is a shell Netpwn will also try to stabilize it to get a pty (Only Linux and MacOS shells).

## Requirements

You need Python 3 installed in your system and also Pwntools, that can be installed executing the next command (Keep in mind that this tool only works in Linux):

```bash
pip3 install -r requirements.txt
```

You can use a virtual env to install the dependencies or intall them system wide.

## Usage

If you have all the requirements you can start playing! You can add the repository folder to your `PATH` and execute the tool everywhere.

```
Netpwn  - A netcat listener alternative

usage: netpwn.py [-h] [-v] [--no-pty] [-P LPORT]

A listener capable of stabilize Linux and MacOS reverse shells automatically

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  --no-pty              if this flag is set, no shell stabilization is perform
  -P LPORT, --lport LPORT
                        the port used to listen for the reverse shell (Default: 8080)
```
