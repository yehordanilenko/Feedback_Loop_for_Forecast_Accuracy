from collections import defaultdict
import pandas as pd
from datetime import datetime
import math
from statistics import mean

file_delfor = 'DELFOR2023.10.15.csv' # Name of delfor file
file_demand = 'demand_file.xlsx'  # Name of demand file


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
print("====================================================================================")
print("Length of FC delfor: ", len(all_FC_list))
print("====================================================================================")

for r in all_FC_list:
    date_number = r[2]  # Replace this with your integer representing the date
    # Convert the integer to a string and then to datetime64[ns]
    date_string = str(date_number)
    date_without_time = datetime.strptime(date_string, '%Y%m%d').date()
    dd = pd.Timestamp(date_without_time)
    r[2] = dd                                   # convert int to data


# Read the Excel file into a Pandas DataFrame
data_demand = pd.read_excel(file_demand, sheet_name='Closed_SSD')
data_demand_open = pd.read_excel(file_demand, sheet_name='Open_SSD')
l1 = data_demand.values.tolist()  # list of demand file I work with him for finding number of weeks
l2 = data_demand_open.values.tolist()

sorted_list_delfor = sorted(all_FC_list, key=lambda  x: x[2]) # sorted by dates delfor
#print(sorted_list_delfor[0][2])
sorted_list = sorted(l1, key=lambda x: x[1]) # sorted by date demand
min_date = sorted_list_delfor[0][2] if sorted_list_delfor[0][2] > sorted_list[0][1] else sorted_list[0][1]
#print(sorted_list_delfor[0][2] > sorted_list[0][1])
#print(min_date)
n = (sorted_list[len(sorted_list)-1])[1].date() - min_date.date() # At first n is number of days between first and last dates
n = (n/7).days + 1 # We change n to count number of weeks
print("====================================================================================")
print("Number of weeks: ", n)
#print("====================================================================================")

list_of_demand_all = []

for i in range(len(l1)):
    for j in range(len(l2)):
        if(l1[i][0] == l2[j][0] and l1[i][1] == l2[j][1]):
            l1[i][2] += l2[j][2]


for i in range(len(l2)):
    temp_c = 0
    for j in range(len(l1)):
        if(l2[i][0] == l1[j][0] and l2[i][1] == l1[j][1]):
            temp_c += 1
    if(temp_c == 0):
        l1.append(l2[i])

#print("====================================================================================")
print("Number of demand data: ",len(l1))
print("====================================================================================")

all_rows_as_list = l1 # data_demand.values.tolist() # dataframe demand to list

sorted_list_delfor = sorted(all_FC_list, key=lambda x: x[2]) # Sorting delfor by date
sorted_list_demand = sorted(all_rows_as_list, key=lambda x: x[1]) # Sorting demand by date
# print("First element of delfor and demand list: ")
# print(sorted_list_delfor[0], sorted_list_demand[0])
print("====================================================================================")
print("Size of delfor list and size of demand list: ")
print(len(all_FC_list), len(all_rows_as_list))
print("====================================================================================")


spec_data = (sorted_list_demand[len(sorted_list_demand) - 1])[1] # last date in demand list
temp_data = (sorted_list_delfor[len(sorted_list_delfor) - 1])[2] # last date in delfor list

arr1 = []   # list data FC before last date in demand including this date
for i in range(len(all_FC_list)):
    if((all_FC_list[i])[2] <= spec_data ):
        arr1.append(all_FC_list[i])

print("====================================================================================")
print("Amount items in delfor with dates before last date in demand: ")
print(len(arr1))
print("====================================================================================")

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

sumDemand = 0

countABSFCD = 0
sumDemAllPeriod = 1
forecast_allPer = 0

