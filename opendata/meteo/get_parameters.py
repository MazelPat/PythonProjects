# maps label to attribute name and types
label_attr_map = {
    "path_to_file:": ["path_to_file", str],
    "base_url:": [ "base_url", str],
    "extension:": [ "extension", str],
    "extension_csv:": [ "extension_csv", str],
    "annee_min:": [ "annee_min", int]
}

class Params(object):
    def __init__(self, input_file_name):
        with open(input_file_name, 'r') as input_file:
            for line in input_file:
                row = line.split()
                label = row[0]
                data = row[1:]  # rest of row is data list

                attr = label_attr_map[label][0]
                datatypes = label_attr_map[label][1:]

                values = [(datatypes[i](data[i])) for i in range(len(data))]
                self.__dict__[attr] = values if len(values) > 1 else values[0]


params = Params('/home/patricemazel/opendata/data/meteo/param.dat')
print('params.path_to_file:', params.path_to_file)
print('params.base_url:', params.base_url)
print('params.extension:', params.extension)
print('params.extension_csv:', params.extension_csv)
print('params.annee_min:', params.annee_min)