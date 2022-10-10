import numpy as np
import matplotlib.pyplot as plt
 
# set width of bar
barWidth = 0.2
fig = plt.subplots(figsize =(12, 8))
 
# set height of bar
small_subtasks = [26.1, 46.5, 25.9, 29.1, 96.3]
big_subtasks = [19.3, 58.3, 29.3, 37.6, 119.5]
DiRL = [17.3, 43.6, 24.2, 24.8, 0]
SPECTRL = [23.3, 0, 36.9, 0, 0]
# Set position of bar on X axis
br1 = np.arange(len(small_subtasks))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]
 
# Make the plot
bar1 = plt.bar(br1, small_subtasks, color ='firebrick', width = barWidth-0.02,
         label ='OM + small subtasks')
plt.bar_label(bar1, fontsize = 12)
bar2 = plt.bar(br2, big_subtasks, color ='darkgreen', width = barWidth-0.02,
        label ='OM + big subtasks')
plt.bar_label(bar2, fontsize = 12)
bar3 = plt.bar(br3, DiRL, color ='midnightblue', width = barWidth-0.02,
        label ='DiRL')
plt.bar_label(bar3, fontsize = 12)
bar4 = plt.bar(br4, SPECTRL, color ='darkorange', width = barWidth-0.02,
        label ='SPECTRL')
plt.bar_label(bar4, fontsize = 12)
 
# Adding Xticks
plt.ylabel('Success probability (%)', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(small_subtasks))],
        ['Task 1', 'Task 2', 'Task 3', 'Task 4', 'Task 5']) 
plt.tick_params(labelsize = 12)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5, fontsize = 15)
plt.show()