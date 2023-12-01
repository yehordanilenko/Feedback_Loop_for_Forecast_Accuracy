import pandas as pd
from datetime import datetime


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


file_demand = 'Demand.xlsx'  # Name of demand file

# Read the Excel file into a Pandas DataFrame
data_demand = pd.read_excel(file_demand)


l1 = data_demand.values.tolist()  # list of demand file I work with him for finding number of weeks
sorted_list = sorted(l1, key=lambda x: x[1])  # sorted by data for getting n
n = (sorted_list[len(sorted_list)-1])[1].date() - (sorted_list[0])[1].date() # At first n is number of days between first and last dates
n = (n/7).days + 1 # We change n to count number of weeks
print("Number of weeks: ", n)

all_rows_as_list = data_demand.values.tolist() # dataframe demand to list

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

# Основной цикл уже для всего
for i in range(len(arr1)):
    if ((arr1[i])[0] not in setf):
        finalArray.append([(arr1[i])[0], count / n, 0 if sumDemand == 0 else count/sumDemand, countABSFCD/n])
        count = 0
        sumDemand = 0
        countABSFCD = 0

    setf.add((arr1[i])[0])

    if((arr1[i])[1] in arr2):
        if(len(arr1[i]) == 4):
            count+= (arr1[i])[2] - (arr1[i])[3]
            sumDemand+=(arr1[i])[3]
            countABSFCD += abs((arr1[i])[2] - (arr1[i])[3])
        else:
            count+= (arr1[i])[2]
            countABSFCD += abs((arr1[i])[2])


print(sumDemand)


for i in range(len(finalArray)-1):
    (finalArray[i])[1] = (finalArray[i+1])[1]
    (finalArray[i])[2] = (finalArray[i+1])[2]
    (finalArray[i])[3] = (finalArray[i + 1])[3]
(finalArray[len(finalArray)-1])[1] = count/n
(finalArray[len(finalArray)-1])[3] = countABSFCD/n


temp2 = []  # THIS FINAL LIST

for i in range(len(finalArray)):
    if((finalArray[i])[0] in arrTe):
        temp2.append(finalArray[i])
        (temp2[len(temp2)-1])[2] = round((finalArray[i])[2] * 100, 1)

for el in temp2:
    print(el)
print(len(temp2))