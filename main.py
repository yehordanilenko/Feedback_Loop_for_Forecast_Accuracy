from collections import defaultdict
import pandas as pd
from datetime import datetime
import math
from statistics import mean
from openpyxl import Workbook

file_delfor = 'DELFOR 2023.10.09.csv' # Name of delfor file
file_demand = 'Forecast vs Target SSD Demand V2.2.xlsx'  # Name of demand file


data_delfor = pd.read_csv(file_delfor, sep='|', header=None, skiprows=2) # Reading data from csv
data_delfor.columns = ['Col1','Col2','Col3','Col4','Col5','PrimeItem','Col7','Col8','Col9','Col10','Qty', 'Date', 'Col13'] # Assign a name for columns

data_delfor = data_delfor[data_delfor['Col1'] != 'DEL.01'] # Deleting all rows with PrimeItem name DEL.01
data_delfor = data_delfor[data_delfor['Col1'] != 'DEL.02'] # Deleting all rows with PrimeItem name DEL.01

data_delfor = data_delfor.iloc[:, [5, 10, 11]] # Leaving only the necessary columns

text_to_add = 'CIS-'
data_delfor['PrimeItem'] = text_to_add + data_delfor['PrimeItem'].astype(str) # Concatenate CIS- to PrimeItem

# Convert columns from float to int
data_delfor['Qty'] = data_delfor['Qty'].fillna(-1).astype(int)
data_delfor['Date'] = data_delfor['Date'].fillna(-1).astype(int)

import pandas as pd

# Load the DELFOR data (assuming it's already loaded as data_delfor)
# data_delfor = pd.read_csv('your_delfor_file.csv')  # Replace with your file name if not loaded

# Load the ItemSubstitutes CSV file
file_second = 'FCS_VRY_ItemSubstitutes.csv'
data_second = pd.read_csv(file_second, delimiter='|')

# Strip leading and trailing spaces from the 'Item Code' column
data_second['Item Code'] = data_second['Item Code'].str.strip()

import pandas as pd

# Load the DELFOR data and ItemSubstitutes CSV file (Assuming it's already loaded)
# data_delfor = pd.read_csv('your_delfor_file.csv')  # Replace with your file name if not loaded

# Load the ItemSubstitutes CSV file
file_second = 'FCS_VRY_ItemSubstitutes.csv'
data_second = pd.read_csv(file_second, delimiter='|')

# Strip leading and trailing spaces from the 'Item Code' column
data_second['Item Code'] = data_second['Item Code'].str.strip()

# Merge the two DataFrames
merged_data = pd.merge(data_delfor, data_second, left_on='PrimeItem', right_on='Item Code', how='left')

# Fill NaN values in 'Priority' and 'Record No.' columns
merged_data['Priority'] = merged_data['Priority'].fillna(-1).astype(int)
merged_data['Record No.'] = merged_data['Record No.'].fillna(-1).astype(int)

# Drop unnecessary columns
merged_data = merged_data.drop(['Item Code'], axis=1)

# Group by 'Record No.', 'Date', and 'PrimeItem', and aggregate
grouped_data = merged_data.groupby(['Record No.', 'Date', 'PrimeItem']).agg({
    'Qty': 'sum',
    'Priority': 'first'
}).reset_index()

# Identify groups that need a priority 1 item
group_keys = grouped_data.groupby(['Record No.', 'Date'])['Priority']
need_priority_1 = group_keys.transform(lambda x: 1 not in x)

# Use boolean indexing to filter rows
priority_1_rows = grouped_data[need_priority_1].copy()
priority_1_rows['Qty'] = 0
priority_1_rows['Priority'] = 1

# Concatenate the original and new priority 1 rows
final_data = pd.concat([grouped_data, priority_1_rows], ignore_index=True)

# Sort and reset index if needed
final_data = final_data.sort_values(by=['Record No.', 'Date', 'PrimeItem']).reset_index(drop=True)

# Drop 'Priority' and 'Record No.' columns
final_data = final_data.drop(['Priority', 'Record No.'], axis=1)

# Print or use the resulting DataFrame as needed
print(final_data)




# Print or use the resulting DataFrame as needed
#priority_diff_than_minus_one = merged_data[merged_data['Priority'] != -1].shape[0]
#print("Number of rows with Priority different than -1:", priority_diff_than_minus_one)
listx = final_data.values.tolist()

# Initialize a new list to store the filtered data
filtered_list = []

# Create a set to track seen combinations of date and itemname
seen = set()

for item in listx:
    date, itemname, qty = item

    # Construct a unique identifier for each date and itemname combination
    identifier = (date, itemname)

    # Add to filtered list if it's the first occurrence or if qty is non-zero
    if identifier not in seen or qty != 0:
        filtered_list.append(item)
        seen.add(identifier)

