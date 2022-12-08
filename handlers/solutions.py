import os
import json
from common.classes import Instance


def get_solution_path(instance_id):
    return 'solutions/{}.json'.format(instance_id)


def save_solution(solution, instance: Instance):
    # create folder solutions if doesn't exist
    if not os.path.exists('solutions'):
        os.makedirs('solutions')

    solution["points"] = instance.serialize_customers()

    # create a json file with the instance id saving the solution
    with open(get_solution_path(instance.instance_id), 'w') as f:
        f.write(json.dumps(solution))


def load_solution(instance_id, silent=True):
    path = get_solution_path(instance_id)
    if not os.path.exists(path):
        if not silent:
            print("Solution for instance {} not found".format(instance_id))
        return

    with open(path, 'r') as f:
        return json.loads(f.read())
