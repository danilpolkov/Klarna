This case study pertains to a personalized product ranking problem similar to the one that we have in Klarna. Your task is to create a model that can predict top_100 items that a user might be interested in. Please populate the provided predictions.csv with 100 items for every ​visitorid in the file. Also note that you should not use the events for the month of Sep 2015 for training. Once done expose this model with an API endpoint that can return us a list of 100 ranked itemid​ for a given ​visitorid

structure:
```
|
|- data        -> folder with external and processed data
|
|- notebooks   -> folder with notebooks
|
|- src         -> folder with necessary functions
|
 ```