List_of_SKUs_with_some_D_but_0_FCST = []
list_of_demands_and_delfors = []
# Основной цикл уже для всего
for i in range(len(arr1)):
    if ((arr1[i])[0] not in setf):
        # if(sumDemand > 0 and forecast_allPer == 0):
        #     List_of_SKUs_with_some_D_but_0_FCST.append((arr1[i])[0])
        BIAS = count / n
        MAE = countABSFCD / n
        RMSE = math.sqrt(((count*count)/n))
        RMSE_percent = RMSE if sumDemAllPeriod == 0 else RMSE/(sumDemAllPeriod/n)
        SCORE = MAE + abs(BIAS)
        SCORE_percent = abs(BIAS if sumDemand == 0 else count / sumDemand) + (MAE if sumDemAllPeriod == 0 else countABSFCD / sumDemAllPeriod)
        list_of_demands_and_delfors.append([sumDemand, forecast_allPer])
        last_for_demand = sumDemand
        last_for_FC = forecast_allPer
        finalArray.append([(arr1[i])[0], BIAS, BIAS if sumDemand == 0 else count / sumDemand, MAE , MAE if sumDemAllPeriod == 0 else countABSFCD / sumDemAllPeriod, RMSE, RMSE_percent, SCORE, SCORE_percent])
        count = 0
        sumDemand = 0
        countABSFCD = 0
        sumDemAllPeriod = 0
        forecast_allPer = 0

    setf.add((arr1[i])[0])

    if((arr1[i])[1] in arr2):
        if(len(arr1[i]) == 4):
            count+= (arr1[i])[2] - (arr1[i])[3]
            sumDemand+=(arr1[i])[3]
            countABSFCD += abs((arr1[i])[2] - (arr1[i])[3])
            sumDemAllPeriod+=(arr1[i])[3]
            forecast_allPer += (arr1[i])[2]
        else:
            count+= (arr1[i])[2]
            countABSFCD += abs((arr1[i])[2])
            forecast_allPer += (arr1[i])[2]


for i in range(len(finalArray)-1):
    (finalArray[i])[1] = (finalArray[i + 1])[1]
    (finalArray[i])[2] = (finalArray[i + 1])[2]
    (finalArray[i])[3] = (finalArray[i + 1])[3]
    (finalArray[i])[4] = (finalArray[i + 1])[4]
    (finalArray[i])[5] = (finalArray[i + 1])[5]
    (finalArray[i])[6] = (finalArray[i + 1])[6]
    (finalArray[i])[7] = (finalArray[i + 1])[7]
    (finalArray[i])[8] = (finalArray[i + 1])[8]
    (list_of_demands_and_delfors[i])[0] = (list_of_demands_and_delfors[i+1])[0]
    (list_of_demands_and_delfors[i])[1] = (list_of_demands_and_delfors[i+1])[1]

(finalArray[len(finalArray)-1])[1] = count/n
(finalArray[len(finalArray)-1])[3] = countABSFCD/n
(finalArray[len(finalArray)-1])[5] = math.sqrt(((count*count)/n))
(finalArray[len(finalArray)-1])[6] = RMSE_percent
(finalArray[len(finalArray)-1])[7] = SCORE
(finalArray[len(finalArray)-1])[8] = SCORE_percent
(list_of_demands_and_delfors[i])[0] = last_for_demand
(list_of_demands_and_delfors[i])[1] = last_for_FC

for i in range(len(list_of_demands_and_delfors)):
    if(list_of_demands_and_delfors[i][0] > 0 and list_of_demands_and_delfors[i][1] == 0):
        List_of_SKUs_with_some_D_but_0_FCST.append(finalArray[i][0])



temp2 = []  # THIS FINAL LIST

for i in range(len(finalArray)):
    if((finalArray[i])[0] in arrTe):
        temp2.append(finalArray[i])
        (temp2[len(temp2)-1])[2] = round((finalArray[i])[2] * 100, 1)
        (temp2[len(temp2) - 1])[4] = round((finalArray[i])[4] * 100, 1)
        (temp2[len(temp2) - 1])[6] = round((finalArray[i])[6] * 100, 1)
        (temp2[len(temp2) - 1])[8] = round((finalArray[i])[8] * 100, 1)


print("====================================================================================")
for el in temp2:
    print(el)             # ЭТО ВСЁ ИТОГОВЫЙ ТО ЧТО ПЕРВАЯ ЗАДАЧА
print(len(temp2))
print("====================================================================================")


