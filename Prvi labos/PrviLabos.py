from queue import Queue

from heapdict import heapdict

prosSt = {}
f1 = open("ai.txt", "r")
prijelazi = 0
x = 0
for i in f1.readlines():
    x += 1
    djeca = {}
    if '#' in i:
        continue
    if x == 2:
        ishodiste = i.strip()
        continue
    if x == 3:
        odrediste = i.strip().split(" ")
        x = 8
        continue
    if not i:
        continue
    p = i.strip().split(": ")
    if len(p) > 1:
        buD = p[1].split(" ")
        for l in buD:
            dij = l.strip().split(",")
            djeca.update({dij[0]: dij[1]})
            prijelazi += 1
        m = p[0]
    else:
        m = p[0].replace(":", '')
        djeca.update({'no': 0})
    prosSt.update({m: djeca})

f2 = open("ai_fail.txt", "r")

lakse = f2.read().split("\n")
heuristika = heapdict()

for i in lakse:
    if not i:
        continue
    k = i.split(": ")
    if len(k) < 2:
        heuristika.update(({k[0]: 0}))
    else:
        heuristika.update({k[0]: k[1]})

print("Start state: " + ishodiste)
print("End state(s): ", end='')
print(odrediste)
print("State space size: " + str(len(prosSt.keys())))
print("Total transitions: " + str(prijelazi))
print()

#pretrazivanje u sirinu
def trazenjePuta(n, succ, closed):
    roditelji = []
    m = n
    for i in reversed(closed):
        if m in succ.get(i):
            roditelji.append(i)
            m = i
    return roditelji


def breadthFirstSearch(s0, succ, goal):
    print("Running bfs:")
    open = Queue()
    closed = {}
    open.put(s0)
    while open._qsize() != 0:
        n = open.get()
        if n in closed:
            continue
        else:
            closed.update({n: 0})
        if n in goal:
            put = trazenjePuta(n, prosSt, closed)
            print("States visited = " + str(len(closed)))
            print("Found path of lenght " + str(len(put) + 1))
            for i in reversed(put):
                print(i + " =>")
            print(n + "\n")
            return n
        ekspandirano = succ.get(n)
        for m in ekspandirano:
            insertBack(m, open)

    return "fail"


def insertBack(m, open):
    open.put(m)


stanje = breadthFirstSearch(ishodiste, prosSt, odrediste)



# algoritam koj se koristi za pronalazak puta u ucs-u i astar-u
def trazenjePutaCijena(n, succ, closed):
    roditelji = []
    m = n[0]
    for i in reversed(closed):
        lista = succ.get(i)
        if m in lista:
            if float(closed.get(m)) - float(lista.get(m)) == float(closed.get(i)):
                roditelji.append(i)
                m = i
    return roditelji

#pretrazivanje po jednolikoj cijeni
def uniformCostSearch(s0, succ, goal, zaopt):
    open = heapdict()
    closed = {}
    open.update({s0: 0})
    k = 0
    while len(open) != 0:

        n = open.popitem()

        if n[0] in closed:
            if n[1] > closed.get(n[0]):
                continue

        closed.update({n[0]: n[1]})

        if n[0] in goal:
            if zaopt == 0:
                put = trazenjePutaCijena(n, prosSt, closed)
                print("Running ucs:")
                print("States visited = " + str(len(closed)))
                print("Found path of lenght " + str(len(put) + 1) + " total cost of " + str(n[1]))
                for i in reversed(put):
                    print(i + " =>")

                print(n[0] + "\n")
            return n[1]

        ekspandirano = succ.get(n[0])
        f = n[1]

        for m in ekspandirano:
            if m == 'no':
                continue
            g = f + float(ekspandirano.get(m))
            insertSortedBy(g, m, open)

    return "fail"


def insertSortedBy(g, m, open):
    if m in open:
        if g >= open.get(m):
            return
    open.update({m: g})


stanje = uniformCostSearch(ishodiste, prosSt, odrediste, 0)


# A* pretrazivanje

def insertSortedBy2(g, m, open, h, closed, udalj):  # sortiranje cvorova prema heuristici,
    # udalj-> zasebna kolecija koja pamti samo cijene stanja
    if m == 'no':
        return
    if m in closed:
        return

    if m in open:
        if g > (udalj.get(m)):
            return

    b = g + float(h.get(m))
    open.update({m: b})
    udalj.update({m: g})


def optimisticnost(succ, goal, h):
    # provjeravanje optimisticnosti; poziva se  funkcija uniformCostSearch
    # kako bi se odredile sve medusobne udaljenosti cvorova i ciljnog cvora i
    # to se usporeduje
    b = 0
    print(
        "Checking if heuristic is optimistic.")  # vremenska složenost su broj stanja*brojFinalnihStanja*slozenost od ucs-a
    for i in succ:  # O(|S|*|C|*b^(1+C*/e)) tj. eksponencijalna
        for j in goal:  # prostorna slozenost je O(b^(1+c/e)) tj. eksponencijalna
            udalj = uniformCostSearch(i, succ, j, 1)
            if udalj == 'fail':
                continue
            if float(udalj) < float(h.get(i)):
                print("[ERR] h(" + i + ") > h*: " + str(h.get(i)) + " > " + str(udalj))
                b = 1
    if b > 0:
        print("Heuristic is not optimistic.")
    else:
        print("Heuristic is optimistic.")
    print()


def konzistentnost(h, succ):
    # konzistentnost: h(sr)<h(sd)+c, sr je stanje roditelj, sd stanje dijete, a c je cijena puta medu njih
    b = 0
    print("Checking if heuristic is consistent.")  # prostorna je O(b), gdje je b prosjecan broj djece/susjeda
    for i in succ:  # vremenske je O(|S|*b) gdje je |S| broj stanja
        dica = succ.get(i)
        for j in dica:
            if not dica.get(j):
                continue
            if float(h.get(i)) > float(h.get(j)) + float(dica.get(j)):
                print("[ERR] h(" + i + ") > h(" + j + ") + c: " + str(h.get(i)) + " > " + str(h.get(j)) + " + " + str(
                    dica.get(j)))
                b = 1
    if b > 0:
        print("Heuristic is not consistent.")
    else:
        print("Heuristic is consistent.")
    print()


def aStarSearch(s0, succ, goal, h):
    open = heapdict()  # prioritetni red
    udaljenosti = heapdict()
    closed = {}
    p = 0  # pamti se dal je prvo stanje
    open.update({s0: 0})
    while len(open) != 0:
        n = open.popitem()

        if p > 0:
            u = udaljenosti.get(n[0])
        else:
            udaljenosti.update({n[0]: 0})
            u = n[1]
        closed.update({n[0]: u})  # spremanje posjecenog stanja u closed listu
        p += 1
        if n[0] in goal:  # dolazak do ciljnog stanja
            put = trazenjePutaCijena(n, prosSt, closed)
            print("Running astar:")
            print("States visited = " + str(len(closed)))

            print("Found path of lenght " + str(len(put) + 1) + " total cost of " + str(n[1]))
            for i in reversed(put):
                print(i + " =>")
            print(n[0] + "\n")
            optimisticnost(prosSt, goal, h)
            konzistentnost(h, prosSt)
            return n

        ekspandirano = succ.get(n[0])  # ucitavanje djece
        for m in ekspandirano:  # za svako dijete izracunaj cijenu
            f = float(ekspandirano.get(m)) + u
            insertSortedBy2(f, m, open, h, closed, udaljenosti)  # sortiraj prema cijeni


stanje = aStarSearch(ishodiste, prosSt, odrediste, heuristika)
