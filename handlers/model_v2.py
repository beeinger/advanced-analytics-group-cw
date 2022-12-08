from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from common.classes import Instance
import sys
import builtins

# there is a 1000 customers
# we limit the number of customers to 20 for testing speed
# It's basically a sample subset of the customers
LIMIT_NUMBER_OF_CUSTOMERS = -1
MAX_TRUCK_TRAVEL_DISTANCE = sys.maxsize  # 3000 km


def create_data_model(instance: Instance):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = instance.get_distance_matrix(
        LIMIT_NUMBER_OF_CUSTOMERS)
    data['demands'] = instance.get_demands(LIMIT_NUMBER_OF_CUSTOMERS)
    data['vehicle_capacities'] = instance.get_vehicle_capacities()
    data['num_vehicles'] = instance.number_of_vehicles
    data['depot'] = 0
    return data


def print_solution(data, manager, routing, solution, routes, instance):
    def print(*objs, **kwargs):
        builtins.print("[{}] ".format(
            instance.instance_id), *objs, **kwargs)

    """Prints solution on console."""
    # print(f'Objective: {solution.ObjectiveValue()}')
    total_distance = 0
    total_load = 0
    num_vehicles = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = ""
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            if (node_index != data['depot']):
                plan_output += ' {0}'.format(node_index, route_load)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        if (route_distance > 0):
            num_vehicles += 1
            if (routes):
                print('Route {}:'.format(num_vehicles) + plan_output + '; load: {1}kg; distance: {2}m\n'.format(
                    manager.IndexToNode(index), route_load, route_distance))
        total_distance += route_distance
        total_load += route_load
    print('Total distance of all routes: {} m'.format(total_distance))
    print('Total load of all routes: {} kg'.format(total_load))
    print('Total number of vehicles used: {} / {}'.format(num_vehicles,
          data['num_vehicles']))


def handle_model(instance: Instance, routes: bool):
    data = create_data_model(instance)

    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    # -- Distance --
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        MAX_TRUCK_TRAVEL_DISTANCE,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    #  -- Demand --
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution, routes, instance)
    else:
        print('No solution found !')
