from itertools import combinations

import networkx as nx

from database.DAO import DAO
from model.artista import Artista


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()



    def getAllGeneri(self):
        return DAO.getAllGenres()

    def buildGraph(self, genereID):
        self._grafo = nx.DiGraph()
        artisti = DAO.getNodes(genereID)
        print(f"Artisti trovati: {len(artisti)}")  # ← debug
        for a in artisti:
            nodo = Artista(ArtistId=a[0], Name=a[1])
            self._grafo.add_node(nodo)
        print(f"Nodi nel grafo: {len(self._grafo.nodes)}")  # ← debug

        self.addEdges(genereID)


    def addEdges(self, genereID):
        mapArtisti = {}   # idArtista = Artista(id, nome)   --> solo gli artisti nodi del grafo
        for a in self._grafo.nodes :
            mapArtisti[a.ArtistId] = a
        print(f"Nodi in mapArtisti: {len(mapArtisti)}")  # debug

        popolarità = {}
        for artistaID , pop in DAO.getPopolarità():
            popolarità[artistaID] = pop

        acquisti = DAO.getAcquistiClienti(genereID)    # ( (IDcliente, IDartista_acquisato), .... )
        print(f"Acquisti totali: {len(acquisti)}")  # debug
        diz = {}

        for customerID, artistID in acquisti:
            if artistID in mapArtisti:  # ← filtra subito solo artisti del genere
                if customerID not in diz:
                    diz[customerID] = set()
                diz[customerID].add(artistID) # ClienteID = [artista1, artista2....]



        coppie = set()
        for artisti in diz.values(): # itero su id Artisti (acquistati da ogni cliente)
            for a, b in combinations(sorted(artisti), 2):
                if a in mapArtisti and b in mapArtisti:  # filtra solo coppie entrambe nel grafo
                    coppie.add((min(a, b), max(a, b)))
        print(f"Coppie totali: {len(coppie)}")  # debug
                # il set è FONDAMENTALE perchè più clienti potrebbero aver acquistato
                # gli stessi artisti, e non si vuole aggiungere lo stesso arco più volte

        # combinations --> prende una lista e restituisce tutte le coppie possibili
        # senza ripetizioni e senza ordine
        # es. combinations([1,2,3], 2) --> restituisce (1,2), (1,3), (2,3)
        archi_doppi = 0
        for a , b in coppie:


                # mi assicuro che entrambi gli artisti siano dei nodi del grafo
                nodoA = mapArtisti[a]   # oggetto ArtistaA
                nodoB = mapArtisti[b]   # lo recupero passandogli la key= ArtistID
                popA = popolarità.get(a,0)  # dizionario popolarità ---> diz.get(chiave, default)
                popB = popolarità.get(b,0)
                peso = popA+popB

                # attenzione al verso
                if popA > popB:
                    self._grafo.add_edge(nodoA, nodoB, weight=peso)
                elif popB > popA:
                    self._grafo.add_edge( nodoB,nodoA, weight=peso)
                else :
                    archi_doppi += 1
                    self._grafo.add_edge(nodoA, nodoB, weight=peso)
                    self._grafo.add_edge(nodoB, nodoA, weight=peso)

        print(f"Coppie con stessa pop (archi doppi): {archi_doppi}")
        print(f"Archi totali nel grafo: {len(self._grafo.edges)}")




    def getArtistaMaggioreInfluenza(self):
        migliore= None
        maxInfluenza = None

        # itero sugli artisti che sono Nodi del grafo
        for n in self._grafo.nodes:
            # peso archi uscenti
            pesoUscenti= 0
            for vicino in self._grafo.successors(n):
                pesoUscenti += self._grafo[n][vicino]["weight"]

            pesoEntranti = 0
            for predecessore in self._grafo.predecessors(n):
                pesoEntranti += self._grafo[predecessore][n]["weight"]

            influenza  = pesoUscenti - pesoEntranti

            if migliore is None or influenza > maxInfluenza:
                migliore = n
                maxInfluenza = influenza

        return migliore, maxInfluenza



    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)


    def getArchiConPeso(self):
        return list(self._grafo.edges(data=True))