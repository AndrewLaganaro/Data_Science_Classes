# Data Science Classes
In this repository I share some Classes to help with data science development and analysis in general that I came up with along my data sciene journey. At this point these classes are just an initial scketch that shall be improved as I go along.

### Currently, the following classes are available:
- [x] **Dataset loader**

    ![](https://us-central1-progress-markdown.cloudfunctions.net/progress/90)

    - Intended to load files (8GB <) to help and agilize data loading in a given analysis.
    - Serves to import models, scalers, encoders and binary files in general used in machine learning

### Future classes to be added are:
- [ ] **Plotting class with seaborn and matplotlib**

    ![](https://us-central1-progress-markdown.cloudfunctions.net/progress/50)

    - Plotting multiple graphs in one figure with title, subtitle, legend, etc.
    - Most functions are available, but need to be organized and machined as a class
    - Figure out how to make it more flexible with different quantities of graphs in one figure. Probably with gridspec.
    - They also need to be generalized to handle datasets in various plot cases like bar charts, scatter plots, line charts, etc.

- [ ] **General data analysis descriptor class**

    ![](https://us-central1-progress-markdown.cloudfunctions.net/progress/70)

    - Generate tables like data types, missing values, statistics info about dataset, etc.
    - Most functions are available, but need to be organized and machined as a class
    - Easier to be generalized, since we'll just use default pandas functions

---
#### **Dataset loader**

This is the dataset loader class, it's intended to load files (8GB <) to help and agilize data loading in a given analysis.
It also serves to import models, scalers, encoders and binary files in general used by machine learning libraries like Scikit-learn, Tensorflow, Pytorch and others.

General project status (considering only fundamental functioning):

![](https://us-central1-progress-markdown.cloudfunctions.net/progress/90)

Features to be finalized currently are:
- [ ] Replace the direct folder naming by a directory group name, specified inside the .json file

    ![](https://us-central1-progress-markdown.cloudfunctions.net/progress/50)

    - Instead of 'folder name', specify 'directory group name' than may contain multiple folders inside
    
- [ ] Separate validation function from main class and move it to a separate file

    ![](https://us-central1-progress-markdown.cloudfunctions.net/progress/50)

    - Improve main class functioning readability.

##### **Features to be added currently are:**
- [ ] Support to parquet files
- [x] Support to csv files
- [x] Support to txt files
- [ ] Support to hdf5 files
- [x] Support to pickle files
- [x] Support to json files

---
