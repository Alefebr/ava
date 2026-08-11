import random
import math


def distance(a, b):
    return math.sqrt(
        (a[0] - b[0]) ** 2 +
        (a[1] - b[1]) ** 2
    )


def route_distance(route, locations):

    total = 0

    for i in range(len(route) - 1):
        total += distance(
            locations[route[i]],
            locations[route[i + 1]]
        )

    # برگشت به نقطه شروع
    total += distance(
        locations[route[-1]],
        locations[route[0]]
    )

    return total


def create_population(size, number_of_locations):

    population = []

    for _ in range(size):

        route = list(range(number_of_locations))

        random.shuffle(route)

        population.append(route)

    return population


def selection(population, locations):

    population.sort(
        key=lambda route: route_distance(
            route,
            locations
        )
    )

    return population[
        :max(2, len(population) // 2)
    ]


def crossover(parent1, parent2):

    length = len(parent1)

    start = random.randint(0, length - 2)

    end = random.randint(
        start + 1,
        length - 1
    )

    child = [None] * length

    child[start:end] = parent1[start:end]

    remaining = [
        x for x in parent2
        if x not in child
    ]

    index = 0

    for i in range(length):

        if child[i] is None:

            child[i] = remaining[index]

            index += 1

    return child


def mutation(route, mutation_rate):

    if random.random() < mutation_rate:

        i, j = random.sample(
            range(len(route)),
            2
        )

        route[i], route[j] = (
            route[j],
            route[i]
        )

    return route


def genetic_algorithm(
    locations,
    population_size=100,
    generations=300,
    mutation_rate=0.1
):

    number_of_locations = len(locations)

    population = create_population(
        population_size,
        number_of_locations
    )

    best_route = None

    best_distance = float("inf")

    # بسیار مهم:
    # ذخیره بهترین فاصله در هر نسل
    history = []

    for generation in range(generations):

        selected = selection(
            population,
            locations
        )

        new_population = selected.copy()

        while len(new_population) < population_size:

            parent1, parent2 = random.sample(
                selected,
                2
            )

            child = crossover(
                parent1,
                parent2
            )

            child = mutation(
                child,
                mutation_rate
            )

            new_population.append(child)

        population = new_population

        current_best = min(
            population,
            key=lambda route:
            route_distance(
                route,
                locations
            )
        )

        current_distance = route_distance(
            current_best,
            locations
        )

        if current_distance < best_distance:

            best_distance = current_distance

            best_route = current_best.copy()

        # ذخیره نتیجه این نسل
        history.append(
            best_distance
        )

    # خیلی مهم:
    # این تابع دقیقاً 3 مقدار برمی‌گرداند
    return best_route, best_distance, history