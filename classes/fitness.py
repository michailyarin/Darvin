import json
from subprocess import Popen, PIPE


# FitnessTask вызывает внешний скрипт для проверки выживаемости.
# Скрипт должен принимать гены как аргумент-строку в формате [1, 3, 5]
# По окончанию работы скрипт возвращает уровень выживаемости (больше = лучше)


def execute(command):
    res, err = Popen(command, shell = True, stdout = PIPE).communicate()
    return(res.decode())


# Pack json depend on var type
def pack_json(content):
    packed = []
    for element in content:
        if type(element) is str:
            packed.append('{}{}{}'.format("\"\'", element, "\'\""))
        else:
            packed.append(element)
    return(json.dumps(packed))


# FitnessOut вызывает внешний скрипт для проверки выживаемости.
# Скрипт должен принимать гены как аргумент-строку в формате [1, 3, 5]
# По окончанию работы скрипт возвращает уровень выживаемости (больше = лучше)

class FitnessOut():
    def __init__(self, population, interpreter="python3", script="test.py"):
        self.population = population
        self.interpreter = interpreter
        self.script = script

        # Infinite short + long term memory 
        self.all_term_memory = {}
        # Short term memory
        self.short_term_memory = {}

        # Best individual
        self.best_fitness = 0.0
        self.best_genom = []


    def check_fitness(self):

        # Forget on the start
        self.short_term_memory.clear()

        for individual in self.population:

            #  TODO: check speed
            #if self.long_term_memory.__contains__(individual.genom):

            #  TODO: check speed without all_term_memory
            if individual.genom_tuple in self.short_term_memory:
                individual.fitness = self.short_term_memory[individual.genom_tuple]

            else:
                if individual.genom_tuple in self.all_term_memory:
                    individual.fitness = self.all_term_memory[individual.genom_tuple]

                else:
                    self.to_execute = '{} {} "{}"'.format(self.interpreter, self.script, pack_json(individual.genom))
                    self.current_fitness = float(execute(self.to_execute))

                    individual.fitness = self.current_fitness

                    # Save everything to memory
                    self.short_term_memory[individual.genom_tuple] = self.current_fitness
                    self.all_term_memory[individual.genom_tuple] = self.current_fitness

                    # Remember best genome and fitness
                    if individual.fitness > self.best_fitness:
                        self.best_fitness = individual.fitness
                        self.best_genom = individual.genom
