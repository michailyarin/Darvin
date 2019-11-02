import sys
import json

from random import choice
from random import uniform
from random import randint
from random import randrange

from string import ascii_letters
from classes.fitness import FitnessOut
from classes.individual import Individual


def load_json(file_name):
    with open(file_name, "r") as f:
        content = json.loads(f.read())
    return(content)


def wheel_selection(probability, summ):
    if uniform(0.0, summ) < probability:
        return True
    else:
        return False


def select_pair(population, summ):
    selected = []
    while True:
        for genom_fitness in population:
            if len(selected) < 2:
                if wheel_selection(genom_fitness[1], summ):
                    selected.append(genom_fitness[0])
            else:
                return(selected)


def generate_int_genom(size, minimum, maximum):
    genom = []
    for i in range(size):
        genom.append(randint(minimum, maximum))
    return(genom)


def crossover(a, b):
    crossover_point = randint(1, len(a) - 1)
    return([a[0:crossover_point] + b[crossover_point::],
            b[0:crossover_point] + a[crossover_point::]])


config = load_json("config.json")

population_size = config["population_size"]
genom_size = config["genom_size"]
gen_type = config["gen_type"]
gen_int_min = config["gen_int_min"]
gen_int_max = config["gen_int_max"]
gen_str_length = config["gen_str_length"]
mutation_chance = config["mutation_chance"]
breeding_type = config["breeding_type"]
breeding_pairs_total = config["breeding_pairs_total"]
generations_stop = config["generations_stop"]
fitness_stop = config["fitness_stop"]
time_stop = config["time_stop"]
task_type = config["task_type"]
task_interpreter = config["task_interpreter"]
task_script = config["task_script"]


#
######  init zero generation
############################

population_source = []

for i in range(population_size):
    if gen_type == "int":
        population_source.append(Individual(generate_int_genom(genom_size, gen_int_min, gen_int_max), gen_int_min, gen_int_max))

if task_type == "out":
    fitness = FitnessOut(population_source, task_interpreter, task_script)

# population should live only inside fitness class
del population_source


#
######  start evolution
#######################

for i in range(generations_stop):
    print("GENERATION {}:".format(i))


    # Mutation cycle
    for individual in fitness.population:
        if wheel_selection(mutation_chance, 100):
            individual.mutate()

    fitness.check_fitness()

    # Stop if fitness good enough
    if fitness.best_fitness > fitness_stop:
        print("Fitness reached ({}), genom {}".format(fitness.best_fitness, fitness.best_genom))
        sys.exit()

    print(fitness.best_fitness)
    print(fitness.best_genom)


    # Select individuals for breeding, sort by fitness
    population = []
    for individual in fitness.population:
        population.append([individual.genom, individual.fitness])
    population.sort(key=lambda i: i[1], reverse=1)
    

    # Normalise fitness to the positive plane to use in wheel selection algorithm
    offset = abs(population[-1][1])
    for individual in population:
        individual[1] += offset


    probability_sum = sum([i[1] for i in population])


    # Here we contain already breeded individuals
    breeded = []

    for j in range(breeding_pairs_total):
        # TODO: correct case when parent a and parent b have same genom
        parent_a, parent_b = select_pair(population, probability_sum)


        if breeding_type == "crossover":
            child_a, child_b = crossover(parent_a, parent_b)
        

        breeded += child_a, child_b


    # Embed breeded genomes to old population
    j = len(population) - len(breeded)
    k = 0
    while j < len(population):
        population[j][0] = breeded[k]
        j += 1
        k += 1

    
    # Embed new population to fitness class
    j = 0
    for individual in fitness.population:
        individual.genom = population[j][0]
        j += 1
