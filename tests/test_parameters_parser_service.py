import unittest, sys
import unittest.mock
from argparse import Namespace
from io import StringIO
from netpwn.services import ParametersParserService


class ParametersParserServiceTest(unittest.TestCase):
    def test_arguments_parse(self):
        sys.argv = ['./netpawn.py', '--lport', '8000']
        parameterParserService = ParametersParserService()

        with unittest.mock.patch('sys.stderr', new=StringIO()):
            try:
                params = parameterParserService.parse_params()
                self.assertEqual(params, Namespace(lport=8000, no_pty=False))
            except SystemExit:
                raise Exception('Wrong parameters!')

    def test_arguments_parse_default_port(self):
        sys.argv = ['./netpawn.py']
        parameterParserService = ParametersParserService()

        with unittest.mock.patch('sys.stderr', new=StringIO()):
            try:
                params = parameterParserService.parse_params()
                self.assertEqual(params, Namespace(lport=8080, no_pty=False))
            except SystemExit:
                raise Exception('Wrong parameters!')

    def test_arguments_parse_error(self):
        sys.argv = ['./netpawn.py', '--lport']
        parameterParserService = ParametersParserService()

        with unittest.mock.patch('sys.stderr', new=StringIO()) as fakeOutput:
            try:
                parameterParserService.parse_params()
            except SystemExit:
                self.assertTrue('error: argument -P/--lport: expected one argument' in fakeOutput.getvalue().strip())


if __name__ == '__main__':
    unittest.main()
