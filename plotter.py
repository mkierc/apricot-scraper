from config import use_old_data
import matplotlib.pyplot as plt
import datetime
import pickle
from itertools import cycle
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

# todo: posortowac dane po nazwach przed przekazaniem do rysowania
pprint(remapped_dict)

# configure the plot
width = 1500
height = 600
ppi = 72
plt.figure(figsize=(width / ppi, height / ppi), dpi=ppi)

# todo: dodac sensowne kolory
colors = cycle([
    (1, 0, 0, 1),  # red
    'g',
    'b'
])

# serve data to plotter
for product_name in remapped_dict:
    raw_data = remapped_dict.get(product_name)
    sorted_data = sorted(raw_data.items())
    x, y = zip(*sorted_data)
    plt.plot(x, y, label=product_name, color=colors.next())


# Shrink current axis by 20%
ax = plt.subplot(111)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])


handles, labels = ax.get_legend_handles_labels()
# sort both labels and handles by labels
labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
ax.legend(handles=handles, labels=labels, loc='center left', bbox_to_anchor=(1, 0.5))


# draw plot to file
filename = 'plots/' + datetime.datetime.now().strftime('%Y-%m-%d') + '.png'
plt.savefig(filename, dpi=ppi, bbox_inches='tight')
