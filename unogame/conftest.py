import sys, os, pygame
from io import StringIO


def pytest_sessionstart(session):
    unogame_dir = os.path.dirname(__file__)
    sys.path.insert(0, unogame_dir)
    pygame.init()

def pytest_sessionfinish(session, exitstatus):
    pygame.quit()

'''
def pytest_terminal_summary(terminalreporter):
    string_io = StringIO()
    string_io.write("Here's some output\n")
    output = string_io.getvalue()
    terminalreporter.write(output)'''