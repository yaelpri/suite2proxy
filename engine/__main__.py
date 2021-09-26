
try:
    from engine import Engine
except ModuleNotFoundError:
    from sys import path
    from os.path import dirname, abspath, join
    path.append(abspath(join(dirname(__file__), '..', '..')))
finally:
    from engine import Engine


'__main__' == __name__ and Engine.sanity()
