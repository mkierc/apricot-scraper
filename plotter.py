from config import use_old_data
from events import event_dict
from itertools import cycle
import matplotlib.pyplot as plt
import datetime
import json

# todo: automatyczne kopiowanie wykresu do public_html
# todo: dodawanie nowego wykresu jako head-file

# read data from datafile
if use_old_data:
    with open("old-datafile.json", "r") as input_handle:
        input_dict = json.load(input_handle)
else:
    with open("datafile.json", "r") as input_handle:
        input_dict = json.load(input_handle)

# remap data from datetime:{product:price} to product:{datetime:price} format
remapped_dict = dict()
for date_key in input_dict.items():
    for product_entry in date_key[1].items():
        if product_entry[0] not in remapped_dict:
            remapped_dict[product_entry[0]] = dict()
        remapped_dict.get(product_entry[0]).update(
            {datetime.datetime.strptime(date_key[0], "%Y.%m.%d %H:%M:%S"): product_entry[1]})


# configure the plot
subplot1_width = 1200
subplot1_height = 600
ppi = 72
figure, subplot1 = plt.subplots(1, 1, figsize=(subplot1_width / ppi, subplot1_height / ppi), dpi=ppi)

colors = cycle([
    (0.92, 0.30, 0.27),  # red 1
    (1.00, 0.47, 0.47),  # red 2
    (1.00, 0.60, 0.60),  # red 3
    (1.00, 0.71, 0.71),  # red 4
    (0.12, 0.35, 0.27),  # green 1
    (0.30, 0.57, 0.25),  # green 2
    (0.34, 0.65, 0.22),  # green 3
    (0.74, 0.93, 0.71),  # green 4
])

# sort product data by names, drop the values
(sorted_names, _) = zip(*sorted(remapped_dict.items()))


# serve data to plotter
for product_name in sorted_names:
    raw_data = remapped_dict.get(product_name)
    # sort product data by dates
    sorted_data = sorted(raw_data.items())
    x, y = zip(*sorted_data)
    plt.plot(x, y, label=product_name, color=next(colors), linewidth=2)


# prettify the plot
# sort both labels and handles by labels
handles, labels = subplot1.get_legend_handles_labels()
labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))

pretty_labels = []
for label in labels:
    pretty_labels.append(label[2:])

subplot1.legend(handles=handles, labels=pretty_labels, loc="center left", bbox_to_anchor=(1, 0.5))

for event in event_dict:
    event_name = event
    event_date = datetime.datetime.strptime(event_dict.get(event), "%Y.%m.%d")
    x_bounds = subplot1.get_xlim()
    subplot1.axvline(x=event_date, color=(0.5, 0.5, 0.5), linestyle="dashed")
    subplot1.annotate(s=event_name,
                      xy=(((event_date.toordinal() - x_bounds[0]) / (x_bounds[1] - x_bounds[0])), 1.01),
                      xycoords="axes fraction",
                      verticalalignment="bottom",
                      horizontalalignment="left",
                      rotation=270)


# draw plot to file
filename = "plots/" + datetime.datetime.now().strftime("%Y-%m-%d") + ".png"
plt.savefig(filename, dpi=ppi, bbox_inches="tight")

