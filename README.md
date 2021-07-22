# Project-Sandbox
Project-Sandbox is a collection of different useful and interesting Data Science, ML, DL and NLP applications that are both easy to learn and fun to use. You can check out the very first app here: [DataDissect](https://share.streamlit.io/nikhilbartwal/project-sandbox/main/Sandbox_app.py)
  
# Table of Contents

* [About the App](#about-the-app)
* [Screenshots](#screenshots)
* [Contents of Repo](#contents-of-repo)
* [Installation](#installation)
* [Technologies](#technologies)
* [Future Goals](#future-goals)

# About the Project
Project-Sandbox houses a wide variety of apps, each complete on its own and serving various function, with all of them woven together in a complex web app. The most prominent apps being:

## 1. DataDissect
  
 DataDissect lets the user pre-process the dataset completely including fillinf in missing values, changing data types and even handling categorical data with a neat GUI, without
  writing a single piece of code.<br>
  Not only this it also provides the user the feature to perform univariate and bivariate analysis and visualizations for any dataset by simply selecting the variables, the kind of plot/graphs and the library that the user wants to use and DataDissect will take care of the rest.
  
  Here are some screenshots of the app in action:
  
  <SCREENSHOTS>
    
## 2. Once Upon a Time
    
Now, this is a really cool application that I'm currently working on. IT basically lets the user enter a single line and select a genre and the system will generate a complete story of that genre by itself, simply by taking that line and feeding it to a cutting-edge NLP model.
    
Here are some screenshots of the app in action:

# What's in the repo?

Almost all the interesting stuff happens inside the `PLAYABLES` folder, which houses a separate folder for each application. The project structure is something like this:
    
    playables
    |
    |-- DataDissect
    |      |-- data_dissect.py
    |      |-- preprocess.py
    |      |-- preprocess_logic.py
    |      |-- utils.py
    |-- Once Upon a Time
    |          |
    |          |
    |          |
    
### Role of individual files:
    
* **data_dissect.py:** Main wrapper which displays all the avilable features of DataDissect (like Pre-processing, Visualizations etc.)<br>
* **preprocess.py:** Contains the wrapper code for displaying the various pre-processing options and its control flow (like missing values, type conversion etc.)<br>
* **preprocess_logic.py:** Consists of all the complex pre-processing and the logic that is used by the different Pre-processing options.<br>
* **utils.py:** Consists of the various utility functions which are used in this application<br>
