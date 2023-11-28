import pandas as pd
from datetime import datetime

file_delfor = 'DELFOR2023.10.15.csv'  # Replace with your file path

# Read the CSV file, skipping the first two rows
#data_delfor = pd.read_csv(file_delfor, sep='|', usecols=[5, 10, 11], header=None, skiprows=2)
data_delfor = pd.read_csv(file_delfor, sep='|', header=None, skiprows=2)
data_delfor.columns = ['Col1','Col2','Col3','Col4','Col5','PrimeItem','Col7','Col8','Col9','Col10','Qty', 'Date', 'Col13']

data_delfor = data_delfor[data_delfor['Col1'] != 'DEL.01']
data_delfor = data_delfor[data_delfor['Col1'] != 'DEL.02']

data_delfor = data_delfor.iloc[:, [5, 10, 11]]

# # Rename the columns after reading
# data_delfor.columns = ['PrimeItem', 'Qty', 'Date']  # Replace with your desired column names
text_to_add = 'CIS-'
data_delfor['PrimeItem'] = text_to_add + data_delfor['PrimeItem'].astype(str)

# # Convert 'Column_C' from float to int
data_delfor['Qty'] = data_delfor['Qty'].fillna(-1).astype(int)
data_delfor['Date'] = data_delfor['Date'].fillna(-1).astype(int)

all_FC_list = data_delfor.values.tolist()
print("Length of FC delfor: ", len(all_FC_list))

# from openpyxl import load_workbook, Workbook
#
# # Load the existing workbook
# existing_workbook = load_workbook('Demand2.xlsx')  # Replace with the path to your existing file
#
# # Create a new workbook
# new_workbook = Workbook()
#
# # Get the active sheet from the new workbook (the default sheet)
# new_sheet = new_workbook.active
#
# # Add data to the new sheet in the new workbook
#
# for row in all_FC_list:
#     new_sheet.append(row)
#
# # Create a new sheet in the existing workbook and copy data from the new workbook
# new_sheet_name = 'NewSheet'  # Replace with your desired sheet name
# existing_workbook.create_sheet(title=new_sheet_name)
# existing_sheet = existing_workbook[new_sheet_name]
#
# for row in new_sheet.iter_rows(values_only=True):
#     existing_sheet.append(row)
#
# # Save changes to the existing workbook
# existing_workbook.save('Demand2.xlsx')  # Replace with the path to your existing file




print("@@@@@@@@\n FC delfor")
print(data_delfor)
print("@@@@@@@@")


#print((all_FC_list[0])[2])


#print(date_without_time)
#print(type(date_without_time))
#date222 = 2022-01-01

for r in all_FC_list:
    date_number = r[2]  # Replace this with your integer representing the date
    # Convert the integer to a string and then to datetime64[ns]
    date_string = str(date_number)
    date_without_time = datetime.strptime(date_string, '%Y%m%d').date()
    dd = pd.Timestamp(date_without_time)
    r[2] = dd                                   # convert int to data


#print(type((all_FC_list[0])[2]))

# # Swap data between 'Qty' and 'Date' in the DataFrame
# temp = data_delfor['Qty'].copy()  # Create a copy of 'Qty'
# data_delfor['Qty'] = data_delfor['Date']  # Assign 'Date' to 'Qty'
# data_delfor['Date'] = temp  # Assign the copy of 'Qty' to 'Date'
#
# # Rename specific columns in the DataFrame
# new_column_names = {'Qty': 'Date', 'Date': 'Qty'}
# data_delfor = data_delfor.rename(columns=new_column_names)

# Display the DataFrame with the selected and renamed columns
# print(data_delfor)
# print(data_delfor.dtypes)


file_demand = 'Demand.xlsx'  # Replace with your file path

# Read the Excel file into a Pandas DataFrame
data_demand = pd.read_excel(file_demand)

#data_demand['Date'] = data_demand['Date'].fillna(-1).astype(int)
l1 = data_demand.values.tolist()  # list of demand file
sorted_list = sorted(l1, key=lambda x: x[1])  # sorted by data for getting n

print('*****************')
#print(sorted_list)
print('*****************')
n = (sorted_list[len(sorted_list)-1])[1].date() - (sorted_list[0])[1].date()
#print(n.days)
#print((n/7).days)
n = (n/7).days + 1
print(n)
#data_demand['Date'] = data_demand['Date'].astype(str)
#data_demand['Date'] = data_demand['Date'].str.replace('-', '')
#data_demand['Date'] = data_demand['Date'].astype(int)



