import sys
from heapq import heappush, heappop, heapify

verbose = 0
pametna = 0

def strategijaBrisanja(klauzule):
    for i in klauzule:
        for j in klauzule:
            if i == j: continue
            if i in j:
                razdvojiI = i.split(" ")
                zaprovjeru = j.split(" ")
                if all(x in zaprovjeru for x in razdvojiI):
                    klauzule.remove(j)
    return klauzule


def printanjeKlauzula(klauzus, nove, indeksir, indeks):
    zaispisat = klauzus.copy()
    cilj = zaispisat.pop()
    for i in zaispisat:
        print(str(klauzus.index(i) + 1) + ". " + i)
    print("=============")
    ciljevi = cilj.split(" ")
    for i in ciljevi:
        if i == 'v' or i == '': continue
        if '~' in i:
            i = i.replace('~', '')
        else:
            i = '~' + i
        print(str(indeksir.index(i) + 1) + ". " + i)
    print("=============")
    for i in nove:
        print(str(indeksir.index(i) + 1) + "." + i + indeks.get(i))
    print("=============")



def plResolution(klauzus):
    nove = []
    clauses = []
    indeksiranje = []
    clauses = klauzus.copy()

    cilj = clauses.pop()
    indeksiranje = clauses.copy()
    ciljevi = cilj.split(" ")
    new = []
    for i in ciljevi:
        if i == ' ': continue
        if i == 'v': continue
        if '~' in i:
            i = i.replace('~', '')
        else:
            i = '~' + i
        heappush(new, i)
        indeksiranje.append(i)

    br = len(clauses)
    heapify(clauses)
    clauses = strategijaBrisanja(clauses)
    pomocni = []
    pomocni.extend(new)
    heapify(pomocni)
    indeksi = {}
    while 1:
        new = pomocni.copy()
        clauses = strategijaBrisanja(clauses)
        if all(x in pomocni for x in klauzule): return
        for i in new:
            for j in clauses:
                zast = 0
                if i == j: continue  # jesu li klauzule jednake (do ovog ne bi trebalo doci zbog strategije brisanja, ali i dalje)
                literaliI = i.split(" ")
                literaliJ = j.split(" ")
                for k in literaliI:
                    if k == 'v': continue
                    if k == ' ': continue
                    for l in literaliJ:
                        if l == 'v': continue
                        if l == ' ': continue
                        if k in l or l in k:
                            if k == '~' + l or l == '~' + k:
                                if len(literaliJ) == 1 and len(literaliI) == 1:
                                    if verbose == 1 or pametna == 1:
                                        nove.append('NIL')
                                        indeksiranje.append('NIL')
                                        indeks = '(' + str(indeksiranje.index(j) + 1) + ',' + str(
                                            indeksiranje.index(i) + 1) + ')'
                                        indeksi.update({'NIL': indeks})
                                        if verbose == 1:
                                            printanjeKlauzula(klauzus, nove, indeksiranje, indeksi)
                                    return 1
                                literaliI.remove(k)
                                literaliJ.remove(l)
                                zast = 1
                                break
                if zast == 1:
                    premisa = ''
                    for k in literaliI:
                        k=k.strip()
                        if k == 'v' or k == ' ': continue
                        if premisa == '':
                            premisa = k
                        else:
                            premisa = premisa + " v " + k
                    for l in literaliJ:
                        l=l.strip()
                        if l == 'v' or l == ' ': continue
                        if premisa == '':
                            premisa = l
                        else:
                            premisa = premisa + " v " + l

                    if premisa in pomocni or premisa == ' ': continue
                    heappush(pomocni, premisa)
                    if premisa not in clauses and premisa != ' ':
                        heappush(clauses, premisa)

                    strategijaBrisanja(pomocni)
                    if verbose == 1 or pametna == 1:
                        br += 1
                        if premisa != ' ' and premisa not in indeksiranje:
                            nove.append(premisa)
                            indeksiranje.append(premisa)
                            indeks = '(' + str(indeksiranje.index(j) + 1) + ',' + str(indeksiranje.index(i) + 1) + ')'
                            indeksi.update({premisa: indeks})
        if new == pomocni:
            return nove


if sys.argv[1] == 'resolution':
    if sys.argv[-1] == 'verbose':
        verbose = 1
    f1 = open(sys.argv[2], "r")
    klauzule = []
    for i in f1.readlines():
        if "#" in i: continue
        if (i == "\n"): continue
        klauzule.append(i.strip().lower())
    zastavica = plResolution(klauzule)
    cilj = klauzule.pop()

    if zastavica == 1:
        print(cilj + " is true")
    else:
        print(cilj + " is unknown")

if sys.argv[1] == 'cooking_interactive':
    if sys.argv[-1] == 'verbose':
        verbose = 1
    f1 = open(sys.argv[2], "r")
    klauzule = []
    for i in f1.readlines():
        if "#" in i: continue
        if i == "\n": continue
        klauzule.append(i.strip().lower())

    while 1:
        naredba = input("Please enter you query: ")

        if naredba[-1] == '?':
            novaklauz = naredba.replace('?', '').strip()
            klauzule.append(novaklauz.lower())
            zastavica = plResolution(klauzule)
            cilj = klauzule.pop()
            if zastavica == 1:
                print(cilj + " is true")
            else:
                print(cilj + " is unknown")

        if naredba[-1] == '+':
            novaklauz = naredba.replace('+', '').strip()
            if novaklauz.lower() in klauzule:
                print(novaklauz.lower() + " already in.")
            else:
                klauzule.insert(0,novaklauz.lower())
                print("added " + novaklauz.lower())

        if naredba[-1] == '-':
            novaklauz = naredba.replace('-', '').strip()
            if novaklauz.lower() in klauzule:
                klauzule.remove(novaklauz.lower())
                print("removed " + novaklauz.lower())
            else: print("There is no "+novaklauz.lower())
        if naredba == 'exit':
            exit(0)

