from ortools.linear_solver import pywraplp
from common.classes import Instance


def handle_model(instance: Instance):
    # define the solver and the MIP model
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print('Could not create solver SCIP')
        exit(1)

    infinity = solver.infinity()

    # -- Depot --
    depot_x = solver.IntVar(0.0, infinity, 'depot_x')
    depot_y = solver.IntVar(0.0, infinity, 'depot_y')
    number_of_vehicles = solver.IntVar(0.0, infinity, 'number_of_vehicles')
    total_capacity = solver.IntVar(0.0, infinity, 'total_capacity')

    total_demand = 0

    # -- Customer --
    customer_x = {}
    customer_y = {}
    demand = {}
    ready_time = {}
    due_date = {}
    service_time = {}

    for i in range(len(instance.customers)):
        customer_x[i] = solver.IntVar(0.0, infinity, 'customer_x[%i]' % i)
        customer_y[i] = solver.IntVar(0.0, infinity, 'customer_y[%i]' % i)
        demand[i] = solver.IntVar(0.0, infinity, 'demand[%i]' % i)
        ready_time[i] = solver.IntVar(0.0, infinity, 'ready_time[%i]' % i)
        due_date[i] = solver.IntVar(0.0, infinity, 'due_date[%i]' % i)
        service_time[i] = solver.IntVar(0.0, infinity, 'service_time[%i]' % i)

    # solver.Add()
    print('Number of variables =', solver.NumVariables())


# minimize TotalDeliveryTime

# subject to:
#     TotalDeliveryTime = sum(DeliveryTime[i] for i in Deliveries)

#     DeliveryTime[i] = Distance[i] / Speed[i] + LoadingTime[i] + UnloadingTime[i]
#     for all i in Deliveries

#     Distance[i] = sqrt((DeliveryLat[i] - DepoLat)^2 + (DeliveryLon[i] - DepoLon)^2)
#     for all i in Deliveries

#     Speed[i] <= TruckSpeed
#     for all i in Trucks

#     TimeWindowStart[i] <= ArrivalTime[i] <= TimeWindowEnd[i]
#     for all i in Deliveries

#     LoadingTime[i] <= MaxLoadingTime
#     for all i in Deliveries

#     UnloadingTime[i] <= MaxUnloadingTime
#     for all i in Deliveries

#     sum(TruckLoad[j,i] for j in Deliveries) <= 1
#     for all i in Trucks

#     sum(PackageCount[i] * TruckLoad[j,i] for j in Deliveries) <= Truck