all_rows_as_list = data_demand.values.tolist()
#print(type((all_rows_as_list[0])[1]))
#print(all_rows_as_list)



strrr = 'CIS-07-100190-01'
print((all_FC_list[0])[0])
print((all_rows_as_list[0])[0])

sorted_list_delfor = sorted(all_FC_list, key=lambda x: x[2])
sorted_list_demand = sorted(all_rows_as_list, key=lambda x: x[1])
print(sorted_list_delfor[0], sorted_list_demand[0])




print((all_FC_list[0])[2], (all_rows_as_list[0])[1])
print(len(all_FC_list), len(all_rows_as_list))

print((all_FC_list[0])[1] , (all_rows_as_list[0])[2])
spec_data = (sorted_list_demand[len(sorted_list_demand) - 1])[1]

temp_data = (sorted_list_delfor[len(sorted_list_delfor) - 1])[2]

arr1 = []   # list data FC before last date in demand including this date
for i in range(len(all_FC_list)):
    if((all_FC_list[i])[2] <= spec_data ):
        arr1.append(all_FC_list[i])

print(len(arr1))
# for el in all_FC_list:
#     if(el[2] > spec_data):
#         all_FC_list.remove(el)
print(len(all_FC_list), len(all_rows_as_list))




# nums1 = [1,2,3,4,5,6]
# nums2 = [1,3,4,6]
#
# for i in range(len(nums1)):
#     if(nums1[i] != nums2[i]):
#         nums2.insert(i, nums1[i])
# print(nums1)
# print(nums2)

# c = 0
#
# set = {""}
# l1FC = [[sublist[0], sublist[2]] for sublist in arr1]
# l2D = all_rows_as_list[0:2]
# m = len(set21)
# for i in range(len(l2D)):
#
#     if ((all_rows_as_list[i])[0] not in set):
#         print(c/n)
#         print((all_rows_as_list[i])[0])
#         c = 0
#     set.add((all_rows_as_list[i])[0])
#
#     for j in range(len(l1FC)):
#
#             if(l1FC[j] in l2D):
#                 print((arr1[j])[2], (all_rows_as_list[i])[1])
#                 print((arr1[j]), (all_rows_as_list[i]))
#                 print((arr1[j])[1] - (all_rows_as_list[i])[2])
#                 c += (arr1[j])[1] - (all_rows_as_list[i])[2]
#             else:
#                 c+=(arr1[j])[1]


# for i in range(len(all_rows_as_list)):
#
#     if ((all_rows_as_list[i])[0] not in set):
#         print(c/n)
#         print((all_rows_as_list[i])[0])
#         c = 0
#     set.add((all_rows_as_list[i])[0])
#
#     for j in range(len(arr1)):
#
#         if ( ext_list[i] in extra_list2):
#             if((all_rows_as_list[i])[0] == (arr1[j])[0] and (all_rows_as_list[i])[1] == (arr1[j])[2]):
#                 print((arr1[j])[2], (all_rows_as_list[i])[1])
#                 print((arr1[j]), (all_rows_as_list[i]))
#                 print((arr1[j])[1] - (all_rows_as_list[i])[2])
#                 c += (arr1[j])[1] - (all_rows_as_list[i])[2]
#
#         else:
#             c += (arr1[j])[1] - 0
#



# for i in range(len(sorted_list1_FC)):
#     if((sorted_list1_FC[i])[0] == (sorted_list2_D[i])[0] and (sorted_list1_FC[i])[2] != (sorted_list2_D[i])[1]):
#         sorted_list2_D.insert(i, [(sorted_list1_FC[i])[0], (sorted_list1_FC[i])[2], 0])
#
# print(len(sorted_list1_FC), len(sorted_list2_D))

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

for i in range(len(arr1)):
    if ((arr1[i])[0] not in setf):
        finalArray.append([(arr1[i])[0], count / n])
        count = 0

    setf.add((arr1[i])[0])

    if((arr1[i])[1] in arr2):
        if(len(arr1[i]) == 4):
            count+= (arr1[i])[2] - (arr1[i])[3]
        else:
            count+= (arr1[i])[2]



#print(count/n)
#print(finalArray)

for i in range(len(finalArray)-1):
    (finalArray[i])[1] = (finalArray[i+1])[1]
#print(finalArray)
(finalArray[len(finalArray)-1])[1] = count/n

print(finalArray)
print(len(finalArray))

temp2 = []  # THIS FINAL LIST

for i in range(len(finalArray)):
    if((finalArray[i])[0] in arrTe):
        temp2.append(finalArray[i])

print(temp2)
print(len(temp2))