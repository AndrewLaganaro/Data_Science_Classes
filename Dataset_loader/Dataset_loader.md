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
