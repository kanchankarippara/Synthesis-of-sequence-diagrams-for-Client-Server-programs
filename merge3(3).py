#!/usr/bin/env python
# coding: utf-8

# In[827]:


#Taking csv files(Execution traces) as input
import csv
import re
csv_arr = []
n = input('Enter no of csv files: ')
for i in range(int(n)):
    csv_arr.append(input('Enter the paths: '))
dataset1 = []
c = []
for i in csv_arr:
    path = i
    file = open(path, newline = '')
    reader = csv.reader(file)
    data = [row for row in reader]
    c.append(len(data))
    dataset1.append(data)


# In[828]:


#Counting the number of lines in the execution traces of both server and client
client_count = []
client_sync = []
server_count = len(dataset1[0])
for i in range(1, int(n)):
    client_count.append(len(dataset1[i]))
    client_sync.append(0)
print(server_count)
print(client_count)


# In[829]:


print(dataset1[2][16])


# In[830]:


#Identifying the connected clients through the port no
no_of_clients = int(n) - 1
port_list = [r'port\=\d{5}', r'localport=\d{5}']
server_port = []
client_port = []
socket_port = []
server = []
connected_clients = []
flg_count = 0
c = 0
p = re.compile(port_list[0])
q = re.compile(port_list[1])
for i in range(server_count):
    for j in dataset1[0][i]:
        if p.findall(j):
            server_port.append(dataset1[0][c][6])
            if flg_count == 0:
                server.append(dataset1[0][c][4])
                flg_count = 1
#             server_port.append(c+1)
            socket_port.append(c+1)
    c = c + 1

    
for i in range(no_of_clients):
    c1 = 0
    for j in range(client_count[i]):
        for k in dataset1[i+1][j]:
            if q.findall(k):
                connected_clients.append(dataset1[i+1][c1][4])
                client_port.append(dataset1[i+1][c1][7])
#                 client_port.append(dataset[i+1][c1][4])
#                 client_port.append(c1+1)
        c1 = c1 + 1
    
    
print(server_port)
server_port_distinct = []
[server_port_distinct.append(x) for x in server_port if x not in server_port_distinct]
print(server_port_distinct)
print(client_port)
# print(server_port[0][5:10])
# print(client_port[0][10:15])
# del client_port[1], client_port[2], client_port[3]
print(server)
print(socket_port)
print(connected_clients)


# In[831]:


server_text = []
flag = 0
for i in range(len(server[0])):
    if server[0][i] == '#':
        tem = i
    if server[0][i] == '.':
        tem1 = i
        flag = 1
if flag == 1:
    server_text.append(server[0][tem1:tem])
else:
    server_text.append(server[0][11:tem])
print(server_text)


# In[832]:


unique = []
client_start = []
client_end = []
c = 0
for x in server_port: 
    if x not in unique:
        unique.append(x)
        client_start.append(c)
        for i in range(c+1, len(server_port)):
            if(x == server_port[i]):
                client_end.append(i)
    c = c + 1
print(client_start)
print(client_end)


# In[833]:


client_startpoints = []
for i in range(len(client_start)):
    client_startpoints.append(socket_port[client_start[i]])
print(client_startpoints)
client_endpoints = []
for i in range(len(client_end)):
    client_endpoints.append(socket_port[client_end[i]])
print(client_endpoints)    


# In[834]:


#Checks whether a new client communicates to the server before an existing client finishes its communication 
#If no new client comes before an existing client then sync is set to true else sync is set to false 
sync = True
for i in range(0, len(server_port) - 1, 2):
    if(server_port[i] != server_port[i+1]):
        sync = False
        break
print(sync)


# In[835]:


merge_list = []
for i in range(len(server_port_distinct)):
    for j in range(len(client_port)):
        if server_port_distinct[i][5:10] == client_port[j][10:15]:
            merge_list.append(j + 1)
            break
print(merge_list)   


# In[836]:


#Identifies the order in which the clients communicate to the server and stores them in a list
connected_clients_sync = []
for i in range(len(merge_list)):
    connected_clients_sync.append(connected_clients[merge_list[i]- 1])
print(connected_clients_sync)


# In[837]:


client_text = []
print(connected_clients[0][1:10])
for i in range(len(connected_clients_sync)):
    flag = 0
    for j in range(len(connected_clients_sync[i])):
        if connected_clients_sync[i][j] == '#':
            tem = j
        if connected_clients_sync[i][j] == '.':
            tem1 = j
            flag = 1
    if flag == 1:
        client_text.append(connected_clients_sync[i][tem1+1:tem])
    else:
        client_text.append(connected_clients_sync[i][11:tem])
print(client_text)


# In[838]:


#The csv files are arranged in the hierarchical order of clients
csv_arr_ordered = []
csv_arr_ordered.append(csv_arr[0])
for i in merge_list:
    for j in range(len(csv_arr)):
        if i == j:
            csv_arr_ordered.append(csv_arr[j])
            break
print(csv_arr_ordered)


# In[839]:


dataset = []
client_count = []
for i in csv_arr_ordered:
    path = i
    file = open(path, newline = '')
    reader = csv.reader(file)
    data = [row for row in reader]
    client_count.append(len(data))
    dataset.append(data)


