# Phonepe-Data-Visulazation
 In this project i have done dashbord regarding Phonepe Data of top 10 states, district, pincode, brand has the most number of users, total transaction amount , total transaction count and users appoppens frequency with intreactive Visualizations such as bar-chart , pie- chart and Geographical map 

 Demo video link - https://drive.google.com/file/d/1VMo3TuKCAfPTg2wTfhEPUJZBLnin3PS6/view?usp=share_link
 
 # Modules and libraries used in this project
 1. Plotly- used to ploting and visualizing the Data
 2. streamlit - dashbord
 3. MySQL - store data and retriving
 4. json - load the json files
 5. git.repo.base - it used to clone the github repository

# WorkFlow of Project
# Step 1
importing the libraries: which I hve mentioned in Modules and libraries used in the project

# Step 2
  Data extraction : Clone the phonepe pulse repository using scripts fetch and store it in applicable format such as json.

# Step 3
  Data Transformation : In this step the cloned data files are stored in json format and I have coverted into Csv files and stored in the local drive by using the pandas , json and os packages

# Step 4 
  Database insertion : To insert the dataframe into the Mysql first I created the connection between the python and mysql in python by using the mysql-connector library and the  I created the Tables to insert the transformed data into mysql database

# Step 5 
  Dashboard creation : to create Dashboard i've used plotly library in python to display bar-chart, pie-chart , geo map function are used to display the data on a charts and map  and streamlit is used to create the user friendly interface with multiple options to select and facts and figures to display in it 

# Step 6 
  Data retrival: Using mysql-connector library to connect the mysql database and fetch the data into the pandas data frame

  
