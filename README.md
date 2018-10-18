# Data preprocessing applicaton for paper "Discovering User-context in Indoor Space".

We discover user-context in indoor space by combining activity and location context for user. 

This application is forked from [yscacaca/HHAR-Data-Process](https://github.com/yscacaca/HHAR-Data-Process) and modified for data preprocessing purpose in our project. Also, you can see our app for data collection [here](https://github.com/STEMLab/android_sensor_reader).

There is only two main files (``` stem_HHAR_data.py ``` and ``` stem_HHAR_data_eval.py ```) for data preprocessing, other files used for data analysis.

Edit following vars for your data:
 - ```pairSaveDir```: path to folder with your collected data;
 - ```gtType```: define actions performed by users in your data;
 - ```uList```: define list of user's id in your data;
 - ```roomList```: define list of rooms where data was collected;
 - ```outdir```: definde output path

Instructions:
- ``` stem_HHAR_data.py ``` - training data preparation. 
- ``` stem_HHAR_data.py ``` - eval data preparation.



