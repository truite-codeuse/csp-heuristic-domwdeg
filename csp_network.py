class Variable:

    def __init__(self, name: str, domain: set[int]):
        self._name = name
        self._domain = domain
        self._ac_domain = self._domain.copy() # Will be modified when applying arc consistency

    def remove_from_ac_domain(self, value):
        self._ac_domain.remove(value)
        #print(f"Var {self._name} has removed {value}, domain : {self._ac_domain}")

    def is_empty_domain(self) -> bool:
        return len(self._ac_domain) == 0

    def domain(self) -> set[int]:
        return self._domain

    def ac_domain(self) -> set[int]:
        return self._ac_domain

    def name(self) -> str:
        return self._name


class Constraint:

    def __init__(self, scope: set[str]):
        self._scope = scope
        self._weights = {
            name : 1.0 for name in scope
        }
        self._weight = 1.0

    def get_scope(self) -> set[str]:
        return self._scope

    def is_consistent(self, instances: set[tuple[str,int]]) -> bool:
        return True

    def get_weight(self) -> float:
        return self._weight

    def add_weight(self):
        self._weight += 1

    def get_weight_var(self, var_name: str) -> float:
        if var_name in self._weights:
            return self._weights[var_name]
        else:
            return -1

    def add_weight_var(self, var_name: str, quantity:float):
        if var_name in self._weights:
            self._weights[var_name] += quantity

class EqualConstraint(Constraint):
    def __init__(self, scope: set[str]):
        super(EqualConstraint, self).__init__(scope)

    def is_consistent(self, instances: set[tuple[str, int]]) -> bool:
        if not self.get_scope().issubset({i[0] for i in instances}) :
            return True
        first = None # Will contain the value of instantiated variables
        for x in instances:
            if first is None:
                first = x[1]
            else:
                if x[1] != first:
                   return False
        return True


class NotEqualConstraint(Constraint):
    def __init__(self, scope: set[str]):
        super(NotEqualConstraint, self).__init__(scope)

    def is_consistent(self, instances: set[tuple[str,int]]) -> bool:
        if not self.get_scope().issubset({i[0] for i in instances}):
            return True
        first = None # Will contain the value of instantiated variables
        for x in instances:
            if first is None:
                first = x[1]
            else:
                if x[1] == first:
                    return False
        return True

class LessOrEqualConstraint(Constraint):
    def __init__(self, less: set[str], greater: set[str]):
        super(LessOrEqualConstraint, self).__init__(less.union(greater))
        self._less = less
        self._greater = greater

    def is_consistent(self, instances: set[tuple[str,int]]) -> bool:
        if not self.get_scope().issubset({i[0] for i in instances}):
            return True
        less = {i for i in instances if i[0] in self._less}
        greater = {i for i in instances if i[0] in self._greater}
        for l in less:
            for g in greater:
                if l[1] > g[1]:
                    return False
        return True

class Network:

    def __init__(self, vars: set[Variable], constraints: set, filename=None):
        if filename is not None:
            with open(filename, 'r') as f:
                content = f.readlines()
                content_vars = set()
                content_ctrs = set()
                for line in content:
                    line = line.replace('\n', '')
                    if line[0] == 'x':
                        var_name = line.split("|")[0]
                        domain = {int(d) for d in line.split('|')[1].split(',')}
                        content_vars.add(Variable(var_name, domain))
                    else:
                        ctr_name = line.split('|')[0]
                        var_names = line.split('|')[1].split(',')
                        if ctr_name == "Eq":
                            content_ctrs.add(EqualConstraint(set(var_names)))
                        elif ctr_name == "NEq":
                            content_ctrs.add(NotEqualConstraint(set(var_names)))
                        elif ctr_name == "LEq":
                            content_ctrs.add(LessOrEqualConstraint(set(var_names[0]), set(var_names[1])))
                self._vars = content_vars
                self._constr = content_ctrs
        else:
            self._vars = vars
            self._constr = constraints

    def get_variables(self) -> set[Variable]:
        return self._vars

    def get_constraints(self) -> set[Constraint]:
        return self._constr
