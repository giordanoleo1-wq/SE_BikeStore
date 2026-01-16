import datetime
from model.model import Model
model = Model()

print(model.get_all_categories())

model.crea_grafo(7, datetime.date(2016, 1, 1), datetime.date(2018, 12, 28))
print(model.lista_product_category_valid)
#print(model.dic_category_products)
#print(model.G.nodes())
print(len(model.G.nodes()))
#print(model.dic_order_date)
#print(model.dic_product_order_id)
#print(len(model.lista_orders))
#print(sorted(model.dic_quantita_per_prodotto.keys()))
print(model.lista_products_year_valid)
print(len(model.lista_products_year_valid))
print(model.G.edges())
print(len(model.G.edges()))

print(model.percorso_ottimo)
print(model.costo_ottimo)

print("Finito")