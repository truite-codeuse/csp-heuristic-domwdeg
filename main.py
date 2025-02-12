from ac_algorithms import BackTracking
from os import listdir
from os.path import isfile, join
import time
from csp_network import Network

num_vars = [10, 15, 20, 25, 30, 35, 40, 45, 50]
heuristics = ["lexico", "dom_wdeg", "dom_wdeg_wattez"]

for num_var in num_vars:
    onlyfiles = [f for f in listdir(f"data/{num_var}") if isfile(join(f"data/{num_var}", f))]
    for heuristic in heuristics:
        with open(f"results/{heuristic}/{num_var}.csv", "w") as f:
            for file in onlyfiles:
                net = Network(set(), set(), f"data/{num_var}/{file}")
                bt = BackTracking()
                start_time = time.time()
                solved, _ = bt.solve(net, heuristic)
                timespan = (time.time() - start_time)
                f.write(f"{timespan},{bt.get_counter()}\n")
