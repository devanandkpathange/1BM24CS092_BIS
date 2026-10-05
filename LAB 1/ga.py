import random
import math

NUM_CUSTOMERS = 8
NUM_VEHICLES = 3
VEHICLE_CAPACITY = 10
POPULATION_SIZE = 100
GENERATIONS = 500
MUTATION_RATE = 0.1

locations = [
    (0, 0),   # Depot
    (2, 3),
    (5, 4),
    (1, 7),
    (6, 8),
    (8, 2),
    (3, 6),
    (7, 5),
    (4, 1)
]

demands = [0, 4, 2, 3, 5, 2, 4, 3, 2]


def distance(a, b):
    return math.sqrt(
        (locations[a][0] - locations[b][0]) ** 2 +
        (locations[a][1] - locations[b][1]) ** 2
    )


def create_individual():
    customers = list(range(1, NUM_CUSTOMERS + 1))
    random.shuffle(customers)

    routes = [[] for _ in range(NUM_VEHICLES)]
    capacities = [0] * NUM_VEHICLES

    for customer in customers:
        possible = [
            i for i in range(NUM_VEHICLES)
            if capacities[i] + demands[customer] <= VEHICLE_CAPACITY
        ]

        if not possible:
            return create_individual()

        vehicle = random.choice(possible)
        routes[vehicle].append(customer)
        capacities[vehicle] += demands[customer]

    return routes


def route_distance(route):
    if not route:
        return 0

    total = distance(0, route[0])

    for i in range(len(route) - 1):
        total += distance(route[i], route[i + 1])

    total += distance(route[-1], 0)

    return total


def fitness(individual):
    total_distance = 0

    for route in individual:
        total_distance += route_distance(route)

    return 1 / (1 + total_distance)


def selection(population):
    tournament = random.sample(population, 5)
    return max(tournament, key=fitness)


def crossover(parent1, parent2):
    p1 = [customer for route in parent1 for customer in route]
    p2 = [customer for route in parent2 for customer in route]

    start, end = sorted(random.sample(range(NUM_CUSTOMERS), 2))

    child = [None] * NUM_CUSTOMERS
    child[start:end] = p1[start:end]

    remaining = [x for x in p2 if x not in child]

    index = 0

    for i in range(NUM_CUSTOMERS):
        if child[i] is None:
            child[i] = remaining[index]
            index += 1

    routes = [[] for _ in range(NUM_VEHICLES)]
    capacities = [0] * NUM_VEHICLES

    for customer in child:
        possible = [
            i for i in range(NUM_VEHICLES)
            if capacities[i] + demands[customer] <= VEHICLE_CAPACITY
        ]

        if not possible:
            return create_individual()

        vehicle = min(possible, key=lambda x: capacities[x])
        routes[vehicle].append(customer)
        capacities[vehicle] += demands[customer]

    return routes


def mutation(individual):
    route1, route2 = random.sample(range(NUM_VEHICLES), 2)

    if not individual[route1] or not individual[route2]:
        return individual

    i = random.randrange(len(individual[route1]))
    j = random.randrange(len(individual[route2]))

    c1 = individual[route1][i]
    c2 = individual[route2][j]

    if (
        sum(demands[x] for x in individual[route1]) - demands[c1] + demands[c2]
        <= VEHICLE_CAPACITY
        and
        sum(demands[x] for x in individual[route2]) - demands[c2] + demands[c1]
        <= VEHICLE_CAPACITY
    ):
        individual[route1][i], individual[route2][j] = c2, c1

    return individual


population = [create_individual() for _ in range(POPULATION_SIZE)]

for generation in range(GENERATIONS):

    new_population = []

    best = max(population, key=fitness)
    new_population.append(best)

    while len(new_population) < POPULATION_SIZE:

        parent1 = selection(population)
        parent2 = selection(population)

        child = crossover(parent1, parent2)

        if random.random() < MUTATION_RATE:
            child = mutation(child)

        new_population.append(child)

    population = new_population

    if generation % 50 == 0:
        best = max(population, key=fitness)
        print(
            "Generation:",
            generation,
            "Distance:",
            round(1 / fitness(best) - 1, 2)
        )


best_solution = max(population, key=fitness)

print("\nBest Routes:")

total = 0

for i, route in enumerate(best_solution):
    d = route_distance(route)
    total += d

    load = sum(demands[x] for x in route)

    print(
        f"Vehicle {i + 1}: "
        f"Depot -> {' -> '.join(map(str, route))} -> Depot"
    )

    print(f"Load: {load}/{VEHICLE_CAPACITY}")
    print(f"Distance: {d:.2f}")

print(f"\nTotal Distance: {total:.2f}")