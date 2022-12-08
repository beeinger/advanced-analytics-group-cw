import timeit


from multiprocessing import Process

from handlers.handle_instances import get_all_instances
from handlers.handle_inline_args import handle_inline_args

from common.classes import Instance

from handlers.handle_model_v3 import handle_model as handle_model_v3
from handlers.handle_model_v2 import handle_model as handle_model_v2
from handlers.handle_model_v1 import handle_model as handle_model_v1


def run_instance(instance: Instance, version: int, routes: bool):
    if (version == 3):
        handle_model_v3(instance, routes)
    elif (version == 2):
        handle_model_v2(instance, routes)
    elif (version == 1):
        handle_model_v1(instance, routes)


def main(version: int, index: int, all: bool, routes: bool):
    instances = get_all_instances()
    print("Number of instances found: " + str(len(instances)))
    print("Running version " + str(version) + " of the model\n")

    if (all):
        all_processes = []
        for instance in instances:
            p = Process(target=run_instance, args=(instance, version, routes))
            p.start()
            all_processes.append(p)
        for p in all_processes:
            p.join()
    else:
        instance = instances[index]
        run_instance(instance, version, routes)


if __name__ == "__main__":
    args = handle_inline_args()

    if (args.benchmark):
        seconds = timeit.timeit(
            "main({0}, {1}, {2}, {3})".format(args.version, args.instance, args.all, args.routes), setup="from __main__ import main", number=1)
        print("Time elapsed: " + str(seconds) + " seconds")
    else:
        main(args.version, args.instance, args.all, args.routes)
