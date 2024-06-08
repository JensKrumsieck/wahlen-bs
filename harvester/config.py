import os;

url_to2019 = "https://www3.braunschweig.de/statistik/2021_Wahl-Atlas_bis2019/data.js"
url = "https://www3.braunschweig.de/statistik/2024_Wahl-Atlas/data.js"

endpoints = [url_to2019, url]
data_dir =  os.path.dirname(__file__) + "/data/"
output_dir = os.path.dirname(__file__) + "/../data/"
filenames = ["electionsTo2019.json", "electionsSince2021.json"]