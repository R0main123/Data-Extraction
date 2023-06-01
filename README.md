# Data-Extraction
## Table of Contents
1. [Description of the project](#project-description)
2. [Installation instructions](#instructions)
3. [User's guide](#User's guide)
4. [Data structure](#Data Structure)
4. [Documentation](#Documentation)


## Description of the project
**This project is designed to work exclusively on windows. If needed, please contact me and I will be delighted to adapt it to Unix machines.**

This projects aims to obtain all information needed from a simple .txt file containing information about a wafer's measurements: 
* An Excel file with all the measurements, with one sheet per coordinates
* Two PowerPoint File with all plots: one with current value depending on voltage, and the other with current density depending on voltage.

## Installation instructions 
### Windows
#### Software needed
Please ensure that you have **Python 3.8** or a newer python distribution.  
#### Requirements 
This project uses some python libraries to work correctly. Please run

```pip install -r requirements.txt```


## User's guide 
Please open **main.py** and run the program. A User Interface should open and here, chose if you want to plot I-V datas, J-V datas or both. This will decide of the PowerPoint's structure. 

Then, a window opens and here, you can drag and drop as many files as you want. Three new folders should have been created:
* **plots:** It contains all plots separately. One file conatains all plots for a couple of coordinates. The name of a file is the name of the wafer with corresponding coordinates and if it's a I-V or a J-V plot.
*  **PowerPoint files:** It contains all PowerPoint files, named afet this convention: 
``name of the wafer + "plot_" + IV or JV, depending on what the user wants``
* **Excel Files:** It contains an Excel file per txt file treated. This file contains all measuremets and as many sheets as the wafer has coordinates.

## Data Structure
Datas are registred in a MongoDB database. MongoDB is like a digital library that lets you store your datas in custom-sized boxes, makes it easy to handle nested and complex datas. That's why it is relevant to use it here, knowing the structure of our datas.

Our datas are stored this way: In the database, there are multiple wafers. Each wafer has an ID and contains a list of structures (Structures are testdeviceIDs). Like wafers, each structure has his own ID and has a list of dies. Finally, each die have an ID, and contains 2 information: 
* A couple of coordinates 
* 2 array of results. Each contains type of measurements (I-V or J-V) and a list of couples of values. Value 0 is voltage and Value 1 is current, if we are in I-V measurement, or current density if we are in J-V Measurements.

Here is a schema of the data structure used:
![Data structure used](images\WaferStructure.png)

## Documentation
A documentation is available for this project. Please run

``cd Documentation/build/html``

and open ``index.html`` with a web browser (Chrome, Firefox, Edge...).





























