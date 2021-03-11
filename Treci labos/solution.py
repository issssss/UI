import sys
from heapq import heappush, heappop, heapify
import math


class ID3:
    def __init__(self, mode, model, depth, trees, fr, er):
        self.mode = mode
        self.model = model
        self.maxD = depth
        self.numTrees = trees
        self.feature = fr
        self.example = er

    def entropija(self, D):
        D2 = {}
        br = 0
        ent = 0
        for i in D:
            vrij = i.split(',')
            zadnji = vrij[len(vrij) - 1]
            if zadnji in D2:
                n = D2.get(zadnji)
                n += 1
                D2.update({zadnji: n})
                continue
            else:
                D2.update({zadnji: 1})
            br += 1

        for i in D2:
            ent += D2.get(i) / len(D) * math.log2(D2.get(i) / len(D))
        return -ent

    def argMaxP(self, D, x):
        V = {}
        for i in D:
            linija = i.split(',')
            # indeks = znacajkeTren.index(x)
            # if linija[indeks] == P[0][0]:
            if linija[len(linija) - 1] in V:
                m = V.get(linija[len(linija) - 1])
                m += 1
                V.update({linija[len(linija) - 1]: m})
            else:
                V.update({linija[len(linija) - 1]: 1})
        V = sorted(V.items(), key=lambda x: (-x[1], x[0]))
        # print(V)
        return V[0][0]

    def argMaxIG(self, X, D):
        IG = {}
        for i in X:
            ige = self.ig(D, i)
            IG.update({i: ige})
        IG = sorted(IG.items(), key=lambda x: (-x[1], x[0]))

        return IG[0][0]

    def ig(self, D, x):
        entSkupa = self.entropija(D)
        indeks = znacajkeTren.index(x)

        entX = 0

        P = {}
        for i in skupoviVrijednosti.get(x):
            zaEnt = []
            P.update({i: 0})
            for j in D:
                linija = j.split(',')
                if i == linija[indeks]:
                    zaEnt.append(j)
                    n = P.get(i)
                    n += 1
                    P.update({i: n})
            entX += P.get(i) / len(D) * self.entropija(zaEnt)

        return entSkupa - entX

    def fit(self, D, Dp, X, y, ind, zaPri):
        node = {}
        if len(D) == 0:
            v = self.argMaxP(Dp, y)
            return v
        v = self.argMaxP(D, y)
        if y in znacajkeTren:
            for i in skupoviVrijednosti.get(znacajkeTren[len(znacajkeTren) - 1]):
                br = 0
                for j in D:
                    linija = j.split(',')
                    if linija[len(linija) - 1] == i:
                        br += 1
                if br == len(D):
                    return v
        if len(X) == 0:
            # print(v)
            return v
        if int(ind) == int(maxD) and int(maxD) > 0:
            return v
        x = self.argMaxIG(X, D)
        Xcopy = X.copy()
        Xcopy.remove(x)
        string = str(ind) + ":" + x
        zaPri.append(string)
        subtrees = {}

        indeks = znacajkeTren.index(x)
        for v in sorted(skupoviVrijednosti.get(x)):
            noviD = []
            # noviD = D.copy()
            for j in D:
                linija = j.split(',')
                if v == linija[indeks]:
                    noviD.append(j)
                    # continue
                # else: noviD.remove(j)
            t = self.fit(noviD, D, Xcopy, x, ind + 1, zaPri)

            subtrees.update({v: t})
            node.update({x: subtrees})
        return node

    def predict(self, stablo, linija, znacajkeTest, D):
        if type(stablo) is str:
            return stablo
        else:
            zn = list(stablo.keys())[0]
            indeks = znacajkeTest.index(zn)
            vrZnacajke = linija.split(",")[indeks]
            Dcopy = D.copy()
            for d in D:
                if d.split(",")[indeks] != vrZnacajke:
                    Dcopy.remove(d)
            if vrZnacajke in stablo[zn].keys():
                return self.predict(stablo[zn][vrZnacajke], linija, znacajkeTest, Dcopy)
            else:
                return self.argMaxP(D, "")


f1 = open(sys.argv[1], "r")
#f1 = open("C://Users/Izabela/Desktop/datasets/logic_small.csv", "r")
j = 0;
znacajkeTren = []
vrijednostiTren = []
for i in f1.readlines():
    if j == 0:
        znacajkeTren = i.strip().split(',')
    else:
        vrijednostiTren.append(i)
    j += 1;
    if i == "\n": continue

