import random
import math

# ---------------------------------------------------------
# VEHICULAR MONITORING USING PARTICLE SWARM OPTIMIZATION
# ---------------------------------------------------------

# Traffic information for different routes
# [distance in km, traffic level (0-10), average speed km/h]

routes = {
    1: [10, 3, 50],
    2: [8, 7, 35],
    3: [12, 2, 60],
    4: [7, 8, 30],
    5: [9, 4, 45]
}

# ---------------------------------------------------------
# FITNESS FUNCTION
# ---------------------------------------------------------
# Lower fitness = better route
#
# Fitness considers:
#   Distance
#   Traffic congestion
#   Estimated travel time
# ---------------------------------------------------------

def fitness(route):
    distance, traffic, speed = routes[route]

    travel_time = distance / speed

    cost = (
        0.4 * distance +
        0.3 * traffic +
        0.3 * travel_time * 10
    )

    return cost


# ---------------------------------------------------------
# PARTICLE CLASS
# ---------------------------------------------------------

class Particle:

    def __init__(self):
        self.position = random.randint(1, len(routes))
        self.velocity = random.uniform(-1, 1)

        self.best_position = self.position
        self.best_fitness = fitness(self.position)


# ---------------------------------------------------------
# PSO PARAMETERS
# ---------------------------------------------------------

num_particles = 10
iterations = 30

w = 0.7          # Inertia weight
c1 = 1.5         # Personal learning coefficient
c2 = 1.5         # Global learning coefficient


# ---------------------------------------------------------
# INITIALIZE PARTICLES
# ---------------------------------------------------------

particles = [Particle() for _ in range(num_particles)]

global_best_position = particles[0].position
global_best_fitness = particles[0].best_fitness

for particle in particles:

    if particle.best_fitness < global_best_fitness:
        global_best_fitness = particle.best_fitness
        global_best_position = particle.best_position


# ---------------------------------------------------------
# PSO ALGORITHM
# ---------------------------------------------------------

for iteration in range(iterations):

    for particle in particles:

        # Generate random values
        r1 = random.random()
        r2 = random.random()

        # Update velocity
        particle.velocity = (
            w * particle.velocity
            + c1 * r1 * (particle.best_position - particle.position)
            + c2 * r2 * (global_best_position - particle.position)
        )

        # Update position
        new_position = particle.position + particle.velocity

        # Convert to nearest valid route
        new_position = round(new_position)

        # Keep position within available routes
        new_position = max(1, min(len(routes), new_position))

        particle.position = new_position

        # Calculate new fitness
        current_fitness = fitness(particle.position)

        # Update personal best
        if current_fitness < particle.best_fitness:

            particle.best_fitness = current_fitness
            particle.best_position = particle.position

        # Update global best
        if current_fitness < global_best_fitness:

            global_best_fitness = current_fitness
            global_best_position = particle.position


# ---------------------------------------------------------
# VEHICLE MONITORING
# ---------------------------------------------------------

print("\n======================================")
print("     VEHICULAR MONITORING SYSTEM")
print("======================================")

print("\nRoute Information:")
print("--------------------------------------")
print("Route | Distance | Traffic | Speed")
print("--------------------------------------")

for route, data in routes.items():

    distance, traffic, speed = data

    print(
        f"  {route}   |   {distance} km  |"
        f"    {traffic}/10   | {speed} km/h"
    )


# ---------------------------------------------------------
# DISPLAY OPTIMAL ROUTE
# ---------------------------------------------------------

distance, traffic, speed = routes[global_best_position]

travel_time = distance / speed

print("\n======================================")
print("       PSO OPTIMIZATION RESULT")
print("======================================")

print("Optimal Route       :", global_best_position)
print("Distance            :", distance, "km")
print("Traffic Level       :", traffic, "/10")
print("Average Speed       :", speed, "km/h")
print("Estimated Time      :", round(travel_time * 60, 2), "minutes")
print("Optimization Score  :", round(global_best_fitness, 3))

print("\nRecommendation:")
print(
    f"Vehicle should use Route {global_best_position} "
    "for efficient travel."
)