# In[840]:


print(dataset[1][0])
print(client_count)
del client_count[0]


# In[841]:


#Identifies the points at which the server communicates to the client and stores them in a list called count_list
re_list = [r'port\=\d{5}',
           '\s[a-zA-Z0-9]+\=java.net.SocketInputStream',
           '\s[a-zA-Z0-9]+\=java.net.SocketOutputStream',
#            '\s[a-zA-Z0-9]+\=java.util.Scanner',
           '\s[a-zA-Z0-9]+\=java.io.PrintStream',
           '\s[a-zA-Z0-9]+\=java.io.DataInputStream',
           '\s[a-zA-Z0-9]+\=java.io.DataOutputStream',
           '\s[a-zA-Z0-9]+\=java.io.BufferedReader']

net_socket = [r'\s[a-zA-Z0-9]+\=java.net.Socket']
q = re.compile(net_socket[0])



count_list = []
flg = 0
for k in range(len(re_list)):
    count = 1
    p = re.compile(re_list[k])
    for i in range(server_count):
        count1 = 0
        for j in dataset[0][i]:
               if p.findall(j):
                    count1 = count
                    print(j)
        count=count+1
        if count1 == 0:
            continue
        else:
            count_list.append(count1)


        
count_list.sort()
count_list.append(server_count - 1)
# count_list.insert(7, 110)
# count_list.insert(15, 203)
# del count_list[len(count_list) - 1]
print(count_list)


# In[842]:


def merge(client_startpoints, client_endpoints): 
    merged_list = [(client_startpoints[i], client_endpoints[i]) for i in range(0, len(client_startpoints))] 
    return merged_list
client_breakpoints = []
client_breakpoints = merge(client_startpoints, client_endpoints)
print(client_breakpoints)


# In[843]:


print(client_sync)
client_sync_count = 0
for i in range(len(client_breakpoints) - 1):
    if(client_breakpoints[i][1] > client_breakpoints[i+1][0]):
        client_sync[i] = 1
        client_sync_count = client_sync_count + 1
print(client_sync)
print(client_sync_count)
print(client_breakpoints)
print(client_breakpoints[0])


# In[844]:


server_socket_breakpoints = []
x = 0
y = 0
for i in range(len(client_breakpoints)):
    for j in client_breakpoints[i]:
        for k in range(len(count_list)):
            if j == count_list[k]:
                server_socket_breakpoints.append(k)
print(server_socket_breakpoints)
print(server_socket_breakpoints)
print(server_socket_breakpoints)


# In[845]:


def bubbleSort(arr, pos):
    n = len(arr)
    # Traverse through all array elements
    for i in range(pos, n):
        ctr = 0
        # Last i elements are already in place
        for j in range(pos, n-ctr-1):
 
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
            ctr = ctr + 1


# In[846]:


sample = [5, 3, 10, 15, 9, 1, 4]
bubbleSort(sample, 2)
print (sample) 


# In[847]:


#Identifies the points at which the clients communicate to the server and stores them in a list called count_list1
re_list = [r'localport=\d{5}',
           '\s[a-zA-Z0-9]+\=java.net.SocketInputStream',
           '\s[a-zA-Z0-9]+\=java.net.SocketOutputStream',
#            '\s[a-zA-Z0-9]+\=java.util.Scanner',
           '\s[a-zA-Z0-9]+\=java.io.PrintStream',
           '\s[a-zA-Z0-9]+\=java.io.DataInputStream',
           '\s[a-zA-Z0-9]+\=java.io.DataOutputStream',
           '\s[a-zA-Z0-9]+\=java.io.BufferedReader']



#Splits the execution trace of server according to the points stored in count_list 
def server_split(c1, c2):
    temp = []
    temp1 = []
    for i in range(c1 , c2 + 1):
        for j in dataset[0][i]:
            if i == c1:
                temp.append(j)
            elif j=="main" or j=="SYSTEM" or j=="pool-1-thread-1" or j=="pool-1-thread-2" or j == "Thread-0" or j == "Thread-1" or j == "Thread-2":
                temp1.append(temp)
                temp=[]
                temp.append(j)
            else:
                temp.append(j)
    return temp1


c_list = []
client_length = []
pos = 0

for z in range(1, int(n)):
    pos1 = pos
    for k in range(len(re_list)):
        p = re.compile(re_list[k])
        count = 1
        for i in range(len(dataset[z])):
            count1 = 0
            for j in dataset[z][i]:
                if p.findall(j):
                    count1 = count
                    print(j)
            count=count+1
            if count1 == 0:
                continue
            else:
                if j == ' client=java.net.Socket (id=29)"':
                    c_list.append(count1)
                    break
                c_list.append(count1)
                pos = pos + 1
    c_list.append(client_count[z - 1] - 1)
    pos = pos + 1
    client_length.append(pos)
    if z == 1:
        c_list.sort()
    else:
        bubbleSort(c_list, pos1 + 1)
        
        

    
print(c_list)
print(client_length)
# for i in client_length:
#     j = i - 1
#     print(j)
#     tem_var = count_list[j] - 2
#     print(tem_var)
#     count_list.insert(j, tem_var-2)
#     break
# print(count_list)

