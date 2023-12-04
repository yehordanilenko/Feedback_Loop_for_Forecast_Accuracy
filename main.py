from collections import defaultdict

import pandas as pd
from datetime import datetime
import math
from statistics import mean

file_delfor = 'DELFOR2023.10.15.csv' # Name of delfor file

data_delfor = pd.read_csv(file_delfor, sep='|', header=None, skiprows=2) # Reading data from csv
data_delfor.columns = ['Col1','Col2','Col3','Col4','Col5','PrimeItem','Col7','Col8','Col9','Col10','Qty', 'Date', 'Col13'] # Assign a name for columns

data_delfor = data_delfor[data_delfor['Col1'] != 'DEL.01'] # Deleting all rows with PrimeItem name DEL.01
data_delfor = data_delfor[data_delfor['Col1'] != 'DEL.02'] # Deleting all rows with PrimeItem name DEL.01

data_delfor = data_delfor.iloc[:, [5, 10, 11]] # Leaving only the necessary columns

text_to_add = 'CIS-'
data_delfor['PrimeItem'] = text_to_add + data_delfor['PrimeItem'].astype(str) # Concatenate CIS- to PrimeItem

# Convert 'Column_C' from float to int
data_delfor['Qty'] = data_delfor['Qty'].fillna(-1).astype(int)
data_delfor['Date'] = data_delfor['Date'].fillna(-1).astype(int)

all_FC_list = data_delfor.values.tolist() # Convert our delfor dataframe to list
print("Length of FC delfor: ", len(all_FC_list))

for r in all_FC_list:
    date_number = r[2]  # Replace this with your integer representing the date
    # Convert the integer to a string and then to datetime64[ns]
    date_string = str(date_number)
    date_without_time = datetime.strptime(date_string, '%Y%m%d').date()
    dd = pd.Timestamp(date_without_time)
    r[2] = dd                                   # convert int to data


file_demand = 'demand_file.xlsx'  # Name of demand file

# Read the Excel file into a Pandas DataFrame
data_demand = pd.read_excel(file_demand, sheet_name='Closed_SSD')
data_demand_open = pd.read_excel(file_demand, sheet_name='Open_SSD')
print('**************************************')
print(data_demand_open)
print('**************************************')
l1 = data_demand.values.tolist()  # list of demand file I work with him for finding number of weeks
l2 = data_demand_open.values.tolist()

sorted_list = sorted(l1, key=lambda x: x[1])  # sorted by data for getting n
n = (sorted_list[len(sorted_list)-1])[1].date() - (sorted_list[0])[1].date() # At first n is number of days between first and last dates
n = (n/7).days + 1 # We change n to count number of weeks
print("Number of weeks: ", n)

list_of_demand_all = []

for i in range(len(l1)):
    for j in range(len(l2)):
        if(l1[i][0] == l2[j][0] and l1[i][1] == l2[j][1]):
            l1[i][2] += l2[j][2]
print(len(l1))
l11 = l1
for i in range(len(l2)):
    temp_c = 0
    for j in range(len(l1)):
        if(l2[i][0] == l1[j][0] and l2[i][1] == l1[j][1]):
            temp_c += 1
    if(temp_c == 0):
        l1.append(l2[i])
print(len(l1))

all_rows_as_list = l1 # data_demand.values.tolist() # dataframe demand to list

sorted_list_delfor = sorted(all_FC_list, key=lambda x: x[2]) # Sorting delfor by date
sorted_list_demand = sorted(all_rows_as_list, key=lambda x: x[1]) # Sorting demand by date
print("First element of delfor and demand list: ")
print(sorted_list_delfor[0], sorted_list_demand[0])
print("Size of delfor list and size of demand list: ")
print(len(all_FC_list), len(all_rows_as_list))


spec_data = (sorted_list_demand[len(sorted_list_demand) - 1])[1] # last date in demand list
temp_data = (sorted_list_delfor[len(sorted_list_delfor) - 1])[2] # last date in delfor list

arr1 = []   # list data FC before last date in demand including this date
for i in range(len(all_FC_list)):
    if((all_FC_list[i])[2] <= spec_data ):
        arr1.append(all_FC_list[i])

print("Amount items in delfor with dates before last date in demand: ")
print(len(arr1))

