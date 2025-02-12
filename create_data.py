import random
from csp_network import Network
from ac_algorithms import BackTracking

def create_problem(nbr_var, nbr_ctrs, domains, filename):
    with open(filename, 'w') as f:
        vars = [i for i in range(nbr_var)]
        ctrs = ["NEq", "LEq"]
        curr_ctrs = {
            x : [] for x in vars
        }
        for i in vars:
            curr_dom = []
            for z in list({random.choice(domains) for d in range(len(domains)//2)}):
                if len(curr_dom) == 0:
                    curr_dom.append(z)
                elif random.random() >= 0.5:
                    curr_dom.append(z)
            curr_dom.sort()
            f.write(f"x{i}|{str(curr_dom).replace('[', '').replace(']','').replace(' ', '')}\n")
        for j in range(nbr_ctrs):
            first = random.choice(vars)
            second = random.choice(vars)
            i = 0
            while first == second or (second in curr_ctrs[first] or first in curr_ctrs[second]) and i < 10:
                second = random.choice(vars)
                i += 1
            if not (first == second or (second in curr_ctrs[first] or first in curr_ctrs[second])):
                ctr_type = random.choice(ctrs)
                f.write(f"{ctr_type}|x{first},x{second}\n")

num_vars = 10
num_ctrs = 10
for i in [0, 5, 10, 15, 20, 25, 30, 35, 40]:
    print(f"{num_vars + i}")
    for j in range(50):
        solved = False
        count = 0
        while not solved or count == 0:
            create_problem(num_vars + i, num_ctrs + i, [k + 1 for k in range(num_vars + i)], f"data/{num_vars+i}/prob{j}")
            net = Network(set(), set(), f"data/{num_vars+i}/prob{j}")
            bt = BackTracking()
            solved, vars = bt.solve(net, "lexico")
            count = bt.get_counter()
