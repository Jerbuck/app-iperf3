#!/usr/bin/env python
import subprocess
import atexit

class ArgParser:

    app_name = None
    command_line = None

    def __init__(self, app_name, command_line):
        self.app_name = app_name
        self.command_line = command_line
        atexit.register(self._clean_up)

    def _clean_up(self):
        print(f'\nStopping {self.app_name} process...')

    def _get_input(self):
        args = input(f'\nEnter {self.app_name} arguments: ')
        return args

    def _call_process(self, args):
        print(f'\nPassing command-line arguments to {self.app_name}: ' + args)
        subprocess.run([self.command_line, args])

    def run(self):
        try:
            args = self._get_input()
            self._call_process(args)
        except KeyboardInterrupt:
            self._clean_up()

        self.run()

if __name__=="__main__":
    arg_parser = ArgParser('iperf3', 'iperf3')
    arg_parser.run()