for l in arr1:
    l[1], l[2] = l[2], l[1]

for i in range(len(arr1)):
    for j in range(len(all_rows_as_list)):
        if((arr1[i])[0] == (all_rows_as_list[j])[0] and (arr1[i])[1] == (all_rows_as_list[j])[1]):
            arr1[i].append((all_rows_as_list[j])[2])

count = 0
setf = {''}

arr1 = sorted(arr1, key=lambda x: x[0])
arr2 = [item[1] for item in all_rows_as_list]
arrTe = [item[0] for item in all_rows_as_list]
finalArray = []

sumDemand = 1

countABSFCD = 0
sumDemAllPeriod = 1



# Основной цикл уже для всего
for i in range(len(arr1)):
    if ((arr1[i])[0] not in setf):
        RMSE = 123 if sumDemand == 0 else math.sqrt(((count*count)/n))
        RMSE_percent = 0 if sumDemAllPeriod == 0 else RMSE/(sumDemAllPeriod/n)
        BIAS = count / n
        MAE = countABSFCD/n
        SCORE = MAE + abs(BIAS)
        SCORE_percent = abs(0 if sumDemand == 0 else count / sumDemand) + (0 if sumDemAllPeriod == 0 else countABSFCD / sumDemAllPeriod)
        finalArray.append([(arr1[i])[0], BIAS, 0 if sumDemand == 0 else count / sumDemand, MAE , 0 if sumDemAllPeriod == 0 else countABSFCD / sumDemAllPeriod, RMSE, RMSE_percent, SCORE, SCORE_percent])
        count = 0
        sumDemand = 0
        countABSFCD = 0
        sumDemAllPeriod = 0

    setf.add((arr1[i])[0])

    if((arr1[i])[1] in arr2):
        if(len(arr1[i]) == 4):
            count+= (arr1[i])[2] - (arr1[i])[3]
            sumDemand+=(arr1[i])[3]
            countABSFCD += abs((arr1[i])[2] - (arr1[i])[3])
            sumDemAllPeriod+=(arr1[i])[3]
        else:
            count+= (arr1[i])[2]
            countABSFCD += abs((arr1[i])[2])


print(sumDemand)


for i in range(len(finalArray)-1):
    (finalArray[i])[1] = (finalArray[i + 1])[1]
    (finalArray[i])[2] = (finalArray[i + 1])[2]
    (finalArray[i])[3] = (finalArray[i + 1])[3]
    (finalArray[i])[4] = (finalArray[i + 1])[4]
    (finalArray[i])[5] = (finalArray[i + 1])[5]
    (finalArray[i])[6] = (finalArray[i + 1])[6]
    (finalArray[i])[7] = (finalArray[i + 1])[7]
    (finalArray[i])[8] = (finalArray[i + 1])[8]

(finalArray[len(finalArray)-1])[1] = count/n
(finalArray[len(finalArray)-1])[3] = countABSFCD/n
(finalArray[len(finalArray)-1])[5] = math.sqrt(((count*count)/n))
(finalArray[len(finalArray)-1])[6] = RMSE_percent
(finalArray[len(finalArray)-1])[7] = SCORE
(finalArray[len(finalArray)-1])[8] = SCORE_percent
temp2 = []  # THIS FINAL LIST

for i in range(len(finalArray)):
    if((finalArray[i])[0] in arrTe):
        temp2.append(finalArray[i])
        (temp2[len(temp2)-1])[2] = round((finalArray[i])[2] * 100, 1)
        (temp2[len(temp2) - 1])[4] = round((finalArray[i])[4] * 100, 1)
        (temp2[len(temp2) - 1])[6] = round((finalArray[i])[6] * 100, 1)
        (temp2[len(temp2) - 1])[8] = round((finalArray[i])[8] * 100, 1)

for el in temp2:
    print(el)
print(len(temp2))

print("Так теперь метрики ебать: ")
#print("Metrics of BIAS: ", mean([item[1] for item in temp2]))
print("Metrics of BIAS%: ", round(mean([item[2] for item in temp2]), 1))
#print("Metrics of MAE: ", mean([item[3] for item in temp2]))
print("Metrics of MAE%: ", round(mean([item[4] for item in temp2]), 1))
#print("Metrics of RMSE: ", mean([item[5] for item in temp2]))
print("Metrics of RMSE%: ", round(mean([item[6] for item in temp2]), 1))
#print("Metrics of SCORE: ", mean([item[7] for item in temp2]))
print("Metrics of SCORE%: ", round(mean([item[8] for item in temp2]), 1))

