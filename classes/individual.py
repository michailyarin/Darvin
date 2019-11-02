from random import choice
from random import uniform
from random import randint
from sys import float_info
from string import ascii_letters


# Особь (Individual), может нести в себе разные виды генов одновременно.
# Может мутировать случайный ген по команде.

class Individual():
    def __init__(self, genom, gen_int_min, gen_int_max):
        self.genom = genom
        # Keep tuple copy of genome to use in fitness memory
        self.genom_tuple = tuple(genom)
        self.size = len(genom)
        self.gen_int_min = gen_int_min
        self.gen_int_max = gen_int_max
        self.fitness = 0.0

    def mutate(self):
        index_mutated = randint(0, self.size - 1)
        self.mutated = self.genom[index_mutated]

        if type(self.mutated) is float:
            self.genom[index_mutated] = round(uniform(float_info.min, float_info.max), 4)

        elif type(self.mutated) is int:
            self.genom[index_mutated] = randint(self.gen_int_min, self.gen_int_max)
            
        elif type(self.mutated) is str:
            self.genom[index_mutated] = ''.join(choice(ascii_letters) for i in range(len(self.mutated)))
        
        self.genom_tuple = tuple(self.genom)

    def get_genom(self):
        return(self.genom)
