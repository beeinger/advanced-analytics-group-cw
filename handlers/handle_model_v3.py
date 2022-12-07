from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from common.classes import Instance

MAX_TRUCK_TRAVEL_DISTANCE = 3 * 1000  # 3000 km
MAX_TRUCK_TRAVEL_TIME = 24 * 60  # 24 hours in minutes
MAX_WAIT_TIME = 24 * 60  # 24 hours in minutes
LIMIT_NUMBER_OF_CUSTOMERS = 4  # out of 1000
VEHICLE_SPEED = 60 / 60  # 60 km/h in km/min


def create_data_model(instance: Instance):
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = instance.get_distance_matrix(
        LIMIT_NUMBER_OF_CUSTOMERS)
    data['time_matrix'] = instance.get_time_matrix(VEHICLE_SPEED,
                                                   LIMIT_NUMBER_OF_CUSTOMERS)
    data['time_windows'] = instance.get_time_windows(LIMIT_NUMBER_OF_CUSTOMERS)
    data['demands'] = instance.get_demands(LIMIT_NUMBER_OF_CUSTOMERS)
    data['vehicle_capacities'] = instance.get_vehicle_capacities()
    data['num_vehicles'] = instance.number_of_vehicles
    data['depot'] = 0
    print(data['time_matrix'])
    print(data['time_windows'])

    return data

# Logs time

# def print_solution(data, manager, routing, solution):
#     """Prints solution on console."""
#     print(f'Objective: {solution.ObjectiveValue()}')
#     time_dimension = routing.GetDimensionOrDie('Time')
#     total_time = 0
#     for vehicle_id in range(data['num_vehicles']):
#         index = routing.Start(vehicle_id)
#         plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
#         while not routing.IsEnd(index):
#             time_var = time_dimension.CumulVar(index)
#             plan_output += '{0} Time({1},{2}) -> '.format(
#                 manager.IndexToNode(index), solution.Min(time_var),
#                 solution.Max(time_var))
#             index = solution.Value(routing.NextVar(index))
#         time_var = time_dimension.CumulVar(index)
#         plan_output += '{0} Time({1},{2})\n'.format(manager.IndexToNode(index),
#                                                     solution.Min(time_var),
#                                                     solution.Max(time_var))
#         plan_output += 'Time of the route: {}min\n'.format(
#             solution.Min(time_var))
#         if (solution.Min(time_var) > 0):
#             print(plan_output, solution.Min(time_var))
#         total_time += solution.Min(time_var)
#     print('Total time of all routes: {}min'.format(total_time))

# Logs distance


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    total_distance = 0
    total_load = 0
    num_vehicles = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                 route_load)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        if (route_distance > 0):
            print(plan_output)
            num_vehicles += 1
        total_distance += route_distance
        total_load += route_load
    print('Total distance of all routes: {} m'.format(total_distance))
    print('Total load of all routes: {} kg'.format(total_load))
    print('Total number of vehicles used: {} / {}'.format(num_vehicles,
          data['num_vehicles']))


def handle_model(instance: Instance):
    data = create_data_model(instance)

    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Time Windows constraint.
    time = 'Time'
    routing.AddDimension(
        transit_callback_index,
        MAX_WAIT_TIME,  # allow waiting time
        MAX_TRUCK_TRAVEL_TIME,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time)
    time_dimension = routing.GetDimensionOrDie(time)

    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == data['depot']:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])

    # Add time window constraints for each vehicle start node.
    depot_idx = data['depot']
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(
            data['time_windows'][depot_idx][0],
            data['time_windows'][depot_idx][1])

    # Instantiate route start and end times to produce feasible times.
    for i in range(data['num_vehicles']):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i)))
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.End(i)))

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
        print_solution(data, manager, routing, solution)
    else:
        print('No solution found !')
