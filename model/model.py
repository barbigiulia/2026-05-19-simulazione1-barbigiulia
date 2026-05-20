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

        self.addEdges()



    def addEdges(self):

        mapArtisti = {}   # idArtista = Artista(id, nome)   -- solo gli artisti nodi del grafo
        for a in self._grafo.nodes :
            mapArtisti[a.ArtistId] = a

        popolarità = {}
        for artistaID , pop in DAO.getPopolarità():
            popolarità[artistaID] = pop

        acquisti = DAO.getAcquistiClienti()    # ((cliente, artista_acquisato),(cliente, artista_acquisato),.... )
        diz = {}

        for a in acquisti:
            if a[0] not in diz:
                diz[a[0]] = []
            diz[a[0]].append(a[1])  # ClienteID= [artista1, artista2....]
        coppie = set()
        for artisti in diz.values():
            for a, b in combinations(artisti, 2):
                coppie.add((a,b))

        # aggiungo gli archi solo tra il nodo del grafo
        for a , b in coppie:
            if a in mapArtisti and b in mapArtisti:
                nodoA = mapArtisti[a]   # oggetto ArtistaA
                nodoB = mapArtisti[b]
                popA = popolarità.get(a,0)  # dizionario popolarità --- get(chiave, default)
                popB = popolarità.get(b,0)
                peso = popA+popB

                # attenzione al verso
                if popA > popB:
                    self._grafo.add_edge(nodoA, nodoB, weight=peso)
                elif popB > popA:
                    self._grafo.add_edge( nodoB,nodoA, weight=peso)
                else :
                    self._grafo.add_edge(nodoA, nodoB, weight=peso)
                    self._grafo.add_edge(nodoB, nodoA, weight=peso)



    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)