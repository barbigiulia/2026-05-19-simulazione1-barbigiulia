import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        generi = self._model.getAllGeneri()
        res = []
        for g in generi:
            res.append(ft.dropdown.Option(key= g[0],
                                          text = g[1]))
        return res

    def handleCreaGrafo(self, e):
        genereID = self._view._ddGenre.value
        if genereID is None or genereID =="":
            self._view.txt_result.clear()
            self._view.txt_result.controls.append(ft.Text("selezionare un genere"))
            self._view.update_page()
            return

        try :
            id= int(genereID)
        except ValueError:
            self._view.txt_result.clear()
            self._view.txt_result.controls.append(ft.Text("Genere non valido"))
            self._view.update_page()
            return

        self._model.buildGraph(id)
        self._view.txt_result.controls.append(ft.Text(f"Grafo con {self._model.getNumNodi()} nodi e {self._model.getNumArchi()}"))
        self._view.update_page()


    def handleCammino(self,e):
        pass

