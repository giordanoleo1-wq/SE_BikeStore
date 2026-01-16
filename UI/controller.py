from UI.view import View
from model.model import Model
import flet as ft
import datetime

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def set_dates(self):
        first, last = self._model.get_date_range()

        self._view.dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view.dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view.dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view.dp2.current_date = datetime.date(last.year, last.month, last.day)

    def handle_dd_categories(self):
        lista_categories= self._model.get_all_categories()
        result= []
        for c in lista_categories:
            result.append(ft.dropdown.Option(text=c.category_name, key=c.id))

        return result

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """
        # TODO
        self._view.txt_risultato.clean()
        category= int(self._view.dd_category.value)
        try:
            date1= self._view.dp1.value.date()
            date2= self._view.dp2.value.date()
        except Exception:
            self._view.show_alert("Inserire le date")
            return
        self._model.crea_grafo(category, date1, date2)

        self._view.txt_risultato.controls.append(ft.Text(f"Date slezionate:\n"
                                                         f"start date: {date1}\n"
                                                         f"end date: {date2}"))

        self._view.txt_risultato.controls.append(ft.Text(f"Grafo correttamente creato: \n"
                                                         f"Numero di nodi: {self._model.G.number_of_nodes()}\n"
                                                         f"Numero di archi: {self._model.G.number_of_edges()}"))


        for n in self._model.G.nodes():
            self._view.dd_prodotto_iniziale.options.append(ft.dropdown.Option(key=n.id, text=n.product_name))
            self._view.dd_prodotto_finale.options.append(ft.dropdown.Option(key=n.id, text=n.product_name))
            self._view.txt_lunghezza_cammino.disabled = False
            self._view.dd_prodotto_iniziale.disabled= False
            self._view.dd_prodotto_finale.disabled = False
            self._view.pulsante_cerca_cammino.disabled = False






        self._view.update()

    def handle_best_prodotti(self, e):
        """ Handler per gestire la ricerca dei prodotti migliori """
        # TODO

        lista_prodotti= self._model.get_prodotti_piu_venduti()

        self._view.txt_risultato.controls.append(ft.Text(f"I cinque prodotti più venduti sono: "))
        for p, tot in lista_prodotti:
            self._view.txt_risultato.controls.append(ft.Text(f"{p.product_name} with total {tot}"))

        self._view.update()









    def handle_cerca_cammino(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
        self._view.txt_risultato.clean()

        try:
            lunghezza= int(self._view.txt_lunghezza_cammino.value)
        except Exception:
            self._view.show_alert("Inserire una lunghezza corretta")
            return

        try:
            start_id= int(self._view.dd_prodotto_iniziale.value)
            finish_id= int(self._view.dd_prodotto_finale.value)
        except Exception as exc:
            self._view.show_alert("Inserire un prodotto iniziale e finale corretto")
            print(exc)
            return
        start= self._model.dic_product_id[start_id]
        finish= self._model.dic_product_id[finish_id]

        if start== finish:
            self._view.show_alert("Inserire un prodotto finale diverso da quello iniziale")
        if start is None or finish is None:
            self._view.show_alert("Inserire un prodotto iniziale e finale")

        sequenza_ottima, costo_ottimo= self._model.get_percorso_ottimo(lunghezza, start, finish)
        self._view.txt_risultato.controls.append(ft.Text("Cammino migliore: \n"))


        for nodo in sequenza_ottima:
            self._view.txt_risultato.controls.append(ft.Text(f"{nodo.product_name}"))

        self._view.txt_risultato.controls.append(ft.Text(f"Score {costo_ottimo}"))

        self._view.update()





