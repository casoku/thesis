import numpy as np
import matplotlib.pyplot as plt
 
# set width of bar
barWidth = 0.1
fig = plt.subplots(figsize =(12, 8))
 
# set height of bar
small_subtasks = [0.82]
big_subtasks = [0.72]
DiRL = [0.65]
SPECTRL = [0.7]
# Set position of bar on X axis
br1 = np.arange(len(small_subtasks))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]
 
# Make the plot
bar1 = plt.bar(br1, small_subtasks, color ='firebrick', width = barWidth-0.02,
         label ='OM + small subtasks')
plt.bar_label(bar1, fontsize = 18)
bar2 = plt.bar(br2, big_subtasks, color ='darkgreen', width = barWidth-0.02,
        label ='OM + big subtasks')
plt.bar_label(bar2, fontsize = 18)
bar3 = plt.bar(br3, DiRL, color ='midnightblue', width = barWidth-0.02,
        label ='DiRL')
plt.bar_label(bar3, fontsize = 18)
bar4 = plt.bar(br4, SPECTRL, color ='darkorange', width = barWidth-0.02,
        label ='SPECTRL')
plt.bar_label(bar4, fontsize = 18)
 
# Adding Xticks
plt.ylabel('Success probability (%)', fontsize = 20)
plt.xticks([r + barWidth + 0.05 for r in range(len(small_subtasks))],
        ['Task 1']) 
plt.tick_params(labelsize = 15)
#plt.legend(loc = 'center left' , bbox_to_anchor=(1, 0.5), fontsize = 20)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5, fontsize = 18)
plt.show()