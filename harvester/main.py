import pandas as pd;
import downloader;
import config;
import excelparse;
import geoparse;

# download files if not present
downloader.download()

# read files 2019
df_districts2019 = geoparse.read_file(config.data_dir + "electionsTo2019.json", False)
df_electoral_districts2019 = geoparse.read_file(config.data_dir + "electionsTo2019.json", True)

# read excel 2021
df_districts2021 = excelparse.read_file(config.data_dir + "2024-06_Daten_Wahl-Atlas.xlsx", False)
df_electoral_districts2021 = excelparse.read_file(config.data_dir + "2024-06_Daten_Wahl-Atlas.xlsx", True)

# combine data
df_districts = pd.concat([df_districts2019, df_districts2021])
df_electoral_districts = pd.concat([df_electoral_districts2019, df_electoral_districts2021])

# save data
df_districts.to_csv(config.output_dir + "districts.csv", index=False)
df_electoral_districts.to_csv(config.output_dir + "electoral_districts.csv", index=False)