from csp_network import Constraint, Network, Variable

class AC3:

    def arc_consistency(self, net: Network, all_vars: set[Variable]) -> bool:
        queue = {(x,c) for x in net.get_variables() for c in net.get_constraints() if x.name() in c.get_scope()}
        while len(queue) > 0:
            (var,ctr) = queue.pop()
            appendix = {x_k for x_k in net.get_variables() if x_k.name() != var.name() and x_k.name() in ctr.get_scope()}
            if self.revise(var, ctr, appendix):
                if var.is_empty_domain():
                    future_vars = {i for i in all_vars if i.name() not in {j.name() for j in net.get_variables()}}
                    for future in future_vars:
                        ctr.add_weight()
                        ctr.add_weight_var(future.name(), 1/(len(future_vars)*(1+len(future.ac_domain()))))
                    return False
                else:
                    new_queue = {(x_j,c_j) for x_j in net.get_variables() for c_j in net.get_constraints() if {var.name(), x_j.name()}.issubset(c_j.get_scope()) and var.name() != x_j.name()}
                    queue = queue.union(new_queue)
        return True

    def revise(self, x: Variable, c: Constraint, other_vars: set[Variable]) -> bool:
        change = False
        to_remove = []
        for v in x.ac_domain():
            var_iter = iter(other_vars)
            x_j = next(var_iter, None) # Gets the next variable or None if empty
            if x_j is not None:
                value_iter = iter(x_j.ac_domain())
                v_j = next(value_iter, None)
                if v_j is not None:
                    instance = {(x.name(), v), (x_j.name(), v_j)}
                    while v_j is not None and not c.is_consistent(instance):
                        v_j = next(value_iter, None)
                        instance = {(x.name(), v), (x_j.name(), v_j)}
                if v_j is None:
                    to_remove.append(v)
                    change = True
        for value in to_remove:
            x.remove_from_ac_domain(value)
        return change

class BackTracking:

    def __init__(self):
        self._counter = 0

    def get_counter(self):
        return self._counter

    def solve(self, problem, heuristic: str) -> tuple[bool, set[tuple[str,int]]]:
        return self.backtrack(problem, set(), heuristic)

    def backtrack(self, problem: Network, instance: set[tuple[str,int]], heuristic: str) -> tuple[bool, set[tuple[str,int]]]:
        vars = problem.get_variables().copy()
        if len(instance) == len(vars):
            return True, instance

        instance_vars = {v for v in vars if v.name() in [i[0] for i in instance]}
        instance_ctrs = {c for c in problem.get_constraints() for v in instance_vars if v.name() in c.get_scope()}
        local_net = Network(instance_vars, instance_ctrs)
        ac3 = AC3()
        if not ac3.arc_consistency(local_net, problem.get_variables()):
            return False, instance

        sub_vars = vars.difference(instance_vars)

        #var = self.choose_dom_wdeg_wattez(sub_vars, {c for c in problem.get_constraints() for v in sub_vars if v.name() in c.get_scope()})
        if heuristic == "dom_wdeg":
            var = self.choose_dom_wdeg(sub_vars, {c for c in problem.get_constraints() for v in sub_vars if v.name() in c.get_scope()})
        elif heuristic == "dom_wdeg_wattez":
            var = self.choose_dom_wdeg_wattez(sub_vars, {c for c in problem.get_constraints() for v in sub_vars if v.name() in c.get_scope()})
        else:
            var = self.choose_lexico(sub_vars)

        if var is None:
            return False, instance


        domain = var.ac_domain().copy()
        for value in domain:
            new_inst = instance.union({(var.name(), value)})
            curr_ctr = {c for c in problem.get_constraints() if c.get_scope().issubset({inst[0] for inst in new_inst})}

            coherence = True
            for c in curr_ctr:
                vars_ctr = {x for x in new_inst for y in c.get_scope() if x[0] == y}
                if not c.is_consistent(vars_ctr):
                    coherence = False
                    self._counter += 1
            if coherence:
                is_solved, new_inst = self.backtrack(problem, new_inst, heuristic)
                if is_solved:
                    return True, new_inst

        return False, set()

    def choose_lexico(self, vars: set[Variable]) -> Variable | None:
        names = [var.name() for var in vars]
        names.sort()
        first = names.pop(0)
        chosen = None
        for var in vars:
            if var.name() == first:
                chosen = var
        return chosen


    def choose_dom_wdeg(self, vars: set[Variable], constraints: set) -> Variable:
        dom_wdeg = {}
        for var in vars:
            curr_ctrs = {c for c in constraints if var.name() in c.get_scope()}
            weights = 1
            for c in curr_ctrs:
                weights += c.get_weight()
            dom_wdeg[var.name()] = len(var.ac_domain())/weights
        min_var = None
        min_value = 0
        for x in dom_wdeg:
            if min_var is None:
                min_var = x
                min_value = dom_wdeg[x]
            else:
                if dom_wdeg[x] < min_value:
                    min_var = x
                    min_value = dom_wdeg[x]

        result = [x for x in vars if x.name() == min_var][0]

        return result

    def choose_dom_wdeg_wattez(self, vars: set[Variable], constraints: set) -> Variable:
            dom_wdeg = {}
            for var in vars:
                curr_ctrs = {c for c in constraints if var.name() in c.get_scope()}
                weights = 1
                for c in curr_ctrs:
                    weights += c.get_weight_var(var.name())
                dom_wdeg[var.name()] = len(var.ac_domain())/weights
            min_var = None
            min_value = 0
            for x in dom_wdeg:
                if min_var is None:
                    min_var = x
                    min_value = dom_wdeg[x]
                else:
                    if dom_wdeg[x] < min_value:
                        min_var = x
                        min_value = dom_wdeg[x]

            result = [x for x in vars if x.name() == min_var][0]

            return result
