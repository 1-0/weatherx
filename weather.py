import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# http://rp5.ua/archive.php?wmo_id=34300&lang=ru
# lt_kh - local Kharkov Time, a30 - end
COLUM_NAME = [
    "lt_kh","T","Po","P","Pa","U","DD","Ff","ff10","ff3","N","WW","W1","W2","Tn","Tx","Cl","Nh","H","Cm","Ch","VV","Td","RRR","tR","E","Tg","E'","sss","a30"
    ]


def show_extrems_column(df, freq, column, maximum):
    dataframe = df.groupby(pd.Grouper(key="lt_kh", freq=freq)).mean()
    if maximum:
        data = np.max(dataframe,axis=0)
    else:
        data = np.min(dataframe,axis=0)
    arr = dataframe[column]
    d = np.where(arr==data[column])
    
    try:
        res1, res2 = int(d[-1]), data[column]
    except TypeError:
        res1, res2 = d, data[column]
    return res1, res2 

# 1. Найти самый ветреный месяц - (месяц и средняя скорость ветра)
# 2. Найти самый холодный месяц - (месяц и средняя температура)
# 3. Найти самый холодный день - (день и средняя температура)
# 4. Найти самый тёплый месяц - (месяц и средняя температура)
# 5. Найти самый тёплый день - (день и средняя температура)
# 6. Найти самую дождливую неделю - (период и количество осадков)
if __name__ == "__main__":
    d = pd.read_csv(
                       '34300.01.01.2016.01.01.2017.1.0.0.ru.csv.gz', 
                       comment='#', 
                       parse_dates=[0, ], 
                       skiprows=[0, 1, 2, 3 , 4, 5, 6],
                       delimiter=';',
                       names = COLUM_NAME,
                       compression='gzip',
                       error_bad_lines=False
                      )

    print("#1. Найти самый ветреный месяц - (месяц и средняя скорость ветра)", show_extrems_column(d, '1M', 'Ff', maximum = True))
    print("#2. Найти самый холодный месяц - (месяц и средняя температура)", show_extrems_column(d, '1M', 'T', maximum = False))
    print("#3. Найти самый холодный день - (день и средняя температура)", show_extrems_column(d, '1D', 'T', maximum = False))
    print("#4. Найти самый тёплый месяц - (месяц и средняя температура)", show_extrems_column(d, '1M', 'T', maximum = True))
    print("#5. Найти самый тёплый день - (день и средняя температура)", show_extrems_column(d, '1D', 'T', maximum = True))
    print("#6. Найти самую дождливую неделю - (период и количество осадков)", show_extrems_column(d, '1W', 'tR', maximum = True))
