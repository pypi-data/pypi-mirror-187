'''
Module containing utilities for generating, manipulating and verifing
Danish CPR-numbers.

This includes a HTTP server that generates CPR-numbers on demand.
'''

import argparse
from ctypes import memset

from .generator import CPRGenerator
from .server import CPRGeneratorServer
from .cpr_verifier import is_cpr_number, satisfies_mod11


def _get_parser(application: str):
    match application:
        case 'generator':
            parser = argparse.ArgumentParser(
                prog='cpr-gen',
                description="An Unofficial tool for generating Danish CPR-numbers.")
            parser.add_argument('-n',
                                '--numbers',
                                dest='numbers',
                                type=int,
                                default=1,
                                help="the number of CPR-numbers to generate")
            parser.add_argument('--hyphen',
                                dest='hyphen',
                                type=bool,
                                default=False,
                                help="include a hyphen (-) in the generated number(s)")
            parser.add_argument('-m',
                                '--modulus11',
                                dest='mod11',
                                type=bool,
                                default=True,
                                help="enforce modulus-11 rule")

            return parser
        case 'verifier':
            parser = argparse.ArgumentParser(
                prog='cpr-verify',
                description="An Unofficial tool for verifying Danish CPR-numbers.")
            parser.add_argument('cpr_number',
                                metavar='C',
                                type=str,
                                help="the CPR-number to verify")
            parser.add_argument('-m',
                                '--modulus11',
                                dest='mod11',
                                type=bool,
                                default=True,
                                help="check that the CPR-number satisfies the modulus-11 rule")
            return parser
        case _:
            return None


def main_generator():
    parser = _get_parser('generator')
    args = parser.parse_args()

    generator = CPRGenerator()
    cpr_numbers = generator.generate_iter(n=args.numbers,
                                          hyphen=args.hyphen,
                                          mod11=args.mod11)

    for cpr_number in cpr_numbers:
        print(cpr_number)


def main_server():
    server = CPRGeneratorServer()
    server.run()


def main_verifier():
    parser = _get_parser('verifier')
    args = parser.parse_args()

    if args.mod11:
        print(satisfies_mod11(args.cpr_number))
    else:
        print(is_cpr_number(args.cpr_number))


if __name__ == '__main__':
    main_generator()