# Now filtered_list contains the desired data without unwanted duplicates
# If you want to calculate the total qty again, you can do so with the filtered data
total_qty = sum(item[2] for item in filtered_list)

print(f"Total Quantity: {total_qty}")
print(f"Filtered Data Length: {len(filtered_list)}")


print("Length our new я удалил дубликаты",len(filtered_list))
# for huy in new_temp_list:
#     print(huy)

workbook2 = Workbook()
sheet111 = workbook2.active
sheet111.title = 'All_data'
cols1 = ['Date', 'Item', 'Qty']
# Write column names to Sheet 1
sheet111.append(cols1)
# Write data to the worksheet
for row in filtered_list:
    sheet111.append(row)



# Save the workbook
workbook2.save(filename='delforchick.xlsx')


#all_FC_list = merged_data.values.tolist() # Convert our delfor dataframe to list
all_FC_list = filtered_list
for sublist in all_FC_list:
    sublist[0], sublist[1] = sublist[1], sublist[0]

for sublist in all_FC_list:
    sublist[1], sublist[2] = sublist[2], sublist[1]
print("====================================================================================")
print("Length of FC delfor: ", len(all_FC_list))
print("====================================================================================")

for r in all_FC_list:
    date_number = r[2]
    # Convert the integer to a string and then to datetime64[ns](date type)
    date_string = str(date_number)
    date_without_time = datetime.strptime(date_string, '%Y%m%d').date()
    dd = pd.Timestamp(date_without_time)
    r[2] = dd                                   # convert int to data


# Read the Excel file into a Pandas DataFrame
data_demand = pd.read_excel(file_demand, sheet_name='TransactionHistory') #CLOSED SSD
data_demand_open = pd.read_excel(file_demand, sheet_name='PlannedTransactions') #OPEN SSD
l1 = data_demand.values.tolist()  # list of demand closed ssd file I work with it for find number of weeks
l2 = data_demand_open.values.tolist() # list of demand open ssd file I work with it to find number of weeks

sorted_list_delfor = sorted(all_FC_list, key=lambda  x: x[2]) # sorted by dates delfor

sorted_list = sorted(l1, key=lambda x: x[1]) # sorted by date demand
sorted_list2 = sorted(l2, key=lambda x: x[1])# sorted by date demand
min_date = sorted_list_delfor[0][2] if sorted_list_delfor[0][2] > sorted_list[0][1] else sorted_list[0][1] # finding minimum date  between delfor and demand
print(l1[0])
print("MIN DATE", min_date)
current_date = datetime(2023, 12, 11).date()#datetime.today().date() # CURRENT DATE
print("Current date (we do it by self)", current_date)
# print((sorted_list2[len(sorted_list2)-1])[1].date())
# print(current_date - (sorted_list2[len(sorted_list2)-1])[1].date())
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
list_bef_cur_date = [] # list of dates less or equal curr date
for el in l1:   # process of getting list with data where date less or equal exact(current) date
    if(el[1].date() <= current_date):
        list_bef_cur_date.append(el)

list_bef_cur_date.sort(key=lambda x: x[1])
workbook3 = Workbook()
shee = workbook3.active
# Write data to the worksheet
for row in list_bef_cur_date:
    shee.append(row)
# Save the workbook
workbook3.save(filename='demand_proverka.xlsx')

name_sum_dict = []  # Initialize as a list

dem_cop = list_bef_cur_date.copy()

# Calculate the cumulative sum for each name
for sublist in dem_cop:
    name = sublist[0]
    value = sublist[2]

    # Check if the name is already in the list
    name_exists = False
    for entry in name_sum_dict:
        if entry[0] == name:
            entry[1] += value
            name_exists = True
            break

    # If the name is not in the list, append a new entry
    if not name_exists:
        name_sum_dict.append([name, value])

# Print the result
#print(name_sum_dict)


# Extract unique names from name_sum_dict
unique_names_in_dict = set(name for name, _ in name_sum_dict)

# Create a new list of names that are in name_sum_dict but not in list2

print("length filtered data", len(filtered_list))
#print([item[0] for item in filtered_list])
extra_list = [name for name in unique_names_in_dict if name not in [item[0] for item in filtered_list]]
print(len(name_sum_dict))
# Print the result
print(len(extra_list), extra_list)

print("Number of demand data: ",len(list_bef_cur_date))
print("Number of prev try for demand (not using current date)", len(l1))
sorted_list_demand_before_cur_d = sorted(list_bef_cur_date, key=lambda x: x[1]) # sorted demand list
n = sorted_list_demand_before_cur_d[len(sorted_list_demand_before_cur_d) - 1][1].date() - min_date.date() # At first n is number of days between first and last dates
n = (n/7).days + 1 # We change n to count number of weeks
print("Number of weeks: ", n)
print("====================================================================================")

