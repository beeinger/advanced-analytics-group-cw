import math


class Customer:
    customer_id: int
    x: int
    y: int
    demand: int
    ready_time: int
    due_date: int
    service_time: int

    def serialize(self):
        return {
            "customer_id": self.customer_id,
            "x": self.x,
            "y": self.y,
            "demand": self.demand,
            "ready_time": self.ready_time,
            "due_date": self.due_date,
            "service_time": self.service_time
        }

    def distance_to(self, customer: "Customer"):
        # return abs(self.x - customer.x) + abs(self.y - customer.y)
        return math.ceil(math.sqrt((self.x - customer.x)**2 + (self.y - customer.y)**2))

    def __init__(self, customer: dict):
        self.customer_id = customer["customer_id"]
        self.x = customer["x"]
        self.y = customer["y"]
        self.demand = customer["demand"]

        # 773/100 => 7.73 * 60 => 463.8
        # self.ready_time = math.ceil(customer["ready_time"]/100*60)
        # self.due_date = math.ceil(customer["due_date"]/100*60)

        self.ready_time = customer["ready_time"]
        self.due_date = customer["due_date"]

        self.service_time = customer["service_time"]


class Instance:
    instance_id: str
    number_of_vehicles: int
    total_capacity: int
    customers: list[Customer]

    def serialize_customers(self):
        return [customer.serialize() for customer in self.customers]

    def serialize(self):
        return {
            "instance_id": self.instance_id,
            "number_of_vehicles": self.number_of_vehicles,
            "total_capacity": self.total_capacity,
            "customers": self.serialize_customers()
        }

    def get_time_windows(self, limit: int = -1):
        length = len(self.customers)
        if (limit > 1 and limit < length):
            length = limit

        # [(0, 10), (20, 40)]
        time_windows: list[tuple[int, int]] = []
        for i in range(length):
            time_windows.append(
                (self.customers[i].ready_time, self.customers[i].due_date))
        return time_windows

    def get_time_matrix(self, vehicle_speed: float, limit: int = -1):
        distance_matrix = self.get_distance_matrix(limit)
        time_matrix: list[list[int]] = []
        for i in range(len(distance_matrix)):
            time_matrix.append([])
            for j in range(len(distance_matrix[i])):
                time_matrix[i].append(
                    math.ceil(distance_matrix[i][j] / vehicle_speed))
        return time_matrix

    def get_distance_matrix(self, limit: int = -1):
        length = len(self.customers)
        if (limit > 1 and limit < length):
            length = limit

        # [[1, 1], [1, 1]]
        # [[0, 20, 30], [20, 0, 40], [30, 40, 0]]
        distance_matrix: list[list[int]] = []
        for i in range(length):
            distance_matrix.append([])
            for j in range(length):
                distance_matrix[i].append(
                    self.customers[i].distance_to(self.customers[j]))
        return distance_matrix

    def get_demands(self, limit: int = -1):
        # Limiter
        length = len(self.customers)
        if (limit > 1 and limit < length):
            length = limit

        # [30, 40, 20, 10]
        demands: list[int] = []
        for i in range(length):
            demands.append(self.customers[i].demand)
        return demands

    def get_vehicle_capacities(self):
        # [20, 30, 40]
        # 200 -> [200] * number_of_vehicles => [200, 200, 200]
        return [self.total_capacity] * self.number_of_vehicles

    # initialize the instance
    def __init__(self, instance: dict):
        self.instance_id = instance["instance_id"]
        self.number_of_vehicles = instance["number_of_vehicles"]
        self.total_capacity = instance["total_capacity"]
        self.customers = instance["customers"]
