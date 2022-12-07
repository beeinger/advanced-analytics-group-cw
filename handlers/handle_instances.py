import os

from common.classes import Instance, Customer


def get_instance(path: str):
    global instance_id
    global number_of_vehicles
    global total_capacity
    customers = []

    with open(path) as f:
        lines = f.readlines()
        instance_id = lines[0].replace("\n", "").strip()

        tmp = lines[4].replace("\n", "").split()
        number_of_vehicles = int(tmp[0])
        total_capacity = int(tmp[1])

        tmp = lines[9:]
        for i in range(len(tmp)):
            raw_customer = tmp[i].replace("\n", "").split()
            customer = Customer({
                "customer_id": int(raw_customer[0]),
                "x": int(raw_customer[1]),
                "y": int(raw_customer[2]),
                "demand": int(raw_customer[3]),
                "ready_time": int(raw_customer[4]),
                "due_date": int(raw_customer[5]),
                "service_time": int(raw_customer[6])
            })
            customers.append(customer)

    return Instance({
        "instance_id": instance_id,
        "number_of_vehicles": number_of_vehicles,
        "total_capacity": total_capacity,
        # ? First "customer" is actually the depot in our data
        "customers": customers,
    })


def get_all_instances():
    instances: list[Instance] = []
    for file in os.listdir("./instances"):
        if file.endswith(".TXT"):
            instances.append(get_instance("./instances/" + file))
    return instances