# for k in range(len(re_list)):
#     p = re.compile(re_list[k])
#     for z in range(2, int(n)):
#         count = 1
#         for i in range(len(dataset[z])):
#             count1 = 0
#             for j in dataset[z][i]:
#                 if p.findall(j):
#                     count1 = count
#                     print(j)
#             count=count+1
#             if count1 == 0:
#                 continue
#             else:
#                 if j == ' client=java.net.Socket (id=29)"':
#                     c_list1.append(count1)
#                     break
#                 c_list1.append(count1)
#     c_list1.sort()


# for i in range(len(client_count)):
#     c_list.append(client_count[i] - 1)

# c_list.append(client_count[0] - 1)
# c_list.append(client_count[1] - 1)
# print(c_list)
# print(c_list1)

count_list1 = []

# count_list1.extend(c_list)
# count_list1.extend(c_list1)
# x = 0
# client_length_list = []
# client_length = 0
# for i in range(len(client_count)):
#     for m in c_list:
#         if x % no_of_clients == i:
#             count_list1.append(m)
#             if x % no_of_clients == 0:
#                 client_length = client_length + 1
#         x = x + 1
#     client_length_list.append(client_length)

# print(client_length_list)
count_list1.extend(c_list)
print(count_list1)

#Splits the execution traces of the clients according to the points stored in count_list1
def client_split(c1, c2, z):
    temp = []
    temp1 = []
    for i in range(c1 , c2 + 1):
        for j in dataset[z][i]:
            if i == c1:
                temp.append(j)
            elif j=="main" or j=="SYSTEM":
                temp1.append(temp)
                temp=[]
                temp.append(j)
            else:
                temp.append(j)
    return temp1 
 
a = []
a.append(server_split(0, count_list[0]))
import numpy as np
np.shape(server_split(count_list[0],count_list[1]))


# In[848]:


temp = []
stream = []
for i in range(len(server_socket_breakpoints) - 1):
    if i % 2 == 1:
        if server_socket_breakpoints[i] > server_socket_breakpoints[i+1]:
            temp.append(server_socket_breakpoints[i+1])
# temp.reverse()
print(temp)
count = 0
print(len(count_list))
for i in range(len(count_list)):
    if len(temp) == 0:
        break
    if i == temp[count]:
        stream.append(i-3)
        stream.append(i-2)
        stream.append(i-1)
        count = count + 1
        
        if(count == len(temp)):
            break
        
print(stream)
list_order = [3, 4, 5, 0, 1, 2]

# del stream[0]
# del stream[0]
# del stream[0]
print(stream)


# In[849]:


stream[3:6], stream[0:3] = stream[0:3], stream[3:6]
print(stream)


# In[850]:


#Client length stores the points at which a new client communicates to the server 
print(client_length)
client_length1 = []
append_count = 0

k = 2
if sync == False:
    for i in range(len(client_length)):
        if client_sync[i] == 1:
            append_count = append_count + 1
            client_length1.append(client_length[i] - k)
            k = k + 2
        else:
            client_length1.append(client_length[i] - append_count*2)
    for i in range(append_count):
        client_length1.append(2)
print(client_length)
print(client_length1)


# In[851]:


count_two = 0
for i in client_length1:
    if i == 2:
        count_two = count_two + 1
print(count_two)


# In[852]:


server_socket_breakpoints.sort()


# In[853]:


#Merges the execution traces of server and clients in the case where no new client communicates to the server during an
#existing client server communication
if sync == True:
    merge = []
    merge_flag = 0
    client_counter = 1
    for i in range(len(count_list1)):
        if i == 0:
            merge.append([[server_text[0], 1,' ','Method Call']])
            merge.append(server_split(0, count_list[0]))
            merge.append([[server_text[0], count_list[0] + 2,' ','Method Exit']])
            merge.append([[client_text[0], count_list[0] + 3,' ','Method Call']])
            merge.append(client_split(0, count_list1[0], client_counter))
            merge.append([[client_text[0], count_list1[0] + 4,' ','Method Exit']])
        elif (i+1) % client_length[client_counter - 1] == 0:
            merge.append([[client_text[client_counter - 1], 1,' ','Method Call']])
            merge.append(client_split(count_list1[i-1], count_list1[i], client_counter))
            merge.append([[client_text[client_counter - 1], 1,' ','Method Exit']])
            merge.append([[server_text[0], 1,' ','Method Call']])
            merge.append(server_split(count_list[i-1], count_list[i]))
            if client_counter == len(client_length):
                merge.append(server_split(count_list[len(count_list)- 2], count_list[len(count_list) - 1]))
            merge.append([[server_text[0], 1,' ','Method Exit']])
            merge_flag = 1
            client_counter = client_counter + 1
