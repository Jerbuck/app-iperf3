#!/usr/bin/env python
import subprocess
import atexit

class ArgParser:

    app_name = None
    command_line = None

    def __init__(self, app_name, command_line):
        self.app_name = app_name
        self.command_line = command_line
        atexit.register(self.__clean_up)

    def __clean_up(self):
        print(f'\nStopping {self.app_name} process...')

    def __get_input(self):
        args = input(f'\nEnter {self.app_name} arguments: ')
        return args

    def __call_process(self, args):
        print(f'\nPassing command-line arguments to {self.app_name}: ' + args)
        subprocess.run([self.command_line, args])

    def run(self):
        try:
            args = self.__get_input()
            self.__call_process(args)
        except KeyboardInterrupt:
            self.__clean_up()
        self.run()

if __name__=="__main__":
    arg_parser = ArgParser('iperf3', 'iperf3')
    arg_parser.run()