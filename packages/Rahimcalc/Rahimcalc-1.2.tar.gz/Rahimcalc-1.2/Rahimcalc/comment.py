from tkinter import *
import Rahimcalc as rc
import sys
import random as r
def main():
    l=len(sys.argv)
    if(sys.argv[1]=='1'):
        if(sys.argv[2]=='1'):
            if(sys.argv[3]=='a'):
                s="""import numpy as np\nx=np.zeros(10)\nprint(x)\nprint("Update sixth value to 11")\nx[6]=11\nprint(x)"""
            if(sys.argv[3]=='b'):
                s="""import numpy as np\na=[1,2,3,4]\nprint("Original arrray")\nprint(a)\nx=np.asfarray(a)\nprint("Array Converted to a float type:")\nprint(x)"""
            if(sys.argv[3]=='c'):
                s="""import numpy as np\nx=np.arange(2,11).reshape(3,3)\nprint(x)"""
            if(sys.argv[3]=='d'):
                s="""import numpy as np\nl=[12.23,13.32,100,36.32]\nprint("Original List:",l)\na=np.array(l)\nprint("one-Dimensional numpy array:",a)"""
        if(sys.argv[2]=='2'):
            if(sys.argv[3]=='a'):
                s="""import numpy as np\na=[1,2,3,4]\nprint("Original Array")\nprint(a)\nx=np.asfarray(a)\nprint("Array Converted to a float type:")\nprint(x)"""
            if(sys.argv[3]=='b'):
                s="""import numpy as np\nemp=np.empty((3,4),dtype=int)\nprint("Empty Array")\nprint(emp)\nfll=np.full([3,3],55,dtype=int)\nprint("\n full Array")\nprint(fll)"""
            if(sys.argv[3]=='c'):
                s="""import numpy as np\nmy_list=[1,2,3,4,5,6,7,8]\nprint("List yo array:")\nprint(np.asarray(my_list))\nmy_tuple=([8,4,6],[1,2,3])\nprint("Tuple to Array:")\nprint(np.asarray(my_tuple))"""
            if(sys.argv[3]=='d'):
                s="""import numpy as np
x=np.sqrt([1+0j])
y=np.sqrt([0+1j])
print("Original Array:x",x)
print("Original Array:y",y)
print("Real Part Of The Array:")
print(x.real)
print(y.real)
print("Imagine Part of The Array:")
print(x.imag)
print(y.imag)
"""
        if(sys.argv[2]=='3'):
            s="""import pandas as pd\ndf=pd.DataFrame({'x':[78,85,96,80,86],'y':[84,94,89,83,86],'z':[86,97,96,72,83]})\nprint(df)"""
        if(sys.argv[2]=='4'):
            s="""import pandas as pd\nexam_data  = {'name': ['Anastasia', 'Dima', 'Katherine', 'James', 'Emily', 'Michael', 'Matthew', 'Laura', 'Kevin', 'Jonas'],
        'score': [12.5, 9, 16.5, np.nan, 9, 20, 14.5, np.nan, 8, 19],
        'attempts': [1, 3, 2, 3, 2, 3, 1, 1, 2, 1],
        'qualify': ['yes', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes']}\nlabels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']\ndf = pd.DataFrame(exam_data , index=labels)\nprint("Select specific columns and rows:")\nprint(df.iloc[[1, 3, 5, 6], [1, 3]])"""
        if(sys.argv[2]=='5'):
            s="""import pandas as pd\nexam_data  = {'name': ['Anastasia', 'Dima', 'Katherine', 'James', 'Emily', 'Michael', 'Matthew', 'Laura', 'Kevin', 'Jonas'],
        'score': [12.5, 9, 16.5, np.nan, 9, 20, 14.5, np.nan, 8, 19],
        'attempts': [1, 3, 2, 3, 2, 3, 1, 1, 2, 1],
        'qualify': ['yes', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes']}\nlabels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']\ndf = pd.DataFrame(exam_data , index=labels)\ntotal_rows=len(df.axes[0])\ntotal_cols=len(df.axes[1])\nprint("Number of Rows: "+str(total_rows))\nprint("Number of Columns: "+str(total_cols))\nprint(np.nan)"""
        if(sys.argv[2]=='6'):
            s="""#Data Collect
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
dataset=pd.read_csv("C:\\iris.txt")
dataset.head()
dataset=pd.read_excel("C:\\iris.xlsx")
dataset.head()
dataset=pd.read_csv("C:\\iris.csv")
dataset.head()
dataset.info()
dataset.Species.unique()
#EDA
dataset.describe()
dataset.corr()
dataset.Species.value_counts()
sns.FacetGrid(dataset,hue="Species",size=6).map(plt.scatter,"Sepal.Length","Sepal.Width").add_legend()
sns.FacetGrid(dataset,hue="Species",size=6).map(plt.scatter,"Petal.Length","Petal.Width").aadd_legend()
sns.pairplot(dataset,hue="Species")
plt.hist(dataset["Sepal.Length"],bin=25);
sns.FacetGrid(dataset,hue="Species",size=6).map(sns.displot,"Sepal.Width").add_legend();
sns.boxplot(x='Species',y='Petal.Length',data=dataset)
#Preprocessing
from sklearn.preprocessing import StandardScaler
ss=StandardScaler()
x=dataset.drop(['Species'],axis=1)
y=dataset['Species']
scaler=ss.fit(x)
x_stdscaler=scaler.transform(x)
x_stdscaler
from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
y=le.fit_transform(y)
#Splitting
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=42)
x_train.value_counts
#Model Selection
from sklearn.svm import SVC
svc=SVC(kernel="linear")
svc.fit(x_train,y_train)
y_pred=svc.predict(x_test)
y_pred
from sklearn.metrics import accuracy_score
accuracy_score(y_pred,y_test)
#Prediction
from sklearn.neighbors import KNeighborsClassifier
knn=KNeighborsClassifier(n_neighbors=3)
knn.fit(x_train,y_train)
KNeighborsClassifier(n_neighbors=3)
y_pred=knn.predict(x_test)
accuracy_score(y_pred,y_test)"""
        if(sys.argv[2]=='7'):
            s="""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv("C:\\pima-indians-diabetes.csv")
df.head()
df.mean(axis = 0)
print(df.loc[:,'35'].mean())
df.mean(axis = 1)[0:5]
df.median()
print(df.loc[:,'33.6'].median())
df.median(axis = 1)[0:5]
df.mode()
df.std()
print(df.loc[:,'35'].std())
df.std(axis = 1)[0:5]
df.var()
print(df.skew())
print(df.kurtosis())
norm_data = pd.DataFrame(np.random.normal(size=100000))
norm_data.plot(kind="density",figsize=(10,10));
# Plot black line at mean
plt.vlines(norm_data.mean(),ymin=0, ymax=0.4,linewidth=5.0);
# Plot red line at median
plt.vlines(norm_data.median(),   ymin=0, ymax=0.4, linewidth=2.0,color="red");"""
        if(sys.argv[2]=='8'):
            s="""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
%matplotlib inline
diabetes=pd.read_csv("C:\\pima-indians diabetes.csv")
diabetes.head()
diabetes = datasets.load_diabetes()
diabetes
print(diabetes.DESCR)
diabetes.feature_names
# Now we will split the data into the independent and independent variable
X = diabetes.data[:,np.newaxis,3]
Y = diabetes.target
#We will split the data into training and testing data
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.3)
# Linear Regression
from sklearn.linear_model import LinearRegression,LogisticRegression
reg=LinearRegression()
reg.fit(x_train,y_train)
y_pred = reg.predict(x_test)
Coef=reg.coef_
print(Coef)
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import metrics
MSE=mean_squared_error(y_test,y_pred)
R2=r2_score(y_test,y_pred)
print(R2,MSE)
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
plt.scatter(y_pred, y_test)
plt.title('Predicted data vs Real Data')
plt.xlabel('y_pred')
plt.ylabel('y_test')
plt.show()
plt.scatter(x_test, y_test)
plt.plot(x_test,y_pred,linewidth=2)
plt.title('Linear Regression')
plt.xlabel('y_pred')
plt.ylabel('y_test')
plt.show()
model = LogisticRegression()
model.fit(x_train,y_train)
y_predict=model.predict(x_test)
model_score = model.score(x_test,y_test)
print(model_score)
print(metrics.confusion_matrix(y_test, y_predict))"""
        if(sys.argv[2]=='9'):
            s="""import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import datasets
%matplotlib inline
diabetes=pd.read_csv("C:\\pima-indians-diabetes.csv")
diabetes.head()
import statsmodels.api as sm
from statsmodels.stats.anova import anova_lm
X = diabetes[["Age", "BMI"]]## the input variables
y = diabetes["Glucose"] ## the output variables, the one you want to predict
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model
# Note the difference in argument order
model2 = sm.OLS(y, X).fit()
predictions = model2.predict(X) # make the predictions by the model
# Print out the statistics
model2.summary()"""
        if(sys.argv[2]=='10'):
            if(sys.argv[3]=='a'):
                s="""import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sn
%matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
df=pd.read_csv("C:\\train.csv")
df.head()
mean = df.loc[:,'Fare'].mean()
sd = df.loc[:,'Fare'].std()
plt.plot(x_axis, norm.pdf(x_axis, mean, sd))
plt.show()
"""
            if(sys.argv[3]=='b'):
                s="""import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sn
%matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
df=pd.read_csv("C:\\train.csv")
df.head()
sns.distplot(df["Fare"])
sns.distplot(df["Age"])
plt.contour(df[["Fare","Parch"]])"""
            if(sys.argv[3]=='c'):
                s="""import numpy as np
import pandas as pd
import seaborn as sn
%matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
df=pd.read_csv("C:\\train.csv")
df.head()
%matplotlib inline
fig = plt.figure(figsize=(8,8))
ax = plt.axes(projection='3d')
ax = plt.axes(projection='3d')
zline = np.linspace(0, 15, 1000)
xline = np.sin(zline)
yline = np.cos(zline)
ax.plot3D(xline, yline, zline, 'gray')
zdata = df[["Fare"]]
xdata = df[["Age"]]
ydata = df[["Parch"]]
ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens');

"""
        if(sys.argv[2]=='11'):
            if(sys.argv[3]=='a'):
                s="""import numpy as np
import pandas as pd
importseaborn as sn
%matplotlib inline
importseaborn as sns
importmatplotlib.pyplot as plt
df=pd.read_csv("C:\\train.csv")
df.head()
plt.figure(figsize=(8,8))
sn.scatterplot(x="Age", y="Fare", hue="Sex", data=df)
plt.show()
df.corr()
# plotting correlation heatmap
dataplot = sns.heatmap(df.corr(), cmap="YlGnBu", annot=True)
# displaying heatmap
plt.show()"""
            if(sys.argv[3]=='b'):
                s="""import numpy as np
import pandas as pd
importseaborn as sn
%matplotlib inline
importseaborn as sns
importmatplotlib.pyplot as plt
df=pd.read_csv("C:\\train.csv")
df.head()
plt.hist(df["Fare"])"""
            if(sys.argv[3]=='c'):
                s="""import numpy as np
import pandas as pd
import seaborn as sn
%matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
df=pd.read_csv("C:\\train.csv")
df.head()
%matplotlib inline
fig = plt.figure(figsize=(8,8))
ax = plt.axes(projection='3d')
ax = plt.axes(projection='3d')
zline = np.linspace(0, 15, 1000)
xline = np.sin(zline)
yline = np.cos(zline)
ax.plot3D(xline, yline, zline, 'gray')
zdata = df[["Fare"]]
xdata = df[["Age"]]
ydata = df[["Parch"]]
ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens');
"""
        if(sys.argv[2]=='12'):
            if(sys.argv[3]=='a'):
                s="""import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sn
%matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
df=pd.read_csv("C:\\pima-indians-diabetes.csv")
df.head()
mean = df.loc[:,'Fare'].mean()
sd = df.loc[:,'Fare'].std()
plt.plot(x_axis, norm.pdf(x_axis, mean, sd))
plt.show()
"""
            if(sys.argv[3]=='b'):
                s="""import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sn
%matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
df=pd.read_csv("C:\\pima-indians-diabetes.csv")
df.head()
sns.distplot(df["Fare"])
sns.distplot(df["Age"])
plt.contour(df[["Fare","Parch"]])"""
            if(sys.argv[3]=='c'):
                s="""import numpy as np
import pandas as pd
import seaborn as sn
%matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
df=pd.read_csv("C:\\pima-indians-diabetes.csv")
df.head()
%matplotlib inline
fig = plt.figure(figsize=(8,8))
ax = plt.axes(projection='3d')
ax = plt.axes(projection='3d')
zline = np.linspace(0, 15, 1000)
xline = np.sin(zline)
yline = np.cos(zline)
ax.plot3D(xline, yline, zline, 'gray')
zdata = df[["Fare"]]
xdata = df[["Age"]]
ydata = df[["Parch"]]
ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens');
"""
        if(sys.argv[2]=='13'):
            if(sys.argv[3]=='a'):
                s="""import numpy as np
import pandas as pd
import seaborn as sn
%matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
df=pd.read_csv("C:\\pima-indians-diabetes.csv")
df.head()
plt.figure(figsize=(8,8))
sn.scatterplot(x="Age", y="Fare", hue="Sex", data=df)
plt.show()
df.corr()
# plotting correlation heatmap
dataplot = sns.heatmap(df.corr(), cmap="YlGnBu", annot=True)
# displaying heatmap
plt.show()"""
            if(sys.argv[3]=='b'):
                s="""import numpy as np\nimport pandas as pd\nimport seaborn as sn\n%matplotlib inline\nimport seaborn as sns\nimport matplotlib.pyplot as plt\ndf=pd.read_csv("C:\\pima-indians-diabetes.csv")\ndf.head()\nplt.hist(df["Fare"])"""
            if(sys.argv[3]=='c'):
                s="""import numpy as np
import pandas as pd
import seaborn as sn
%matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
df=pd.read_csv("C:\\pima-indians-diabetes.csv")
df.head()
%matplotlib inline
fig = plt.figure(figsize=(8,8))
ax = plt.axes(projection='3d')
ax = plt.axes(projection='3d')
zline = np.linspace(0, 15, 1000)
xline = np.sin(zline)
yline = np.cos(zline)
ax.plot3D(xline, yline, zline, 'gray')
zdata = df[["Fare"]]
xdata = df[["Age"]]
ydata = df[["Parch"]]
ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens');"""
        if(sys.argv[2]=='14'):
            s="""import pandas as pd\nd = {'col1': [1, 2, 3, 4, 7], 'col2': [4, 5, 6, 9, 5], 'col3': [7, 8, 12, 1, 11]}\ndf = pd.DataFrame(data=d)\nprint("Original DataFrame")\nprint(df)\nprint("\nNumber of columns:")\nprint(len(df.columns))"""
        if(sys.argv[2]=='15'):
            s="""import pandas as pd\ndf = pd.DataFrame( {'col1':['C1','C1','C2','C2','C2','C3','C2'], 'col2':[1,2,3,3,4,6,5]})\nprint("Original DataFrame")\nprint(df)\ndf = df.groupby('col1')['col2'].apply(list)\nprint("\nGroup on the col1:")\nprint(df)"""
        if(sys.argv[2]=='16'):
            s="""import pandas as pd
d = {'col1': [1, 2, 3, 4, 7], 'col2': [4, 5, 6, 9, 5], 'col3': [7, 8, 12, 1, 11]}
df = pd.DataFrame(data=d)
print("Original DataFrame")
print(df)
if 'col4' in df.columns:
  print("Col4 is present in DataFrame.")
else:
  print("Col4 is not present in DataFrame.")
if 'col1' in df.columns:
  print("Col1 is present in DataFrame.")
else:
  print("Col1 is not present in DataFrame.")"""
        if(sys.argv[2]=='17'):
            s="""import numpy as np\nx = np.array([10,-10,10,-10,-10,10])\ny = np.array([.85,.45,.9,.8,.12,.6])\nprint("Original arrays:")\nprint(x)\nprint(y)\nresult = np.sum((x == 10) & (y > .5))\nprint("\nNumber of instances of a value occurring in one array on the condition of another array:")\nprint(result)"""
        if(sys.argv[2]=='18'):
            s="""import numpy as np\nnp_array = np.array([[1, 2, 3], [2, 1, 2]], np.int32)\nprint("Original Numpy array:")\nprint(np_array)\nprint("Type: ",type(np_array))\nprint("Sequence: 1,2",)\nresult = repr(np_array).count("1, 2")\nprint("Number of occurrences of the said sequence:",result)"""
        if(sys.argv[2]=='19'):
            s="""import numpy as np\narr1 = np.random.random(size=(25, 25, 1))\narr2 = np.random.random(size=(25, 25, 1))\narr3 = np.random.random(size=(25, 25, 1))\nprint("Original arrays:")\nprint(arr1)\nprint(arr2)\nprint(arr3)\nresult = np.concatenate((arr1, arr2, arr3), axis=-1)\nprint("\nAfter concatenate:")\nprint(result) """
        if(sys.argv[2]=='20'):
            s="""import numpy as np\narray1 = ['PHP','JS','C++']\narray2 = ['Python','C#', 'NumPy']    \nprint("Original arrays:")          \nprint(array1)\nprint(array2)          \nresult  = np.r_[array1[:-1], [array1[-1]+array2[0]], array2[1:]]   \nprint("\nAfter Combining:")\nprint(result)"""
    if(sys.argv[1]=='2'):
        print("Batch-2")
    import os
    path="C:\\Users\\"+os.getlogin()+"\\Desktop\\output.txt"
    py=path="C:\\Users\\"+os.getlogin()+"\\Desktop\\output.py"
    f=open(path,'w')
    f1=open(py,'w')
    print(s,file=f)
    print(s,file=f1)
    f.close()
    f1.close()
'''
    try:
        m=sys.argv[1]
    except:
        m='-h'
    match(m):
        case '-h':
            print(help1)
        case '-c':
            print("Rahimcalc {comment}")
        case '-i':
            a=int(input("Enter the first value:"))
            b=int(input("Enter the second value:"))
            s=str(input("Enter the opertor:"))
            #main1(a,b,s)
        case '-r':
            print("RT")
            a=r.choice(f)
            b=r.choice(f)
            s=['+','-','*','/','^','&']
            for i in s:
                main1(a,b,s)
        case _:
            print("Invalid choice")
    if s=='sum' or '+':
        print(rc.sum(a,b))
    if s=='sub' or '-':
        print(rc.sub(a,b))
    if s=='mul' or '*':
        print(rc.mul(a,b))
    if s=='div' or '/':
        print(rc.div(a,b))
    if s=='exp' or '^':
        print(rc.exp(a,b))
    if s=='complex' or '&':
        print(rc.complex(a,b))
    '''
if __name__=='__main__':
    main()