#             flag = 1
        elif i == len(count_list1) - 1:
            merge.append([[client_text[client_counter - 1], 1,' ','Method Call']])
            merge.append(client_split(count_list1[i-1], count_list1[i], client_counter))
            merge.append([[client_text[client_counter - 1], 1,' ','Method Exit']])
            merge.append([[server_text[0], 1,' ','Method Call']])
            merge.append(server_split(count_list[i-1], count_list[i]))
            merge.append([[server_text[0], 1,' ','Method Exit']])
            break
        elif merge_flag == 1:
            merge.append([[server_text[0], 1,' ','Method Call']])
            merge.append(server_split(count_list[i-1], count_list[i]))
            merge.append([[server_text[0], count_list[0] + 2,' ','Method Exit']])
            merge.append([[client_text[client_counter - 1], count_list[0] + 3,' ','Method Call']])
            merge.append(client_split(0 , count_list1[i], client_counter))
            merge.append([[client_text[client_counter - 1], count_list1[0] + 4,' ','Method Exit']])
            merge_flag = 0
        else:
            merge.append([[server_text[0], 1,' ','Method Call']])
            merge.append(server_split(count_list[i-1], count_list[i]))
            merge.append([[server_text[0], count_list[0] + 2,' ','Method Exit']])
            merge.append([[client_text[client_counter - 1], count_list[0] + 3,' ','Method Call']])
            merge.append(client_split(count_list1[i-1], count_list1[i], client_counter))
            merge.append([[client_text[client_counter - 1], count_list1[0] + 4,' ','Method Exit']])
            
        
# print(client_count)
# merge[(len(count_list) + len(count_list1)) + 6] = merge[(len(count_list) + len(count_list1))] + [['SYSTEM', server_count, ' "SYSTEM"', ' "System End"', ' " "']]
# merge[(len(count_list) + len(count_list1))] = merge[(len(count_list) + len(count_list1))] + [['SYSTEM', client_count, ' "SYSTEM"', ' "System End"', ' " "']]
# for i in range(server_count + client_count - 3):
#     merge[0]
# print(np.shape(merge))
# print(merge[52])
# print(len(merge))


# In[854]:


#Merges the execution traces of server and clients in the case where a new client communicates to the server during an
#existing client server communication
if sync == False:
    merge = []
    merge_flag = 0
    client_counter = 1
    server_iter = 0
    client_iter = 0
    i = 0
    k = 1
    client_end_flag = 0
    stream_iter = 0
    count_dis = 0
    client_sync_count = 2
    server_index = no_of_clients
    while(1):
        if i == 0:
            merge.append([[server_text[0], 1,' ','Method Call']])
            merge.append(server_split(0, count_list[0]))
            merge.append([[server_text[0], count_list[0] + 2,' ','Method Exit']])
            merge.append([[client_text[client_counter - 1], count_list[0] + 3,' ','Method Call']])
            merge.append(client_split(0, count_list1[0], client_counter))
            merge.append([[client_text[client_counter - 1], count_list1[0] + 4,' ','Method Exit']])
            print(f'{i} 0')
            i = i + 1
            server_iter = server_iter + 1
            client_iter = client_iter + 1
        elif ((i+1) % client_length1[client_counter - 1] == 0) or ((client_iter + 1) % client_length[client_counter-1]  == 0):
            if client_sync[client_counter - 1] == 1:
                server_iter = client_length[client_counter - 1] - k
                k = k + 1
                print(f'{server_iter} server')
                client_iter = client_length[client_counter - 1]
                print(f'{client_iter} client')
                client_counter = client_counter + 1
                print(f'{i}+')
                i = i + 1
                merge_flag = 1
                continue
            if client_sync[client_counter - 1] == 0:
                merge.append([[client_text[client_counter - 1], 1,' ','Method Call']])
                merge.append(client_split(count_list1[client_iter-1], count_list1[client_iter], client_counter))
                merge.append([[client_text[client_counter - 1], 1,' ','Method Exit']])
                merge.append([[server_text[0], 1,' ','Method Call']])
                merge.append(server_split(count_list[server_iter-1], count_list[server_iter]))
                merge.append([[server_text[0], 1,' ','Method Exit']])
                if(client_length1[client_counter] == 2):
                    print(f'{client_counter} client counter')
                    client_counter = client_counter - 1
                    client_end_flag = 1
                    count_dis = count_dis + 1
        elif client_end_flag == 1:
            server_iter = stream[stream_iter] + 1
            client_iter = stream[stream_iter] + 1
            stream_iter = stream_iter + 3
            client_counter = client_sync_count

            for j in range(0, 2):
                merge.append([[server_text[0], 1,' ','Method Call']])
                merge.append(server_split(count_list[server_iter - 1], count_list[server_iter]))
                merge.append([[server_text[0], count_list[0] + 2,' ','Method Exit']])
                merge.append([[client_text[client_counter - 1], count_list[0] + 3,' ','Method Call']])
                merge.append(client_split(count_list1[client_iter - 1], count_list1[client_iter], client_counter))
                merge.append([[client_text[client_counter - 1], count_list1[0] + 10,' ','Method Exit']])
                server_iter = server_iter + 1
                client_iter = client_iter + 1
                print("IN")
            client_sync_count = client_sync_count - 1
            merge.append([[client_text[client_counter - 1], 1,' ','Method Call']])
            print(f'{client_iter}--')
            client_iter = client_iter + client_sync_count
            merge.append(client_split(count_list1[client_iter - 1], count_list1[client_iter], client_counter))
            print("OUT")
            merge.append([[client_text[client_counter - 1], 1,' ','Method Exit']])
            merge.append([[server_text[0], 1,' ','Method Call']])
            merge.append(server_split(count_list[server_socket_breakpoints[len(server_socket_breakpoints) - server_index]], count_list[server_socket_breakpoints[len(server_socket_breakpoints) - (server_index-1)]]))
            server_index = server_index - 1
            if client_sync_count == 0:
                merge.append(server_split(count_list[len(count_list) - 2], count_list[len(count_list) - 1]))
            if client_sync_count == 0:
                break
        elif merge_flag == 1:
            merge.append([[server_text[0], 1,' ','Method Call']])
            merge.append(server_split(count_list[server_iter-1], count_list[server_iter]))
            merge.append([[server_text[0], count_list[0] + 2,' ','Method Exit']])
            merge.append([[client_text[client_counter - 1], count_list[0] + 3,' ','Method Call']])
            merge.append(client_split(0 , count_list1[client_iter], client_counter))
            merge.append([[client_text[client_counter - 1], count_list1[0] + 4,' ','Method Exit']])
            merge_flag = 0
            server_iter = server_iter + 1
            client_iter = client_iter + 1
            i = i + 1
        else:
            merge.append([[server_text[0], 1,' ','Method Call']])
            merge.append(server_split(count_list[server_iter-1], count_list[server_iter]))
            merge.append([[server_text[0], count_list[0] + 2,' ','Method Exit']])
            merge.append([[client_text[client_counter - 1], count_list[0] + 3,' ','Method Call']])
            merge.append(client_split(count_list1[client_iter-1], count_list1[client_iter], client_counter))
            merge.append([[client_text[client_counter - 1], count_list1[0] + 10,' ','Method Exit']])
            server_iter = server_iter + 1
            client_iter = client_iter + 1
            i = i + 1
        
