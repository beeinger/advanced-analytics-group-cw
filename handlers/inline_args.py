import argparse


def handle_inline_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--benchmark", dest="benchmark",
                        action='store_true', default=False, help="Should benchmark be run?")
    parser.add_argument("-a", "--all", dest="all",
                        action='store_true', default=False, help="Should all instances be run?")
    parser.add_argument("-r", "--routes", dest="routes",
                        action='store_true', default=False, help="Should routes be displayed?")
    parser.add_argument("-d", "--draw", dest="draw",
                        action='store_true', default=False, help="Should the solutions be drawn?")
    parser.add_argument("-v", "--version", dest="version", default=3,
                        help="Which version of the model should be run?", type=int)
    parser.add_argument("-i", "--instance", dest="instance", default=0,
                        help="Which instance should be run (index of the instance 0-59)?", type=int)

    return parser.parse_args()
