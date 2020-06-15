# IP-LP3-SUBMISSION-AI-Vikrant_Shah_1304

## Short Description of the files
- **CCFAQBot.py** - Code for the project is present in it
- **intents.json** - Contains the dataset for the **Cloud Counselage Pvt. Ltd.** FAQ Bot
- **CCFAQBot.tflearn** - Pre-trained model, to save the training time
- **requirements.txt** - All the project dependencies is saved here
- **data.pickle** - Contains the data seperated dataset. It saves the time to load the data everytime

## PRE-REQUISITES
- Anaconda Navigator
- Python version=3.6

## Steps to run the project
- Download all the files related to project
- Open Anaconda Prompt
- Navigate to the directory where the project is saved
> cd path_of_the_directory

- Create a virtual environment
> conda create -n CCFAQBot python=3.6

- Activate the virtual environment
> conda activate CCFAQBot

- Install project dependencies - **requirements.txt** contains all the packages saved to run the project
> pip install -r requirements.txt

- Run the project - **CCFAQBot.py** contains the code for the project
> python CCFAQBot.py

- Deactivate the virtual environment
> conda deactivate