List_of_SKUs_with_demand_downside = []
List_of_SKUs_with_demand_upside = []

for el in temp2:
    if(el[2] > 5 ):
        List_of_SKUs_with_demand_downside.append([el[0], el[2]])
    elif(el[2] < -5):
        List_of_SKUs_with_demand_upside.append([el[0], el[2]])

print(f"Count of downside: {len(List_of_SKUs_with_demand_downside)} \nCount of upside: {len(List_of_SKUs_with_demand_upside)}")
print(f"Count of good bias: {len(temp2) - len(List_of_SKUs_with_demand_downside) - len(List_of_SKUs_with_demand_upside)}")

#print(List_of_SKUs_with_demand_downside)
#print(List_of_SKUs_with_demand_upside)


list_dates = []
c2 = 0
for i in sorted_list_demand:
    print(i)
print(len(sorted_list_demand))

sum_by_date = defaultdict(int)

# Calculating sum of integers for each date
for item in sorted_list_demand:
    date = item[1]  # Assuming the date is at index 1
    value = item[2]  # Assuming the integer is at index 2
    sum_by_date[date] += value

# Displaying sums for each date
# Creating a list of lists containing date and total
date_total_list = [ total for total in sum_by_date.items()]

# Extracting only the totals
totals_only = [total for _, total in date_total_list]

# Displaying the list of totals
print(totals_only)

#print(len(all_rows_as_list))


integers_list = [sublist[2] for sublist in all_rows_as_list]

from scipy.stats import kendalltau
import numpy as np
import matplotlib.pyplot as plt
from pandas import Timestamp

# Ваш лист с данными
data = all_rows_as_list

# Преобразование дат в формат Timestamp и количеств в массивы numpy
dates = np.array([row[1] for row in data])
qty = np.array([row[2] for row in data])

# Выполнение теста Кендалла
tau, p_value = kendalltau(qty, range(len(qty)))

# Определение направления тренда
trend_direction = "Upward" if tau > 0 else "Downward" if tau < 0 else "No Trend"

# Вывод результатов
print(f"Trend Direction: {trend_direction}")
print(f"Kendall's Tau: {tau}")
print(f"P-value: {p_value}")

# Постройте график данных
plt.plot(dates, qty, marker='o', label='Actual Demand')
plt.title('Demand Over Time')
plt.xlabel('Date')
plt.ylabel('Demand')
plt.legend()
plt.show()
import pandas as pd
from scipy.stats import kendalltau

# Предположим, что у вас есть DataFrame с данными в листе1
# Замените 'your_data.csv' на путь к вашему файлу или используйте другие способы загрузки данных

# Предположим, что у вас есть два столбца 'X' и 'Y', и вы хотите проверить тренд в 'Y' относительно 'X'
x_values = totals_only
y_values = [num for num in range(len(totals_only))]

# Выполняем тест Кендалла
tau, p_value = kendalltau(x_values, y_values)

# Выводим результаты теста
print(f"Значение статистики Кендалла (τ): {tau}")
print(f"P-значение: {p_value}")

# Проверяем значимость
if p_value < 0.05:
    print("Отвергаем нулевую гипотезу, есть тренд.")
else:
    print("Нет оснований отвергнуть нулевую гипотезу, тренд отсутствует.")

import numpy as np
import matplotlib.pyplot as plt

x = np.array([num for num in range(len(totals_only))])
y = np.array(totals_only)


plt.plot(x, y)
plt.show()
#print(f"P-value: {result.p}")

import pandas as pd
from scipy.stats import kendalltau

# Example list of lists
data = all_rows_as_list

# Convert the list of lists to a DataFrame
df = pd.DataFrame(data, columns=['Label', 'Timestamp', 'Value'])

# Convert Timestamp column to datetime if needed
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Compute Kendall's tau correlation between Timestamp and Value columns
tau, p_value = kendalltau(df['Timestamp'], df['Value'])

print(f"Kendall's Tau: {tau}")
print(f"P-value: {p_value}")
