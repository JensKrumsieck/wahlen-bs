import pandas as pd;
import glob;
import os;


xlsx = pd.ExcelFile('./data/2024-02_Daten_Wahl-Atlas.xlsx')
df = pd.read_excel(xlsx, header=[0,1,2], sheet_name='175 Wahlbezirke', index_col=0)

# get election types
types = df.columns.get_level_values(0).unique()[:-1]
replaceTypes = ["OB", "Stadtrat", "Bezirksrat", "Landtag", "Bundestag", "Europaparlament"]

for t in types:
    # get election years
    years = df[t].columns.get_level_values(0).unique()
    for y in years:
        if str(y).isdigit():
            # get result
            election = df[t][y]
                
            # write to csv
            election.to_csv(f'./data/{replaceTypes[types.get_loc(t)]}_{y}.csv')


# read europawahl folder
csv_files = glob.glob('./data/EU2019/*.{}'.format('csv'))

df_append = pd.DataFrame()

for file in csv_files:
    name = os.path.basename(file)
    df = pd.read_csv(file, index_col=0, sep=';')
    df.columns = [name.replace('.csv', '')]
    df_append = df_append.merge(df, how='outer', left_index=True, right_index=True)
df_append.index.name = 'Wahlbezirke'
df_append.to_csv('./data/EU2019.csv')