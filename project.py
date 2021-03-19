import sys
#import os
#sys.path.append(os.path.join(os.path.dirname(__file__), "core"))
def start_cli():
    from cli import start
    start()
def start_gui():
    from gui import start
    start()
n = len(sys.argv)
if n > 1:
    for i in range(1, n):
        if sys.argv[i] == "-cli":
            start_cli()
        elif sys.argv[i] == "-gui":
            start_gui()
else:
    print("Please add -gui or -cli")