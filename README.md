<img alt="Test status" src="https://img.shields.io/github/workflow/status/anthares101/netpwn/CI?style=for-the-badge"> <img alt="Version v1.2" src="https://img.shields.io/badge/version-v1.2-blue?style=for-the-badge"> <img alt="GPL-2.0 license" src="https://img.shields.io/github/license/anthares101/netpwn?style=for-the-badge">

# Netpwn - A netcat listener alternative

The idea of this Linux tool is to be an alternative to a Netcat listener but with the ability to determine if the received conection is a shell or not. If the conection is a shell Netpwn will also try to stabilize it to get a pty (Only Linux and MacOS shells).

## Installation

Just execute `pip3 install netpwn` and enjoy! You can use a virtual env or intall it system wide.

## Usage

```
Netpwn  - A netcat listener alternative

usage: netpwn [-h] [-v] [--no-pty] [-P LPORT]

A listener capable of stabilize Linux and MacOS reverse shells automatically

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  --no-pty              if this flag is set, no shell stabilization is perform
  -P LPORT, --lport LPORT
                        the port used to listen for the reverse shell (Default: 8080)
```
