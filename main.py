from handlers.handle_instances import get_all_instances
from handlers.handle_inline_args import handle_inline_args
from handlers.handle_model_v3 import handle_model as handle_model_v3
from handlers.handle_model_v2 import handle_model as handle_model_v2
from handlers.handle_model_v1 import handle_model as handle_model_v1
import timeit


def main(version: int):
    instances = get_all_instances()
    print("Number of instances found: " + str(len(instances)))

    print("Running version " + str(version) + " of the model\n")
    if (version == 3):
        handle_model_v3(instances[0])
    elif (version == 2):
        handle_model_v2(instances[0])
    elif (version == 1):
        handle_model_v1(instances[0])


if __name__ == "__main__":
    args = handle_inline_args()

    if (args.benchmark):
        seconds = timeit.timeit(
            "main("+str(args.version)+")", setup="from __main__ import main", number=1)
        print("Time elapsed: " + str(seconds) + " seconds")
    else:
        main(args.version)