f2 = open(sys.argv[2], "r")
#f2 = open("C://Users/Izabela/Desktop/datasets/logic_small_test.csv", "r")
znacajkeTest = []
vrijednostiTest = []
j = 0
for i in f2.readlines():
    if j == 0:
        znacajkeTest = i.strip().split(',')
    else:
        vrijednostiTest.append(i)
    j += 1;
    if i == "\n": continue

f3 = open(sys.argv[3], "r")
#f3 = open("C://Users/Izabela/Desktop/config/id3.cfg", 'r')
for i in f3.readlines():
    if "mode" in i:
        if "model" in i:
            dijelovi1 = i.split("=")
            model = dijelovi1[1].strip()
        else:
            dijelovi = i.split("=")
            mode = dijelovi[1].strip()

    if "max_depth" in i:
        dijelovi2 = i.split("=")
        maxD = dijelovi2[1].strip()
    if "num_trees" in i:
        dijelovi3 = i.split("=")
        trees = dijelovi3[1].strip()
    if "feature_ratio" in i:
        dijelovi4 = i.split("=")
        feature = dijelovi4[1].strip()
    if "example_ratio" in i:
        dijelovi5 = i.split("=")
        example = dijelovi5[1].strip()
    if i == "\n": continue
# print("znak")
# print(mode + " " + model + " " + maxD + " " + trees + " " + feature + " " + example)
skupoviVrijednosti = {}
for i in vrijednostiTren:
    linija = i.lstrip().split(",")
    for j in linija:
        # print(j)
        index = linija.index(j)
        kljuc = znacajkeTren[index]
        if kljuc in skupoviVrijednosti:
            popis = skupoviVrijednosti.get(kljuc)
            if j in popis:
                continue
            else:
                popis.append(j)
                skupoviVrijednosti.update({kljuc: popis})
        else:
            novi = []
            novi.append(j)
            skupoviVrijednosti.update({kljuc: novi})
    # print()

id3 = ID3(mode, model, maxD, trees, feature, example)
znac = []
br = 0
for i in znacajkeTren:
    if br == len(znacajkeTren) - 1:
        break
    else:
        znac.append(i)
        br += 1
printic = []
test = ID3.fit(id3, vrijednostiTren, vrijednostiTren, znac, "yes", 0, printic)

k = 0
for i in printic:
    if k == len(printic) - 1:
        print(i)
    else:
        print(i + ", ", end='')
    k += 1
predicti = []
tocno = 0
for vr in vrijednostiTest:
    rez = ID3.predict(id3, test, vr, znacajkeTest, vrijednostiTren)
    predicti.append(rez)
    if rez == vr.split(",")[-1]:
        tocno += 1
for pr in predicti:
    print(pr[:-1], end=" ")
print()
print("{:.5f}".format(tocno / len(predicti)))
istina = {}
laz = {}

for i in skupoviVrijednosti.get(znacajkeTest[len(znacajkeTest)-1]):
    istina.update({i:0})

    for j in skupoviVrijednosti.get(znacajkeTest[len(znacajkeTest) - 1]):
        if j!= i:
            novi = {}
            novi.update({j:0})
            laz.update({i:novi})

for pr in vrijednostiTest:
    jest = 0
    linija = pr.split(',')
    indeks = vrijednostiTest.index(pr)
    ist = predicti[indeks]
    if ist == linija[len(linija) - 1]:
        if ist in istina:
            jest = istina.get(ist)
            jest += 1
            istina.update({ist:jest})
        else:
            istina.update({ist: 1})
    else:
        if ist in laz:
            nije = laz.get(ist)
            izbor = nije.get(linija[len(linija)-1])
            izbor += 1
            nije.update({linija[len(linija)-1]:izbor})
            laz.update({ist:nije})
        else:
            nije = {}
            nije.update({linija[len(linija)-1]:1})
            laz.update({ist:nije})

ispisIstine = sorted(istina.items(), key=lambda x: (x[0]))
ispisLazi = sorted(laz.items(), key=lambda x: (x[0]))


matrica = [[None for y in range( len(ispisLazi))] for x in range(len(ispisIstine))]
for i in range(len(ispisIstine)):
    for j in range(len(ispisLazi)):

        if i == j:
            matrica[i][i] = ispisIstine[i][1]

        else:
            vrijednost = list(ispisLazi[i][1].values())
            matrica[j][i] = vrijednost[0]

for i in range(len(ispisIstine)):
    for j in range(len(ispisLazi)):
        print(matrica[i][j], end = ' ')
    print()