# print(client_count)
# merge[(len(count_list) + len(count_list1)) + 6] = merge[(len(count_list) + len(count_list1))] + [['SYSTEM', server_count, ' "SYSTEM"', ' "System End"', ' " "']]
# merge[(len(count_list) + len(count_list1))] = merge[(len(count_list) + len(count_list1))] + [['SYSTEM', client_count, ' "SYSTEM"', ' "System End"', ' " "']]
# for i in range(server_count + client_count - 3):
#     merge[0]
# print(np.shape(merge))
# print(merge[52])
# print(len(merge))


# In[855]:


# print(merge)
print(len(merge))


# In[856]:


with open("test.csv", "w", newline="") as f:
    writer = csv.writer(f)
    for i in range(len(merge)):
        writer.writerows(merge[i])


# In[857]:


num = 2
k = 1
temp = 0
client_end_counter = 0
client_start_counter = 0
while temp < client_length[len(client_length) - 1]:
#     if k == len(merge) - 1:
#         break
    if (temp + 1)%client_length[client_end_counter] == 0:
        print(f'{k} value of k')
        for n in range(count_list1[temp] - count_list1[temp - 1]):
            merge[k][n][1] = num
            num = num + 1
        k += 1
        print(k)
#         if k == len(merge) - 1:
#             break
        for o in range(2):
            z = 0
            merge[k][z][1] = num
            num = num + 1
            z += 1
            k += 1
        print(k)
#         if k == len(merge) - 1:
#             break
        for j in range(count_list[temp] - count_list[temp - 1]):
            merge[k][j][1] = num
            num = num + 1
        k += 1
        print(k)
#         if k == len(merge) - 1:
#             break

        if (client_start_counter+1) == len(client_length):
            print(f'{k} +++')
            for i in range(len(merge[k])):
                merge[k][i][1] = num
                num = num + 1
        m = 0    
        for m in range(2):
            merge[k][0][1] = num
            num = num + 1
            k += 1

        print(k)
#         if k == len(merge) - 1:
#             break
        temp += 1
        client_end_counter +=1
#         if k == len(merge) - 1:
#             break
        print(f'{temp}+')

        continue
        
        
    #Server
    if temp == 0:
        for j in range(count_list[temp]):
            merge[k][j][1] = num
            num = num + 1
        k += 1
        print(k)
    else:
        for j in range(count_list[temp] - count_list[temp - 1]):
            merge[k][j][1] = num
            num = num + 1
        k += 1
        print(k)
#     if k == len(merge) - 1:
#         break
    #server exit client call    
    m = 0    
    for m in range(2):
        merge[k][0][1] = num
        num = num + 1
        k += 1

    print(k)
    
    #Client
        
#     print(temp)
    if temp == 0 or temp%client_length[client_start_counter] == 0:
        print(f'{k}cli')
        print(f'{client_start_counter}cli_Counter')
        for n in range(count_list1[temp]):
            merge[k][n][1] = num
            num = num + 1
        k += 1
        if temp != 0:
            client_start_counter +=1
        print(k)
#     elif temp == len(count_list)-2:
#         for n in range(count_list1[temp + 1] - count_list1[temp]):
#             merge[k][n][1] = num
#             num = num + 1
#         k += 1
#         print(k)
    else:
        for n in range(count_list1[temp] - count_list1[temp - 1]):
            merge[k][n][1] = num
            num = num + 1
        k += 1
        print(k)
    if k == len(merge) - 1:
        break
    #client exit server call   
    for o in range(2):
        z = 0
        merge[k][z][1] = num
        num = num + 1
        z += 1
        k += 1
    print(k)
    temp += 1
    print(f'{temp}+')
    