print("====================================================================================")
print("Metrices: ")
#print("Metrics of BIAS: ", mean([item[1] for item in temp2]))
print("Metrics of BIAS%: ", round(mean([item[2] for item in temp2]), 1), "%")
#print("Metrics of MAE: ", mean([item[3] for item in temp2]))
print("Metrics of MAE%: ", round(mean([item[4] for item in temp2]), 1), "%")
#print("Metrics of RMSE: ", mean([item[5] for item in temp2]))
print("Metrics of RMSE%: ", round(mean([item[6] for item in temp2]), 1), "%")
#print("Metrics of SCORE: ", mean([item[7] for item in temp2]))
print("Metrics of SCORE%: ", round(mean([item[8] for item in temp2]), 1), "%")
print("====================================================================================")


List_of_SKUs_with_demand_downside = []
List_of_SKUs_with_demand_upside = []
perfect_demand = []

for el in temp2:
    if(el[2] > 5 ):
        List_of_SKUs_with_demand_downside.append([el[0], el[2]])
    elif(el[2] < -5):
        List_of_SKUs_with_demand_upside.append([el[0], el[2]])
    else:
        perfect_demand.append([el[0],el[2]])

print("====================================================================================")
print(f"Count of downside: {len(List_of_SKUs_with_demand_downside)}")
print(List_of_SKUs_with_demand_downside)
print(f"\nCount of upside: {len(List_of_SKUs_with_demand_upside)}")
print(List_of_SKUs_with_demand_upside)
print(f"\nCount of good bias: {len(temp2) - len(List_of_SKUs_with_demand_downside) - len(List_of_SKUs_with_demand_upside)}")
print(perfect_demand)
print("====================================================================================")
print("====================================================================================")
print("List demand > 0 and FC = 0: ")
#print(len(List_of_SKUs_with_some_D_but_0_FCST))
print(List_of_SKUs_with_some_D_but_0_FCST)
print(f"Length of this items: {len(List_of_SKUs_with_some_D_but_0_FCST)}")
print("====================================================================================")
#print(List_of_SKUs_with_demand_downside)
#print(List_of_SKUs_with_demand_upside)

from openpyxl import Workbook

# Work with write in file
data = temp2
data222 = List_of_SKUs_with_demand_downside
data333 = List_of_SKUs_with_demand_upside
columns1 = ['PrimeItem','Bias','Bias%','MAE','MAE%','RMSE','RMSE%','Score','Score%']
# Create a new workbook and select the active worksheet
workbook = Workbook()
sheet1 = workbook.active
sheet1.title = 'All_data'
# Write column names to Sheet 1
sheet1.append(columns1)
# Write data to the worksheet
for row in data:
    sheet1.append(row)

# Create Sheet 2
sheet2 = workbook.create_sheet(title='SKU')
sheet2.append(['List_of_SKUs_with_demand_downside','','List_of_SKUs_with_demand_upside',''])
columns2 = ['PrimeItem', 'BIAS%', 'PrimeItem', 'BIAS%']
sheet2.append(columns2)

#if(len(data222) >= len(len(data333))):
combined_list = []

for i in range(max(len(data222), len(data333))):
    item_1 = data222[i] if i < len(data222) else ["", ""]
    item_2 = data333[i] if i < len(data333) else ["", ""]
    combined_list.append(item_1 + item_2)

#print(combined_list)
# Write data to Sheet 2
for row in combined_list:
    sheet2.append(row)

sheet2.append([])

sheet3 = workbook.create_sheet(title='хуйня_ой')
sheet3.append(['List items demand > 0 and FCST =0'])
sheet3.append(['PrimeItem'])
for row in List_of_SKUs_with_some_D_but_0_FCST:
    sheet3.append([row])
# Save the workbook
workbook.save(filename='output.xlsx')

sheet3.append([])

#
# list_dates = []
# c2 = 0
# # for i in sorted_list_demand:
# #     print(i)
# #print(len(sorted_list_demand))
#
# sum_by_date = defaultdict(int)
#
# # Calculating sum of integers for each date
# for item in sorted_list_demand:
#     date = item[1]  # Assuming the date is at index 1
#     value = item[2]  # Assuming the integer is at index 2
#     sum_by_date[date] += value
#
# # Displaying sums for each date
# # Creating a list of lists containing date and total
# date_total_list = [ total for total in sum_by_date.items()]
#
# # Extracting only the totals
# totals_only = [total for _, total in date_total_list]

# Displaying the list of totals
#print(totals_only)

