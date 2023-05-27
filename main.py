from random import randint
import random

MAX = 2147483647
START = 0
popSize = 100
mutation_rate = 3
max_gens = 10
threshhold = 600
selection_size = 5

nodes = 7
pos = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6}
GENES = "ABCDEFG"
graph = [[0, 90, MAX, 300, 140, MAX, 220],
         [100, 0, 80, MAX, MAX, 300, 150],
         [MAX, 340, 0, 40, 250, MAX, MAX],
         [360, MAX, 240, 0, 80, 170, MAX],
         [450, 40, MAX, MAX, 0, MAX, 100],
         [70, MAX, 330, 160, MAX, 0, 110],
         [MAX, 320, 140, 90, 280, 190, 0]]


class chromo:
    def __init__(self, _path, _fitness):
        self.path = _path
        self.fitness = _fitness

def fitness(chromo):
    fitness = 0
    
    for r in range(len(chromo)-1):
        g = chromo[r]
        k = chromo[r+1]
        row = pos[g]
        col = pos[k]
        if graph[row][col] == MAX:
            return MAX
        else:
            fitness += graph[row][col]

    return fitness

def apartheid(population, number):
    new = []

    while (len(new) < number):
        index = randint(0, len(population)-1)

        if population[index] not in new:
            new.append(population[index])

    return new




# function to select fittest population
def tournament_selection(population, tournament_size):
    """
    Selects the fittest individuals from the population using tournament selection
    """
    fittest = []
    for i in range(len(population)):
        tournament = random.sample(population, tournament_size)
        fittest_individual = min(tournament, key=lambda x: x.fitness)
        fittest.append(fittest_individual)
        fittest.sort(key=lambda x: x.fitness)
    return fittest


def order_crossover(parent1, parent2):
    """
    Applies order crossover (OX) to two parent individuals and returns two offspring individuals
    """
    n = len(parent1.path)
    p1_path = list(parent1.path[0:len(parent1.path)-1])
    p2_path = list(parent2.path[0:len(parent2.path)-1])
    a = random.randint(0, n-1)
    b = random.randint(0, n-1)

    new_offspring1 = []
    new_offspring2 = []

    if a > b:
        a, b = b, a


    new_offspring1[a:b] = p1_path[a:b]

    j = b
    k = b

    for i in range(0, nodes):
        if i < b:
            new_offspring2[i] = p2_path[i]
        
        if p2_path[i] not in new_offspring1:
            new_offspring1[j] = p2_path[i]
            j+=1

    for i in range(0, nodes):
        if p1_path[i] not in new_offspring2:
            new_offspring2[j] = p1_path[i]
            k+=1

    new_offspring1.extend(new_offspring1[0])
    path1 = "".join(new_offspring1)
    new_genome1 = chromo(path1, fitness(path1))

    new_offspring2.extend(new_offspring2[0])
    path2 = "".join(new_offspring2)
    new_genome2 = chromo(path2, fitness(path2))
    
    return new_genome1, new_genome2

def mutation(individual):
    """
    Applies mutation to an individual by swapping two cities with a certain probability (mutation_rate)
    """
    positions = []
    mutated = []
    n = len(individual.path)

    for i in range(len(individual.path)-1):
        mutated.extend(individual.path[i])

    for i in range(len(mutated)):
        positions.append(i)

    for i in range(mutation_rate):
        pos1, pos2 = random.sample(positions, 2)
        mutated[pos1], mutated[pos2] = mutated[pos2], mutated[pos1]
    

    mutated.extend(mutated[0])
    path = "".join(mutated)
    mutated_genome = chromo(path, fitness(path))

    return mutated_genome

def generate_path(genes):
    start = random.choice(genes)

    remaining = [i for i in genes if i != start]
    random.shuffle(remaining)
    end = start
    path = [start]

    for i in range(len(remaining)):
        if i == 7:
            break
        ver = remaining[i]
        if ver != end:
            path.append(ver)
    
    path.append(end)

    return ''.join(path)

def make_pop(population, genes):
    
    first_pop = []

    for i in range(population):
        path = generate_path(GENES)
        chromosom = chromo(path, fitness(path))
        first_pop.append(chromosom)
    
    return first_pop

def pop_score(population):

    score = 0

    for i in population:
        score =+ i.fitness
    return score


def create_offspring(fittest):
        new_gen = []
        new_parents = []

        for i in range(len(fittest)):
            new_parents.append(i)

        children_size = popSize - len(fittest)

        for i in range(children_size):
            p1, p2 = random.sample(new_parents, 2)
            new_offspring1, new_offspring2 = order_crossover(fittest[p1], fittest[p2])
            mutated1 = mutation(new_offspring1)
            mutated2 = mutation(new_offspring2)
            new_gen.append(mutated1)
            new_gen.append(mutated2)
        
        for i in range(len(fittest)):
            mutated = mutation(fittest[i])
            new_gen.append(mutated)

        print("\nNew Generation:\nPATH\t\tFITNESS")
        for i in new_gen:
            print(i.path,"\t",i.fitness)

        return new_gen

def main():
    population = make_pop(popSize, GENES)

    score = pop_score(population)

    gen = 1

    while (gen <= max_gens) and (score > threshhold):
        print("\t\nGeneration No: ", gen)
        print("Score: ", score)

        fittest = tournament_selection(population, selection_size)

        print("\nFittest:\n")
        print("Path\t\tFitness")

        for i in fittest:
            print(i.path,"\t", i.fitness)

        population = create_offspring(fittest)
        score = pop_score(population)
        gen += 1

    fittest = tournament_selection(population, selection_size)

    print("\nFittest:\n")
    print("Path\t\tFitness")

    for i in fittest:
        print(i.path,"\t", i.fitness)
    print("Shortest Distance Found:", fittest[0].path, fittest[0].fitness)


if __name__ == "__main__":
    main()