# In[858]:


print(client_length)
print(len(merge))
# print(client_length[len(client_length) - 1])


# In[859]:


merge[len(merge) - 1][0][1] = num


# In[860]:


with open("merged-csv.csv", "w", newline="") as f:
    writer = csv.writer(f)
    for i in range(len(merge)):
        writer.writerows(merge[i])


# In[861]:


print(merge[64])


# In[862]:


# socket = []
# sam = []
# for j in range(count_list1[temp]):
#     if merge[4][j][3] == ' "Method Call"':
#         sam = merge[4][j][5]
#         flg = 0
#         for c in range(len(sam)):
#             if sam[c] == '#':
#                 tem = c
#             if sam[c] == '.':
#                 flg = 1
#                 tem1 = c
#         if flg == 0:
#             sam = sam[8:tem]
#         else:
#             sam = sam[tem1+1:tem]
#         socket.append(sam)
#         break
# print(socket)


# In[863]:


temp = 2
print(merge[1][4])


# In[864]:


#Code for generating uml diagram
temp = 0
k = 1
x = 0
uml = ["@startuml"]
start = []
end = []
socket = []
client_counter = 0
while 1:
    if k == len(merge) - 1:
        break
    
    if (temp+1)%client_length[client_counter] == 0:
        print(f'{k}-----')
        print(f'{client_counter} +-')
        print(f'{temp} value of temp')

        for j in range(count_list1[temp] - count_list1[temp-1]):
            if merge[k][j][3] == ' "Method Call"':
                s = merge[k][j][4]
                flg = 0
                for c in range(len(s)):
                    if s[c] == '#':
                        tem = c
                    if s[c] == '.':
                        tem1 = c
                        flg = 1
                if flg == 0:
                    s = s[10:tem+1]
                else:
                    s = s[tem1+1:tem]
                s = s.replace(":",".")
                uml.append(s)
                start.append(s)
                uml.append("->")
                s1 = merge[k][j][5]
                flg1 = 0
                for c in range(len(s1)):
                    if s1[c] == '#':
                        tem = c
                    if s1[c] == '.':
                        tem1 = c
                        flg1 = 1
                if flg1 == 0:
                    s1 = s1[8:tem]
                else:
                    s1 = s1[tem1+1:tem]
                s1 = s1.replace(":",".")
                uml.append(s1)
                uml.append("newline")
            if merge[k][j][3] == ' "Method Exit"':
                s2 = merge[k][j][4]
                flg2 = 0
                for c in range(len(s2)):
                    if s2[c] == '#':
                        tem = c
                    if s2[c] == '.':
                        tem1 = c
                        flg2 = 1
                if flg2 == 0:
                    s2 = s2[12:tem]
                else:
                    s2 = s2[tem1+1:tem]
                s2 = s2.replace(":",".")
                end.append(s2)
                uml.append(end[len(end) - 1])
                uml.append("-->")
                uml.append(start[len(start) - 1])
                start.remove(start[len(start) - 1])
                uml.append("newline")
        client_counter = client_counter + 1
        k+=3
        print(f'{k}----')
        for j in range(count_list[temp] - count_list[temp - 1]):
            if merge[k][j][3] == ' "Method Call"':
                s = merge[k][j][4]
                if s == ' " caller=Ljava/util/concurrent/ThreadPoolExecutor$Worker;.run()' or s == ' " caller=Ljava/util/concurrent/ThreadPoolExecutor;.runWorker(Ljava/util/concurrent/ThreadPoolExecutor$Worker;)':
                    continue
                s1 = merge[k][j][5]
                if s1 == ' target=Ljava/util/concurrent/ThreadPoolExecutor$Worker;.run()"':
                    continue
                print(s)
                s = s.replace(":",".")
                for c in range(len(s)):
                    if s[c] == '#':
                        tem = c
                s = s[10:tem]
                uml.append(s)
                start.append(s)
                uml.append("->")
                s1 = s1.replace(":",".")
                for c in range(len(s1)):
                    if s1[c] == '#':
                        tem = c
                s1 = s1[8:tem]
                uml.append(s1)
                uml.append("newline")
            if merge[k][j][3] == ' "Method Exit"':
                s2 = merge[k][j][4]
                for c in range(len(s2)):
                    if s2[c] == '#':
                        tem = c
                s2 = s2[12:tem]
                s2 = s2.replace(":",".")
                end.append(s2)
                uml.append(end[len(end) - 1])
                uml.append("-->")
                uml.append(start[len(start) - 1])
                start.remove(start[len(start) - 1])
                uml.append("newline")
        k += 1
        
        if client_counter == len(client_length):
            print(f'{k} +++')
            for i in range(len(merge[k])):
                merge[k][i][1] = num
                num = num + 1
            break
        
        for i in range(2):
            k+=1
        temp+=1
        print(f'{temp}+')
        continue
    
    #Server
    if temp == 0:
        uml.extend(socket)
        for j in range(count_list[temp]):
            if merge[k][j][3] == ' "Method Call"':
                s = merge[k][j][4]
                if s == ' " caller=Ljava/util/concurrent/ThreadPoolExecutor$Worker;.run()' or s == ' " caller=Ljava/util/concurrent/ThreadPoolExecutor;.runWorker(Ljava/util/concurrent/ThreadPoolExecutor$Worker;)':
                    continue
                s1 = merge[k][j][5]
                if s1 == ' target=Ljava/util/concurrent/ThreadPoolExecutor$Worker;.run()"':
                    continue
                s = s.replace(":",".")
                for c in range(len(s)):
                    if s[c] == '#':
                        tem = c
                s = s[10:tem]
                uml.append(s)
                start.append(s)
                uml.append("->")
                s1 = s1.replace(":",".")
                for c in range(len(s1)):
                    if s1[c] == '#':
                        tem = c
                s1 = s1[8:tem]
                uml.append(s1)
                uml.append("newline")
            if merge[k][j][3] == ' "Method Exit"':
                s2 = merge[k][j][4]
                for c in range(len(s2)):
                    if s2[c] == '#':
                        tem = c
                s2 = s2[12:tem]
                s2 = s2.replace(":",".")
                end.append(s2)
                uml.append(end[len(end) - 1])
                uml.append("-->")
                uml.append(start[len(start) - 1])
                start.remove(start[len(start) - 1])
                uml.append("newline")
                        
        k += 1
    else:
        uml.extend(socket)
        for j in range(count_list[temp] - count_list[temp - 1]):
            if merge[k][j][3] == ' "Method Call"':
                s = merge[k][j][4]
                if s == ' " caller=Ljava/util/concurrent/ThreadPoolExecutor$Worker;.run()' or s == ' " caller=Ljava/util/concurrent/ThreadPoolExecutor;.runWorker(Ljava/util/concurrent/ThreadPoolExecutor$Worker;)':
                    continue
                s1 = merge[k][j][5]
                if s1 == ' target=Ljava/util/concurrent/ThreadPoolExecutor$Worker;.run()"':
                    continue
                print(s)
                s = s.replace(":",".")
                for c in range(len(s)):
                    if s[c] == '#':
                        tem = c
                s = s[10:tem]
                uml.append(s)
                start.append(s)
                uml.append("->")
                s1 = s1.replace(":",".")
                for c in range(len(s1)):
                    if s1[c] == '#':
                        tem = c
                s1 = s1[8:tem]
                uml.append(s1)
                uml.append("newline")
            if merge[k][j][3] == ' "Method Exit"':
                s2 = merge[k][j][4]
                for c in range(len(s2)):
                    if s2[c] == '#':
                        tem = c
                s2 = s2[12:tem]
                s2 = s2.replace(":",".")
                end.append(s2)
                uml.append(end[len(end) - 1])
                uml.append("-->")
                uml.append(start[len(start) - 1])
                start.remove(start[len(start) - 1])
                uml.append("newline")
        k += 1
    if k == len(merge) - 1:
        break
    socket = []
    #server exit client call     
    for m in range(2):
        if temp != 0 and temp%client_length[client_counter - 1] != 0:
            socket.append(merge[k][0][0])
            if m == 0:
                socket.append("-->")
            else:
                socket.append(":sends response")
                socket.append("newline")
        k += 1
