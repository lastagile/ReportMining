#!/usr/local/bin/python

import logging
import argparse
import sys
import glob
import os
import inspect
import ys
import xs
from generater import Generater

class GenerateCLI:
    def __init__(self):
        self.inject_verbose_info()

    def inject_verbose_info(self):
        logging.VERBOSE = 15
        logging.verbose = lambda x: logging.log(logging.VERBOSE, x)
        logging.addLevelName(logging.VERBOSE, "VERBOSE")

    def exec_command(self, args):
        if "generate" in args.command:
            print("generate data")
            self.generate(args)
        if "listys" in args.command:
            print("list ys")
            self.list_ys()
        if "listxs" in args.command:
            print("list xs")
            self.list_xs()

    def generate(self, args):
        self.generater = Generater()
        if args.y:
            self.generater.init_y(args.y)
        if args.interval:
            self.generater.init_interval(args.interval)
        if args.x:
            self.generater.init_x(args.x)

        self.generater.run()

    def list_ys(self):
        for filename in glob.glob(os.path.join(ys.__path__[0], "*.py")):
            module_name = os.path.basename(filename).replace('.py', '')
            if not module_name.startswith('_'):
                module = __import__("ys." + module_name)
                test = eval('module.' + module_name)
                for name, obj in inspect.getmembers(test):
                    if inspect.isclass(obj) and 'Y' in (j.__name__ for j in obj.mro()[1:]):
                        if not obj.__module__.split('.')[-1].startswith('_'):
                            print(obj.__name__)
        sys.exit(0)

    def list_xs(self):
        for filename in glob.glob(os.path.join(xs.__path__[0], "*.py")):
            module_name = os.path.basename(filename).replace('.py', '')
            if not module_name.startswith('_'):
                module = __import__("xs." + module_name)
                test = eval('module.' + module_name)
                for name, obj in inspect.getmembers(test):
                    if inspect.isclass(obj) and 'X' in (j.__name__ for j in obj.mro()[1:]):
                        if not obj.__module__.split('.')[-1].startswith('_'):
                            print(obj.__name__)
        sys.exit(0)


    def init_logger(self, args):
        level = logging.DEBUG
        if args.verbose:
            level = logging.VERBOSE
        if args.debug:
            level = logging.DEBUG
        logging.basicConfig(format='%(asctime)s %(filename)s: %(lineno)d: [%(levelname)s] %(message)s',
                            level=level)

    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--debug", help="debug verbose mode",
                            action="store_true")
        parser.add_argument("-v", "--verbose", help="info verbose mode",
                            action="store_true")
        parser.add_argument("-i", "--interval", type=int,
                            help="interval, example: -i 7")
        parser.add_argument("-y", "--y", type=str,
                            help="y, example: -y DayDiffY")
        parser.add_argument("-x", "--x", type=str,
                            help="y, example: -x X1")

        parser.add_argument("command", nargs='*', default="generate", help='verb: "generate|listys|listxs"')
        args = parser.parse_args()
        self.init_logger(args)
        self.exec_command(args)


def main():
    cli = GenerateCLI()
    cli.main()

if __name__ == "__main__": 
    main()                   
