from config import use_old_data
import matplotlib.pyplot as plt
import datetime
import pickle
from pprint import pprint

# todo: dodac legende
# todo: sprawdzic czy mozna dodawac pionowe kreski z oznaczeniami wydarzen
# todo: zmiana kolorow linii poszczegolnych produktow
# todo: automatyczne kopiowanie wykresu do public_html
# todo: dodawanie nowego wykresu jako head-file

# read data from datafile
if use_old_data:
    with open('old-datafile.raw', 'r') as input_handle:
        input_dict = pickle.loads(input_handle.read())
else:
    with open('datafile.raw', 'r') as input_handle:
        input_dict = pickle.loads(input_handle.read())

pprint(input_dict)

# remap data from datetime:{product:price} to product:{datetime:price} format
remapped_dict = dict()
for date_key in input_dict.items():
    for product_entry in date_key[1].items():
        if product_entry[0] not in remapped_dict:
            remapped_dict[product_entry[0]] = dict()
        remapped_dict.get(product_entry[0]).update({datetime.datetime.strptime(date_key[0], '%Y.%m.%d %H:%M:%S'): product_entry[1]})

pprint(remapped_dict)

# configure the plot
width = 1500
height = 600
ppi = 72
plt.figure(figsize=(width / ppi, height / ppi), dpi=ppi)

# serve data to plotter
for product_name in remapped_dict:
    raw_data = remapped_dict.get(product_name)
    sorted_data = sorted(raw_data.items())
    x, y = zip(*sorted_data)
    plt.plot(x, y)

# draw plot to file
filename = 'plots/' + datetime.datetime.now().strftime('%Y-%m-%d') + '.png'
plt.savefig(filename, dpi=ppi, bbox_inches='tight')