if sys.argv[1] == 'cooking_test':
    f1 = open(sys.argv[2], "r")
    klauzule = []
    for i in f1.readlines():
        if "#" in i: continue
        if i == "\n": continue
        klauzule.append(i.strip().lower())

    f2 = open(sys.argv[3], "r")
    korNar = []
    for i in f2.readlines():
        if i == "#": continue
        if i == "\n": continue
        korNar.append(i.strip().lower())
    moguciodg = []
    for i in korNar:
        if i[-1] == '?':
            novaklauz = i.replace('?', '').strip()
            klauzule.append(novaklauz.lower())
            zastavica = plResolution(klauzule)
            cilj = klauzule.pop()
            if zastavica == 1:
                print(cilj + " is true")
            else:
                print(cilj + " is unknown")
        if i[-1] == '-':
            novaklauz = i.replace('-', '').strip()
            if novaklauz.lower() in klauzule:
                klauzule.remove(novaklauz.lower())
        if i[-1] == '+':
            novaklauz = i.replace('+', '').strip()
            if novaklauz.lower() not in klauzule:
                klauzule.append(novaklauz.lower())

if sys.argv[1] == 'smart_resolution_interactive':
    if sys.argv[-1] == 'verbose':
        verbose = 1
    pametna = 1
    f1 = open(sys.argv[2], "r")
    klauzule = []
    for i in f1.readlines():
        if "#" in i: continue
        if i == "\n": continue
        klauzule.append(i.strip().lower())

    moguciodg = []
    while 1:
        naredba = input("Please enter you query: ")
        if naredba[-1] == '?':
            novaklauz = naredba.replace('?', '').strip()
            klauzule.append(novaklauz.lower())
            zastavica = plResolution(klauzule)
            cilj = klauzule.pop()
            if zastavica == 1:
                print(cilj + " is true")
            else:
                print(cilj + " is unknown")

                cilj=klauzule.append(cilj)
                for klauz in zastavica:
                    literali=klauz.split(' ')
                    if len(literali) == 1:
                        if '~' in klauz:
                            klauz = klauz.replace('~', '')
                        else:
                            klauz = '~' + klauz
                        heappush(moguciodg, klauz)
                print("Candidate questions: ", '')
                print(moguciodg)
                for b in moguciodg:
                    print(b + "?")
                    odgovor = input("[Y/N/?] ")
                    if odgovor == 'Y':
                        klauzule.insert(0, b.strip().lower())
                        zasti = plResolution(klauzule)
                        cilj=klauzule.pop()
                        if zasti == 1:
                            print(cilj + " is true")
                        else:
                            print(cilj + " is unknown")
                        break
                    elif odgovor == '?' or odgovor == 'F':
                        continue
            #klauzule.append(cilj)

        if naredba[-1] == '+':
            novaklauz = naredba.replace('+', '').strip()
            if novaklauz.lower() in klauzule:
                print(novaklauz.lower() + " already in.")
            else:
                klauzule.insert(0,novaklauz.lower())
                print("added " + novaklauz.lower())

        if naredba[-1] == '-':
            novaklauz = naredba.replace('-', '').strip()
            if novaklauz.lower() in klauzule:
                klauzule.remove(novaklauz.lower())
                print("removed " + novaklauz.lower())
            else: print("There is no "+novaklauz.lower())
        if naredba == 'exit':
            exit(0)
        if naredba[-1] == 'p':
            print(klauzule)

if sys.argv[1] == 'smart_resolution_test':

    pametna = 1
    f1 = open(sys.argv[2], "r")
    klauzule = []
    for i in f1.readlines():
        if "#" in i: continue
        if i == "\n": continue
        klauzule.append(i.strip().lower())
    f2 = open(sys.argv[3], "r")
    korNar = []
    for i in f2.readlines():
        if i == "#": continue
        if i == "\n": continue
        korNar.append(i.strip().lower())
    moguciodg = []
    for naredba in korNar:
        if naredba[-1] == '?':
            novaklauz = naredba.replace('?', '').strip()
            klauzule.append(novaklauz.lower())
            zastavica = plResolution(klauzule)
            cilj = klauzule.pop()
            if zastavica == 1:
                print(cilj + " is true")
                continue
            else:
                for klauz in zastavica:
                    literali=klauz.split(' ')
                    if len(literali) == 1:
                        if '~' in klauz:
                            klauz = klauz.replace('~', '')
                        else:
                            klauz = '~' + klauz
                        heappush(moguciodg, klauz)

                for i in moguciodg:
                    print(i)
        if naredba[-1] == '-':
            novaklauz = naredba.replace('-', '').strip()
            if novaklauz.lower() in klauzule:
                klauzule.remove(novaklauz.lower())
        if naredba[-1] == '+':
            novaklauz = naredba.replace('+', '').strip()
            if novaklauz.lower() not in klauzule:
                klauzule.append(novaklauz.lower())