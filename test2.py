from ac_algorithms import BackTracking
from csp_network import Network, NotEqualConstraint, Variable


x1 = Variable("x1", {1,4})
x2 = Variable("x2", {4})
x3 = Variable("x3", {1,3})
x4 = Variable("x4", {1,3})

c1 = NotEqualConstraint({"x1", "x2"})
c2 = NotEqualConstraint({"x1", "x3"})
c3 = NotEqualConstraint({"x1", "x4"})
c4 = NotEqualConstraint({"x3", "x4"})

net = Network({x1,x2,x3,x4}, {c1,c2,c3,c4})

# Si vous voulez créer un fichier de test, suivre la syntaxe décrite dans "test2data" et décommentez cette ligne
# net = Network(set(), set(), "test2data")

bt = BackTracking()
solved, sol = bt.solve(net, "lexico")

if solved:
    print("Résolu :")
    for x in sol:
        print(f"{x[0]} -> {x[1]}")
    print(f"Nonmbre d'erreurs : {bt.get_counter()}")
else:
    print("Impossible à résoudre")
