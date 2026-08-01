import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_csv('data/stud.csv')
print(df.columns.tolist())
print(df[['gender', 'parental_level_of_education']].head())

fig, axes = plt.subplots(1, 3, figsize=(25, 6))
sns.histplot(data=df, x='average', kde=True, hue='parental level of education', ax=axes[0])
sns.histplot(data=df[df.gender == 'male'], x='average', kde=True, hue='parental level of education', ax=axes[1])
sns.histplot(data=df[df.gender == 'female'], x='average', kde=True, hue='parental level of education', ax=axes[2])
plt.tight_layout()
plt.savefig('test_plot.png')
print('plot ok')
