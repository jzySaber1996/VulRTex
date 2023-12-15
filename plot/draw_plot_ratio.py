import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

#! 解决不显示的问题：中文设置为宋体格式
plt.rcParams['font.family'] = ["Times New Roman", 'SimSun']

data_ablation_1 = pd.read_csv('result/result_test.csv')
df_ablation_1 = pd.DataFrame(data_ablation_1)

# fig, axs = plt.subplots(nrows=2, ncols=1)
palette=['#0068C2EE','#EFC000FF','#868686FF','#88EF00FF']

sns.lineplot(data=df_ablation_1, x="Ratio of Example-IR", y="Result (F1)", hue="Dataset&Experiment",palette=palette)  # 对掉x、y参数可以切换水平、垂直绘图
# axs[0,0].set_title("图1：舱位等级的年龄分布", fontsize=14)
# axs[0].xaxis.grid(True)
plt.ylim([0.3,1.0])
plt.xlim([0.3,0.9])
plt.xticks([0.3,0.4,0.5,0.6,0.7,0.8,0.9], ["30%","40%","50%","60%","70%","80%","90%"])
plt.grid(b=True, which='major', axis='both', color='grey', linewidth=0.5, alpha=0.5)

# # sns.boxplot(ax=axs[0,1], data=df, x="age", y="class", hue="alive")
# sns.boxplot(ax=axs[1], data=df, x="class", y="age", hue="alive")  # 对掉x、y参数可以切换水平、垂直绘图
# axs[1].set_ylabel('')
# # axs[0,1].set_title("图2：基于存活与否分组的舱位等级年龄分布", fontsize=14)
# axs[1].yaxis.grid(True)



plt.show()