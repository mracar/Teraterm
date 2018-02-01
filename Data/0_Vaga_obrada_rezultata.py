import pandas as pd
import re


ime_datoteke_bez_ext = 'Vaga_test'
ime_datoteke = ime_datoteke_bez_ext + '.txt'
data = []
errors =[]

with open(ime_datoteke) as f:
    read_data = f.read()
    data = read_data.split('\n')
    clean_data = []
    for line in data:
        #print(line)
        mass = re.search(r"....\d\.\d\d", line, flags=0)
        timestamp = re.search(r"\d\d\:\d\d\:\d\d", line, flags=0)
        if mass and timestamp :
            mass = mass.group(0)
            time = timestamp.group(0)
            try:
                if mass and time:
                    clean_data.append([float(mass), pd.Timestamp(time)])
            except:
                print (line)

#print(clean_data)
df = pd.DataFrame(clean_data, columns=['Mass, g', 'Time, s'])
df['Time, s'] = df['Time, s'] - df['Time, s'][0]
df['Time, s'] = df['Time, s'].dt.total_seconds()
#df.groupby(['Time, s'])['Mass, g'].mean()
df = df.set_index('Time, s').groupby(['Time, s']).mean().dropna(how='all')
print(df)
 
writer = pd.ExcelWriter(ime_datoteke + '.xlsx')
df.to_excel(writer, 'Sheet1')
writer.save()