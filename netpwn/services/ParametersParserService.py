import argparse
from netpwn.config import VERSION


class ParametersParserService:
	def __init__(self):
		self.parser = argparse.ArgumentParser(description='A listener capable of stabilize Linux and MacOS reverse shells automatically')
		self.parser.add_argument('-v', '--version', action='version', version='%(prog)s version ' + VERSION)
		self.parser.add_argument('--no-pty', action='store_true', help='if this flag is set, no shell stabilization is perform')
		self.parser.add_argument('-P', '--lport', type=int, help='the port used to listen for the reverse shell (Default: 8080)', default=8080)

	def parse_params(self) -> argparse.Namespace:
		return self.parser.parse_args()
