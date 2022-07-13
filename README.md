# Data Science Classes

<img src="Images/Classes_Data_Science.png" min-width="400px" max-width="400px" width="400px" align="center" alt="Classes_Data_Science">

## 📜 About this project

#### Classes to help with data science development and analysis that I came up with along my data sciene journey.

>At this point these classes are just an initial scketch that shall be improved as I go along.
>My intention is to build a library that can be used by other developers and data scientist alike.

#### 🚀 Built with
- 🐍Python
- 🐼Pandas
- 📝Numpy
- 📈Matplotlib
- 📉Seaborn
- 🪐Jupyter Notebook
- 🖼Drawio

####  ⬇️ Take a look at my Portfolio ⬇️
  
  [![Portfolio](https://img.shields.io/badge/Projects-Portfolio-blue)](andrewcode.herokuapp.com)
  
#### 🎯 General project status

![](https://us-central1-progress-markdown.cloudfunctions.net/progress/90)


##### ⭐️ Future classes to be added
- [ ] 📈 **Plotting class with seaborn and matplotlib**

    ![](https://us-central1-progress-markdown.cloudfunctions.net/progress/50)

    - Plotting multiple graphs in one figure with title, subtitle, legend, etc.
    - Most functions are available, but need to be organized and machined as a class
    - Figure out how to make it more flexible with different quantities of graphs in one figure. Probably with gridspec.
    - They also need to be generalized to handle datasets in various plot cases like bar charts, scatter plots, line charts, etc.

- [ ] 📝 **General data analysis descriptor class**

    ![](https://us-central1-progress-markdown.cloudfunctions.net/progress/70)

    - Generate tables like data types, missing values, statistics info about dataset, etc.
    - Most functions are available, but need to be organized and machined as a class
    - Easier to be generalized, since we'll just use default pandas functions


#### 📝 How to use this Project

##### 💻 Pre-requisites

Before starting, make sure you've met the following requirements:

- You have installed the latest version of Python, pandas, numpy, matplotlib, seaborn, and Jupyter Notebook.
    - At least Python 3.6 is required.
- You have either Windows, Linux or Mac machine.

##### 🚀 Installing Data Science Classes

To install the Data Science Classes, follow these steps:

- 📁 Select a folder which you want your project to live in.
```
...
📁 Data Science ⬅️ 💻 Start your terminal here 💻
    📁 Diamond_Analysis
    📁 Python_Studies
    📁 Iris_Analysis
    ...
```
- 💻 Install pandas, numpy, matplotlib, seaborn, and Jupyter Notebook with pip:

```
pip install pandas numpy matplotlib seaborn jupyter
```
- 💻 For now none of the classes are directly installable, but you can download them directly by cloning this repository:

```
git clone https://github.com/AndrewLaganaro/Data_Science_Classes
```
```
...
📁 Data Science
    📁 Diamond_Analysis
    📁 Python_Studies
    📁 Iris_Analysis
    📁 Data Science Classes
    ...
```

#### ☕ Using Data Science Framework
To use those classes take a look at each class description bellow.

##### 📚 Currently the following classes are available
- [x] 📊 **Dataset loader**

    ![](https://us-central1-progress-markdown.cloudfunctions.net/progress/90)

    - Intended to load files (8GB <) to help and agilize data loading in a given analysis.
    - Serves to import models, scalers, encoders and binary files in general used in machine learning

---
#### 📊 Dataset loader

This is the dataset loader class, it's intended to load files (8GB <) to help and agilize data loading in a given analysis.
It also serves to import models, scalers, encoders and binary files in general used by machine learning libraries like Scikit-learn, Tensorflow, Pytorch and others.

##### 🎯 General project status

![](https://us-central1-progress-markdown.cloudfunctions.net/progress/90)

##### ⭐️ Features to be finished
- [ ] Replace the direct folder naming by a directory group name, specified inside the .json file

    ![](https://us-central1-progress-markdown.cloudfunctions.net/progress/50)

    - Instead of 'folder name', specify 'directory group name' than may contain multiple folders inside
    
- [ ] Separate validation function from main class and move it to a separate file

    ![](https://us-central1-progress-markdown.cloudfunctions.net/progress/50)

    - Improve main class functioning readability.

##### ⭐️ Features to be added
- [ ] Support to parquet files
- [x] Support to csv files
- [x] Support to txt files
- [ ] Support to hdf5 files
- [x] Support to pickle files
- [x] Support to json files

---

####  ⬇️ Take a look at my Portfolio ⬇️
  
  [![Portfolio](https://img.shields.io/badge/Projects-Portfolio-blue)](andrewcode.herokuapp.com)
  
