import pandas as pd;
import downloader;
import config;
import geoparse;

# download files if not present
downloader.download()

# read files 2019
df_districts2019 = geoparse.read_file(config.data_dir + "electionsTo2019.json", False)
df_electoral_districts2019 = geoparse.read_file(config.data_dir + "electionsTo2019.json", True)

# read files 2021
df_districts2021 = geoparse.read_file(config.data_dir + "electionsSince2021.json", False)
df_electoral_districts2021 = geoparse.read_file(config.data_dir + "electionsSince2021.json", True)

df_districts = pd.concat([df_districts2019, df_districts2021])
df_electoral_districts = pd.concat([df_electoral_districts2019, df_electoral_districts2021])

df_districts.to_csv(config.output_dir + "districts.csv", index=False)
df_electoral_districts.to_csv(config.output_dir + "electoral_districts.csv", index=False)