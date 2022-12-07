import argparse


def handle_inline_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--benchmark", dest="benchmark",
                        action='store_true', default=False, help="Should benchmark be run?")
    parser.add_argument("-v", "--version", dest="version", default=3,
                        help="Which version of the model should be run?", type=int)
    return parser.parse_args()
