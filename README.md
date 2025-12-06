# Weather Crises
CMPSC 463 --- Project 2

# Weather Pattern Visualizer and Emergency Alert Prioritizer
Our project intends to utilize clustering algorithms such as K-means and a Weighted Scoring Model with dynamic datasets provided by OpenMeteo and the National Weather Service (NWS). The goal of our project is to produce a weather alert system using these algorithms, one that will be able to identify the location of storms and other weather events through the use of our clustering algorithm, and create a prioritized emergency alert order using our weighted scoring model.

# Overview
This project utilized two major algorithms in conjunction with two different dynamic datasets to produce the weather pattern visualizer and emergency alert prioritizer.
  - K-means Clustering Algorithm
  - Weighted Scoring Model

# K-means with OpenMeteo

The K-means clustering algorithm is used with OpenMeteo in order to visualize and locate significant weather events. OpenMeteo provides data on weather reports around the world. We have a dictionary of locations surrounding Abington, PA that are passed into OpenMeteo to collect weather data, which is reshaped in order to be used with K-means. By utilizing the K-means clustering algorithm, we are able to produce clusters of cities that share similar weather patterns. By visualizing these clusters on a map, we are able to determine the general weather of a given area by identifying which clusters relate to which weather events.

# Weighted Scoring with NWS

The Weighted Scoring Model is used with NWS in order to create a prioritized list of weather alerts. Weather alerts are pulled from NWS, utilizing the same location dictionary as before. Alerts are ranked by NWS with severity, certainty and urgency. Each of these features are ranked by one of five different terms that represent the increasing level. Our weighted scoring model rips these emergency alerts, and then provides an average score from 1-5 based on different weighted combinations of severity, certainty and urgency. Once all of these alerts have been ranked by the algorithm, a prioritized list is produced where emergency alerts with the highest score, which represents the most significant emergency, are sent first, while those with the lowest scores, which represents the least significant emergencies, are sent last.
