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

if use_old_data:
    with open('old-datafile.raw', 'rb') as input_handle:
        input_dict = pickle.loads(input_handle.read())
else:
    with open('datafile.raw', 'rb') as input_handle:
        input_dict = pickle.loads(input_handle.read())

pprint(input_dict)

output_dict = dict()
for date_key in input_dict.items():
    for lol in date_key[1].items():
        if lol[0] not in output_dict:
            output_dict[lol[0]] = dict()
        output_dict.get(lol[0]).update({date_key[0]: lol[1]})

pprint(output_dict)

width = 1500
height = 600
ppi = 72
plt.figure(figsize=(width / ppi, height / ppi), dpi=ppi)

for product in output_dict:
    # product == 'GTX 1080'...
    raw_data = output_dict.get(product)
    sorted_data = sorted(raw_data.items())
    x, y = zip(*sorted_data)
    plt.plot(x, y)


filename = 'plots/' + datetime.datetime.now().strftime('%Y-%m-%d') + '.png'
plt.savefig(filename, dpi=ppi, bbox_inches='tight')
