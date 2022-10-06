# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
from typing import Callable


class A:
    def a(self):
        pass

    def set_a(self, func: Callable):
        self.a = func

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(json.loads(b'{"hello": 1}'))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
