from urllib.request import urlopen;
import os;
import config;

def download():   
    dir = config.data_dir
    # get data from urls if not present
    if not os.path.exists(dir + config.filenames[0]):
        with urlopen(config.endpoints[0]) as response:
            data = response.read().decode("utf-8")
            with open(dir + config.filenames[0], "w") as file:
                file.write(data)

    if not os.path.exists(dir + config.filenames[1]):
        with urlopen(config.endpoints[1]) as response:
            data = response.read().decode("utf-8")
            with open(dir + config.filenames[1], "w") as file:
                file.write(data)