#     print('start')
#     print(start)
#     print()
#     print('end')
#     print(end)
#     print()
#     print('uml')
#     print(uml)
    
#     socket.append(uml[len(uml) - 2])
#     uml.append(socket[x])
#     uml.append("->")
#     uml.append(socket[x+1])
#     uml.append(":")
#     if x % 2 == 0:
#         uml.append("sends request")
#     elif x % 2 == 1:
#         uml.append("sends response")
#     uml.append("newline")
#     x +=1
#     print('Socket')
#     print()
#     print(socket)
    
    #Client
    if temp == 0 or temp%client_length[client_counter - 1] == 0:
        uml.extend(socket)
        for j in range(count_list1[temp]):
            if merge[k][j][3] == ' "Method Call"':
                s = merge[k][j][4]
                flg = 0
                for c in range(len(s)):
                    if s[c] == '#':
                        tem = c
                    if s[c] == '.':
                        tem1 = c
                        flg = 1
                if flg == 0:
                    s = s[10:tem+1]
                else:
                    s = s[tem1+1:tem]
                s = s.replace(":",".")
                uml.append(s)
                start.append(s)
                uml.append("->")
                s1 = merge[k][j][5]
                flg1 = 0
                for c in range(len(s1)):
                    if s1[c] == '#':
                        tem = c
                    if s1[c] == '.':
                        tem1 = c
                        flg1 = 1
                if flg1 == 0:
                    s1 = s1[8:tem]
                else:
                    s1 = s1[tem1+1:tem]
                s1 = s1.replace(":",".")
                uml.append(s1)
                uml.append("newline")
            if merge[k][j][3] == ' "Method Exit"':
                s2 = merge[k][j][4]
                flg2 = 0
                for c in range(len(s2)):
                    if s2[c] == '#':
                        tem = c
                    if s2[c] == '.':
                        tem1 = c
                        flg2 = 1
                if flg2 == 0:
                    s2 = s2[12:tem]
                else:
                    s2 = s2[tem1+1:tem]
                s2 = s2.replace(":",".")
                end.append(s2)
                uml.append(end[len(end) - 1])
                uml.append("-->")
                uml.append(start[len(start) - 1])
                start.remove(start[len(start) - 1])
                uml.append("newline")
                client_counter = client_counter + 1
            
        k += 1
    elif temp == len(count_list)-2:
        uml.extend(socket)
        for j in range(count_list1[temp + 1] - count_list1[temp]):
            if merge[k][j][3] == ' "Method Call"':
                s = merge[k][j][4]
                flg = 0
                for c in range(len(s)):
                    if s[c] == '#':
                        tem = c
                    if s[c] == '.':
                        tem1 = c
                        flg = 1
                if flg == 0:
                    s = s[10:tem]
                else:
                    s = s[tem1+1:tem]
                s = s.replace(":",".")
                uml.append(s)
                start.append(s)
                uml.append("->")
                s1 = merge[k][j][5]
                s1 = s1.replace(":",".")
                flg1 = 0
                for c in range(len(s1)):
                    if s1[c] == '#':
                        tem = c
                    if s1[c] == '.':
                        tem1 = c
                        flg1 = 1
                if flg1 == 0:
                    s1 = s1[8:tem]
                else:
                    s1 = s1[tem1+1:tem]
                uml.append(s1)
                uml.append("newline")
            if merge[k][j][3] == ' "Method Exit"':
                s2 = merge[k][j][4]
                flg2 = 0
                for c in range(len(s2)):
                    if s2[c] == '#':
                        tem = c
                    if s2[c] == '.':
                        tem1 = c
                        flg2 = 1
                if flg2 == 0:
                    s2 = s2[12:tem]
                else:
                    s2 = s2[tem1+1:tem]
                s2 = s2.replace(":",".")
                end.append(s2)
                uml.append(end[len(end) - 1])
                uml.append("-->")
                uml.append(start[len(start) - 1])
                start.remove(start[len(start) - 1])
                uml.append("newline")
        k += 1
    else:
        uml.extend(socket)
        for j in range(count_list1[temp] - count_list1[temp - 1]):
            if merge[k][j][3] == ' "Method Call"':
                s = merge[k][j][4]
                flg = 0
                for c in range(len(s)):
                    if s[c] == '#':
                        tem = c
                    if s[c] == '.':
                        tem1 = c
                        flg = 1
                if flg == 0:
                    s = s[10:tem]
                else:
                    s = s[tem1+1:tem]
                s = s.replace(":",".")
                uml.append(s)
                start.append(s)
                uml.append("->")
                s1 = merge[k][j][5]
                flg1 = 0
                for c in range(len(s1)):
                    if s1[c] == '#':
                        tem = c
                    if s1[c] == '.':
                        tem1 = c
                        flg1 = 1
                if flg1 == 0:
                    s1 = s1[8:tem]
                else:
                    s1 = s1[tem1+1:tem]
                s1 = s1.replace(":",".")
                uml.append(s1)
                uml.append("newline")
            if merge[k][j][3] == ' "Method Exit"':
                s2 = merge[k][j][4]
                flg2 = 0
                for c in range(len(s2)):
                    if s2[c] == '#':
                        tem = c
                    if s2[c] == '.':
                        tem1 = c
                        flg2 = 1
                if flg2 == 0:
                    s2 = s2[12:tem]
                else:
                    s2 = s2[tem1+1:tem]
                s2 = s2.replace(":",".")
                end.append(s2)
                uml.append(end[len(end) - 1])
                uml.append("-->")
                uml.append(start[len(start) - 1])
                start.remove(start[len(start) - 1])
                uml.append("newline")
        k += 1
    if k == len(merge) - 1:
        break
    #client exit server call 
    socket = []
    for o in range(2):
        if (temp+2) % client_length[client_counter] != 0:
            socket.append(merge[k][0][0])
            if o == 0:
                socket.append("->")
            else:
                socket.append(":sends request")
                socket.append("newline")
        k += 1

    print('start1')
    print(start)
    print()
    print('end1')
    print(end)
    print()
    print('uml1')
    print(uml)

    temp += 1
    print(f'{temp}+')


# In[865]:


for i in range(len(socket)):
    print(socket[i])


# In[866]:


print(uml)
uml1 = []
def swapPositions(list, pos1, pos2): 
      
    list[pos1], list[pos2] = list[pos2], list[pos1] 
    return list
  
# # Driver function  
# pos1, pos2  = len(uml)-1, len(uml)-5
  
# uml1 = swapPositions(uml, pos1-1, pos2-1) 
# print()
# print(uml1)


# In[867]:


# uml = ["@startuml","Alice","->","Bob",":","Hey","Bob","-->","Alice",":","Hi","@enduml"]
uml.append("@enduml")
uml1.append("@enduml")
print(start)
print()
print(end)


# In[868]:


with open('file.txt', 'w') as file:
    for u in uml:
        if u != "newline":
            file.write(u)
        if u == "@startuml" or u == "@enduml" or u == "newline":
            file.write("\n")


# In[425]:


with open('file1.txt', 'w') as file:
    for u in uml1:
        if u != "newline":
            file.write(u)
        if u == "@startuml" or u == "newline":
            file.write("\n")


# In[869]:


for z in range(1, 3):
    print(z)


# In[ ]:




