import matplotlib.pyplot as plt

with open('IntervalData.csv', 'r') as file:

    usage_date,start_time, end_time, usage,daily_usage = [],[],[],[],[]
    next(file)  # skip the first line
    for line in file:
        data = line.strip().split(',')
        #print(data)
        usage_date.append(data[1])
        start_time.append(data[3])
        end_time.append(data[4])
        usage.append((data[5]))

    i=0
    #for i in range(20):# 
    while i<len(usage)-95:#2975:
        k = 0
        sum = 0
        while k < 95:#2975:
            if usage[i+k] =='':
                #print(i+k)
                usage[i+k] = 0.12 
            sum += float(usage[i+k])
            k +=1
        daily_usage.append(sum)
        i = i+k 
        
#print(daily_usage)   

# plot x and y data
plt.plot(range(len(daily_usage)), daily_usage )

# add x and y axis labels
plt.xlabel('Month')
plt.ylabel('Usage (kWh)')

# add a title
plt.title('Daily Usage of Electricity')

# display the plot
plt.show()
