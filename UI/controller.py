from xxlimited_35 import Null

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        for nat in self._model.getAllNations():
            self._listCountry.append(nat)
            self._view.ddcountry.options.append(ft.dropdown.Option(nat))
        for y in self._model.getAllYears():
            self._listYear.append(y)
            self._view.ddyear.options.append(ft.dropdown.Option(y))


    def handle_graph(self, e):
        nation = self._view.ddcountry.value
        year = self._view.ddyear.value
        if nation is None or year is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Selezionare un anno e una nazione.",
                                                          color="red"))
            self._view.update_page()
            return
        y = int(year)
        self._model.buildGraph(nation, y)
        n, e = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {n} | Numero di archi: {e}"))
        self._view.update_page()


    def handle_volume(self, e):
        volumi = self._model.calcolaVolumi()
        self._view.txtOut2.controls.clear()
        for volume in volumi:
            self._view.txtOut2.controls.append(ft.Text(f"{volume[0]} --> {volume[1]}"))
        self._view.update_page()


    def handle_path(self, e):
        txtN = self._view.txtN.value
        if txtN == "":
            self._view.txtOut3.controls.clear()
            self._view.txtOut3.controls.append(ft.Text(f"Inserire il numero di archi desiderato.",
                                                          color="red"))
            self._view.update_page()
            return
        try:
            N = int(txtN)
        except ValueError:
            self._view.txtOut3.controls.clear()
            self._view.txtOut3.controls.append(ft.Text(f"Il numero di archi deve essere un intero.",
                                                          color="red"))
            self._view.update_page()
            return
        if N < 2:
            self._view.txtOut3.controls.clear()
            self._view.txtOut3.controls.append(ft.Text(f"Il numero di archi deve essere almeno uguale a 2.",
                                                       color="red"))
            self._view.update_page()
            return

        bestPath, bestScore = self._model.getBestPath(N)
        self._view.txtOut3.controls.clear()
        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {bestScore}"))
        for i in range(N):
            self._view.txtOut3.controls.append(ft.Text(f"{bestPath[i]} --> {bestPath[i+1]}: {self._model._graph[bestPath[i]][bestPath[i+1]]["weight"]}"))
        self._view.update_page()
