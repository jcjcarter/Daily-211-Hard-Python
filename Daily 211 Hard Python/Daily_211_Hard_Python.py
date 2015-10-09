import random
import copy

class Solution:
    def __init__(self, treats, fitness=-1000):
        self.solution = copy.copy(treats)
        self.fitness = fitness

    def clone(self):
        return Solution(self.solution, fitness = self.fitness)

    def recalc(self):
        f = 0
        for i in range(len(self.solution)):
            prev = self.solution[1] if i == 0 else self.solution[i-1]
            next = self.solution[i-1] if i == len(self.solution)-1 else self.solution[i+1]
            me = self.solution[i]
            if me < next and me < prev:
                f -= 1
            elif me > next and me > prev:
                f += 1
        self.fitness = f

    def __str__(self):        
        return "%d : %s / ck %d" % (self.fitness, self.solution, sum(self.solution))

def ga(treats, population=40, gens=1000):
    # calc how many of each treat we have
    treat_map = {}
    for t in treats:
        treat_map[t] = treat_map.get(t, 0) + 1

    # Initialization, Evaluation 
    pool = [Solution(treats) for x in range(population)]
    for s in pool:
        random.shuffle(s.solution)
        s.recalc()

    leet = None
    while gens >= 0:
        # Selection 
        # Half of the population will be overwritten
        pool.sort(key = lambda x : -x.fitness)
        if leet:
            pool[-1] = leet.clone()
        if not leet or leet.fitness < pool[0].fitness:
            leet = pool[0].clone()    
        if gens == 0:
            break
        gens -= 1

        for i in range(population / 2, population):        
            p1, p2 = random.randint(0, population / 2 - 1), random.randint(0, population / 2 - 1)
            crossover_treat_map = copy.copy(treat_map)

            for g in range(len(treats)):
                # pick random treat from either parent
                p = pool[p1 if random.randint(1, 2) == 1 else p2]
                if p.solution[g] in crossover_treat_map:
                    k = p.solution[g]
                else:
                    k = random.choice(crossover_treat_map.keys())

                # or any
                crossover_treat_map[k] -= 1
                if crossover_treat_map[k] == 0:
                    del crossover_treat_map[k]
                pool[i].solution[g] = k

        # mutation    
        for p in pool:
            c = max(0, random.randint(-5, 5))
            while c > 0:
                i, j = random.randint(0, len(treats)-1), random.randint(0, len(treats)-1)
                p.solution[i], p.solution[j] = p.solution[j], p.solution[i]
                c -= 1
            p.recalc()
    return leet

def run(s):
    res = ga(list(map(int, s.split())))
    print("%s:\n\t%s\n"%(s,res))


if __name__ == "__main__":
    random.seed(20150424)
    run("1 2 2 3 3 3 4")
    run("1 1 2 3 3 3 3 4 5 5")
    run("1 1 2 2 3 4 4 5 5 5 6 6")
    run("1 1 2 2 2 2 2 2 3 4 4 4 5 5 5 6 6 6 7 7 8 8 9 9 9 9 9 9 9 9")