all_rows_as_list = list_bef_cur_date # data_demand.values.tolist() # dataframe demand to list

sorted_list_delfor = sorted(all_FC_list, key=lambda x: x[2]) # Sorting delfor by date
sorted_list_demand = sorted(all_rows_as_list, key=lambda x: x[1]) # Sorting demand by date
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

for l in arr1:    # I change rows date and qty for easier calculating in future
    l[1], l[2] = l[2], l[1]

for i in range(len(arr1)):     # I combine in delfor list qty from demand list to next process working
    for j in range(len(all_rows_as_list)):
        if((arr1[i])[0] == (all_rows_as_list[j])[0] and (arr1[i])[1] == (all_rows_as_list[j])[1]):
            arr1[i].append((all_rows_as_list[j])[2])

count = 0
setf = {''}

arr1 = sorted(arr1, key=lambda x: x[0])  # Sorting list by PrimeItem
arr2 = [item[1] for item in all_rows_as_list]
arrTe = [item[0] for item in all_rows_as_list]
finalArray = []

sumDemand = 0
countABSFCD = 0
countsq = 0
sumDemAllPeriod = 1
forecast_allPer = 0
list_temp10 = []
List_of_SKUs_with_some_D_but_0_FCST = []
list_of_demands_and_delfors = []
print("FIRST DATA", arr1[0])
print(len(arr1))
print("LAST DATA",arr1[len(arr1)-1])
# Main loop of calculation
for i in range(len(arr1)):
    if ((arr1[i])[0] not in setf):
        BIAS = count / n
        BIAS_percent = BIAS if sumDemand == 0 else count/sumDemand
        MAE = countABSFCD / n
        RMSE = math.sqrt(countsq / n)
        RMSE_percent = RMSE if sumDemAllPeriod == 0 else RMSE/(sumDemAllPeriod/n)
        SCORE = MAE + abs(BIAS)
        SCORE_percent = abs(BIAS if sumDemand == 0 else count / sumDemand) + (MAE if sumDemAllPeriod == 0 else countABSFCD / sumDemAllPeriod)
        list_of_demands_and_delfors.append([sumDemand, forecast_allPer])
        last_for_demand = sumDemand
        last_for_FC = forecast_allPer
        finalArray.append([(arr1[i])[0], BIAS, BIAS_percent, MAE , MAE if sumDemAllPeriod == 0 else countABSFCD / sumDemAllPeriod, RMSE, RMSE_percent, SCORE, SCORE_percent])
        if(i == len(arr1)-1):
            break
        count = 0
        countsq = 0
        sumDemand = 0
        countABSFCD = 0
        sumDemAllPeriod = 0
        forecast_allPer = 0

    setf.add((arr1[i])[0])

    if((arr1[i])[1] in arr2):
        if(len(arr1[i]) == 4):
            count+= (arr1[i])[2] - (arr1[i])[3]
            countsq+= ((arr1[i])[2] - (arr1[i])[3])**2
            sumDemand+=(arr1[i])[3]
            countABSFCD += abs((arr1[i])[2] - (arr1[i])[3])
            sumDemAllPeriod+=(arr1[i])[3]
            forecast_allPer += (arr1[i])[2]
            if(arr1[i][0] in arrTe):
                list_temp10.append([arr1[i][0], arr1[i][1], arr1[i][2], arr1[i][3]])
        else:
            count+= (arr1[i])[2]
            countsq+= ((arr1[i])[2])**2
            countABSFCD += abs((arr1[i])[2])
            forecast_allPer += (arr1[i])[2]
            if (arr1[i][0] in arrTe):
                list_temp10.append([arr1[i][0], arr1[i][1], arr1[i][2]])

# print("lentgh govna: ", len(list_temp10))
# for element in list_temp10:
#     print(element)

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
(finalArray[len(finalArray)-1])[2] = BIAS_percent
(finalArray[len(finalArray)-1])[3] = countABSFCD/n
(finalArray[len(finalArray)-1])[5] = math.sqrt(countsq/n)
(finalArray[len(finalArray)-1])[6] = RMSE_percent
(finalArray[len(finalArray)-1])[7] = SCORE
(finalArray[len(finalArray)-1])[8] = SCORE_percent
(list_of_demands_and_delfors[i])[0] = last_for_demand
(list_of_demands_and_delfors[i])[1] = last_for_FC

# print("FINAL ARRAY: size is \n", len(finalArray))
# for el in finalArray:
#     print(el)

for i in range(len(list_of_demands_and_delfors)):
    if(list_of_demands_and_delfors[i][0] > 0 and list_of_demands_and_delfors[i][1] == 0):
        List_of_SKUs_with_some_D_but_0_FCST.append(finalArray[i][0])



finalArray.pop()

temp2 = []  # THIS FINAL LIST

for i in range(len(finalArray)):
    if((finalArray[i])[0] in arrTe):
        temp2.append(finalArray[i])
        if((temp2[len(temp2) - 1])[2] != (temp2[len(temp2) - 1])[1]):
            (temp2[len(temp2)-1])[2] = round((finalArray[i])[2] * 100, 1)
        if((temp2[len(temp2) - 1])[4] != (temp2[len(temp2) - 1])[3]):
            (temp2[len(temp2) - 1])[4] = round((finalArray[i])[4] * 100, 1)
        if((temp2[len(temp2) - 1])[6] != (temp2[len(temp2) - 1])[5]):
            (temp2[len(temp2) - 1])[6] = round((finalArray[i])[6] * 100, 1)
        if((temp2[len(temp2) - 1])[8] != (temp2[len(temp2) - 1])[7]):
            (temp2[len(temp2) - 1])[8] = round((finalArray[i])[8] * 100, 1)


print("====================================================================================")
from tabulate import tabulate
col_names = ['PrimeItem', 'BIAS', 'Bias%', 'MAE', 'MAE%', 'RMSE', 'RMSE%', 'SCORE', 'SCORE%']
print(tabulate(temp2, headers=col_names, tablefmt='pretty'))
print(len(temp2))
# print(temp2[(len(temp2)-1)])

# for element in temp2:
#     print(element)

print("====================================================================================")
print("Metrics: ")
#print("Metrics of BIAS: ", mean([item[1] for item in temp2]))
print("Average BIAS%: ", round(mean([item[2] for item in temp2]), 1), "%")
#print("Metrics of MAE: ", mean([item[3] for item in temp2]))
print("Average MAE%: ", round(mean([item[4] for item in temp2]), 1), "%")
#print("Metrics of RMSE: ", mean([item[5] for item in temp2]))
print("Average RMSE%: ", round(mean([item[6] for item in temp2]), 1), "%")
#print("Metrics of SCORE: ", mean([item[7] for item in temp2]))
print("Average SCORE%: ", round(mean([item[8] for item in temp2]), 1), "%")



List_of_SKUs_with_demand_downside = []
List_of_SKUs_with_demand_upside = []
perfect_demand = []

for el in temp2:
    if(el[2] > 30 ):
        List_of_SKUs_with_demand_downside.append([el[0], el[2]])
    elif(el[2] < -30):
        List_of_SKUs_with_demand_upside.append([el[0], el[2]])
    else:
        perfect_demand.append([el[0],el[2]])

print("====================================================================================")
print(f"Number of demand downsides: {len(List_of_SKUs_with_demand_downside)}")
print(List_of_SKUs_with_demand_downside)
print(f"\nNumber of demand upsides: {len(List_of_SKUs_with_demand_upside)}")
print(List_of_SKUs_with_demand_upside)
print(f"\nNumber of good bias: {len(temp2) - len(List_of_SKUs_with_demand_downside) - len(List_of_SKUs_with_demand_upside)}")
print(perfect_demand)
print("====================================================================================")

print("List demand > 0 and FC = 0: ")
List_of_SKUs_with_some_D_but_0_FCST.extend(extra_list)
#print(List_of_SKUs_with_some_D_but_0_FCST)
# Remove duplicates from original_list in place
List_of_SKUs_with_some_D_but_0_FCST = [item for index, item in enumerate(List_of_SKUs_with_some_D_but_0_FCST) if item not in List_of_SKUs_with_some_D_but_0_FCST[:index]]

# Print the result
print(f"Length of this items: {len(List_of_SKUs_with_some_D_but_0_FCST)}")
print(List_of_SKUs_with_some_D_but_0_FCST)
print("====================================================================================")



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
sheet2 = workbook.create_sheet(title='Problematic SKUs')
sheet2.append(['List_of_SKUs_with_demand_downside','','List_of_SKUs_with_demand_upside',''])
columns2 = ['PrimeItem (downsides)', 'BIAS% for downsides' , 'PrimeItem (downsides)', 'BIAS% for upsides']
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

sheet3 = workbook.create_sheet(title='Items with some D but 0 FCST')
sheet3.append(['List items demand > 0 and FCST =0'])
sheet3.append(['PrimeItem'])
for row in List_of_SKUs_with_some_D_but_0_FCST:
    sheet3.append([row])

sheet4 = workbook.create_sheet(title='D vs FC')
sheet4.append(['PrimeItem', 'Date', 'FC', 'Demand'])

for row in list_temp10:
    sheet4.append(row)
# Save the workbook
workbook.save(filename='test.xlsx')

sheet3.append([])
