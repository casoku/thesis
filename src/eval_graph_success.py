import numpy as np
import matplotlib.pyplot as plt
 
# set width of bar
barWidth = 0.2
fig = plt.subplots(figsize =(12, 8))
 
# set height of bar
small_subtasks = [0.87, 0.65, 0.87, 0.82, 0.41]
std_small_subtasks = [0.013, 0.019, 0.014, 0.013, 0.02]
#std_small_subtasks = [0.019, 0.02, 0.017, 0.019] calculated wrong?
big_subtasks = [0.72, 0.31, 0.62, 0.56, 0.13]
std_bigsubtasks = [0.018, 0.019, 0.02, 0.02, 0.014]
DiRL = [0.65, 0.37, 0.57, 0.54, 0]
std_DiRL = [0.019, 0.02, 0.02, 0.02, 0]
SPECTRL = [0.7, 0, 0.56, 0, 0]
std_SPECTRL = [0.019, 0, 0.02, 0, 0]
# Set position of bar on X axis
br1 = np.arange(len(small_subtasks))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]
 
# Make the plot
bar1 = plt.bar(br1, small_subtasks, yerr = std_small_subtasks, color ='firebrick', width = barWidth-0.02, capsize =6,
         label ='OM + small subtasks')
plt.bar_label(bar1, fontsize = 12)
bar2 = plt.bar(br2, big_subtasks, yerr = std_bigsubtasks, color ='darkgreen', width = barWidth-0.02, capsize =6,
        label ='OM + big subtasks')
plt.bar_label(bar2, fontsize = 12)
bar3 = plt.bar(br3, DiRL, yerr = std_DiRL, color ='midnightblue', width = barWidth-0.02, capsize =6,
        label ='DiRL')
plt.bar_label(bar3, fontsize = 12)
bar4 = plt.bar(br4, SPECTRL, yerr = std_SPECTRL, color ='darkorange', width = barWidth-0.02, capsize = 6,
        label ='SPECTRL')
plt.bar_label(bar4, fontsize = 12)
 
# Adding Xticks
plt.ylabel('Success probability', fontsize = 15)
plt.xticks([r + barWidth for r in range(len(small_subtasks))],
        ['Task 1', 'Task 2', 'Task 3', 'Task 4', 'Task 5']) 
plt.tick_params(labelsize = 12)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5, fontsize = 15)
plt.show()