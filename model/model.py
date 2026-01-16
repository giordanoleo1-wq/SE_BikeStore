import networkx as nx
from database.dao import DAO
from model.product import Product


class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        self.lista_categories= DAO.read_all_categories()
        self.lista_stocks= DAO.read_all_stocks()
        self.lista_orders= DAO.read_all_orders()
        self.lista_orders_items = DAO.read_all_orders_items()
        self.lista_products= DAO.read_all_products()

        self.dic_id_category = {}
        self.dic_product_id = {}
        self.dic_order_date = {}
        self.dic_category_products = {}

        self.dic_quantita_per_prodotto= {}


        self.lista_product_category_valid = []
        self.lista_products_year_valid = []

        self.percorso_ottimo = []
        self.costo_ottimo = 0


    def get_date_range(self):
        return DAO.get_date_range()

    def get_all_categories(self):
        set_categories= set()
        for category in self.lista_categories:
            set_categories.add(category)

        return list(set_categories)








    def crea_grafo(self, category, start, end):
        self.G= nx.DiGraph()

        self.dic_id_category = {}
        self.dic_product_id = {}
        self.dic_order_date = {}
        self.dic_category_products = {}

        self.dic_quantita_per_prodotto = {}


        self.lista_product_category_valid = []
        self.lista_products_year_valid= []


        for c in self.lista_categories:
            if c.id not in self.dic_id_category:
                self.dic_id_category[c.id] = c.category_name

        for p in self.lista_products:
            if p.id not in self.dic_product_id:
                self.dic_product_id[p.id] = p


            if p.category_id not in self.dic_category_products:
                self.dic_category_products[p.category_id] = set()
            self.dic_category_products[p.category_id].add(p.id)

            if p.category_id == category:
                if p not in self.lista_product_category_valid:
                    self.lista_product_category_valid.append(p)


        for o in self.lista_orders:
            if o.id not in self.dic_order_date:
                self.dic_order_date[o.id] = o.order_date.date()

        for oi in self.lista_orders_items:
            d= self.dic_order_date[oi.order_id]

            if start<=d<=end:
                if oi.product_id not in self.lista_products_year_valid:
                    self.lista_products_year_valid.append(oi.product_id)

                if self.dic_product_id[oi.product_id].category_id == category:
                    if oi.product_id not in self.dic_quantita_per_prodotto:
                        self.dic_quantita_per_prodotto[oi.product_id] = set()
                    self.dic_quantita_per_prodotto[oi.product_id].add(oi.order_id)




        for p in self.lista_product_category_valid:
            self.G.add_node(p)

        for i in range(len(self.lista_product_category_valid)):
            for j in range(i+1, len(self.lista_product_category_valid)):

                p1 = self.lista_product_category_valid[i]
                p2 = self.lista_product_category_valid[j]

                if p1.id in self.dic_quantita_per_prodotto and p2.id in self.dic_quantita_per_prodotto:
                    q1= self.calcola_prodotti_venduti(p1.id)
                    q2= self.calcola_prodotti_venduti(p2.id)

                    if q1>q2:
                        self.G.add_edge(p1, p2, peso= q1+q2)
                    elif q2>q1:
                        self.G.add_edge(p2, p1, peso= q1+q2)
                    elif q1==q2:
                        self.G.add_edge(p1, p2, peso= q1+q2)
                        self.G.add_edge(p2, p1, peso= q1+q2)



    def calcola_prodotti_venduti(self, p_id):
        quantita= 0
        if p_id in self.dic_quantita_per_prodotto:
            quantita= len(self.dic_quantita_per_prodotto[p_id])
        return quantita

    def get_prodotti_piu_venduti(self):
        pesi_tot= []
        for n in self.G.nodes():
            pesi_entranti= []
            pesi_uscenti= []

            for _,_, data in self.G.out_edges(n, data=True):
                peso= data['peso']
                pesi_uscenti.append(peso)
            for _,_, data in self.G.in_edges(n, data=True):
                pesi_entranti.append(data['peso'])
            pesi= sum(pesi_uscenti)-sum(pesi_entranti)
            pesi_tot.append((n, pesi))
        pesi_tot.sort(key=lambda x: x[1], reverse=True)
        pesi_tot_definitivo= pesi_tot[:5]

        return pesi_tot_definitivo




    def get_percorso_ottimo(self, lunghezza, start, finish):
        self.percorso_ottimo= []
        self.costo_ottimo= 0
        set_archi_usati = {start}

        self.ricorsione(start, [start], 0, set_archi_usati, lunghezza, finish)
        return self.percorso_ottimo, self.costo_ottimo







    def ricorsione(self, start, sequenza_parziale, costo_parziale, set_archi_usati, lunghezza, finish):
        if len(sequenza_parziale)> lunghezza:
            return


        if costo_parziale> self.costo_ottimo and len(sequenza_parziale)== lunghezza:
            if sequenza_parziale[-1] == finish:
                self.costo_ottimo = costo_parziale
                self.percorso_ottimo= list(sequenza_parziale)


        for v in self.G.neighbors(start):
            if v not in set_archi_usati:
                peso= self.G[start][v]['peso']
                sequenza_parziale.append(v)
                set_archi_usati.add(v)
                self.ricorsione(v, sequenza_parziale, costo_parziale+peso, set_archi_usati, lunghezza, finish)

                sequenza_parziale.pop()
                set_archi_usati.remove(v)





































