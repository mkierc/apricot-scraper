import pickle
import json


# read data from datafile.raw
def get_current_datafile():
    with open("old-datafile.raw", "r") as input_handle:
        input_dict = pickle.loads(input_handle.read())
    return input_dict


# write data to datafile.raw
def write_raw_datafile(new_dict):
    with open("old-datafile.json", "w") as output_handle:
        json.dump(new_dict, output_handle, indent=4)


def read_datafile():
    with open("old-datafile.json", "r") as input_handle:
        input_dict = json.load(input_handle)
    return input_dict


def main():
    themap = get_current_datafile()
    print(get_current_datafile())
    write_raw_datafile(themap)

    new_map = read_datafile()
    print(new_map)

if __name__ == "__main__":
    main()
