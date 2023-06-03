# Player Compensation Model for Professional American Football Athletes

## Motivation
In the National Football League (NFL) there are many rookies that enter the league and go on to have varying levels of success in their careers. Evaluation of the rookies' performance and predicting their value in the NFL can be very beneficial to teams looking to either move on from their rookie players or retain rookie talent that can become the cornerstone of their franchise. We will be using early career statistics from rookies in the NFL to evaluate their value in the league and predict their expected salaries to determine their expected value after their rookie years in the NFL. We will be using performance statistics from the rookie years of players in the NFL between the timeline of the years 2000-2022 as our database. Particularly, we will be analyzing the positions of quarterback (QB), running back (RB), wide receiver (WR), and tight end (TE) on the offensive side. We will be using AutoML to determine the best machine learning model to implement for our rookie evaluation, and then comparing accuracy statistics to contracts assigned after rookie performances to determine the efficiency and effectiveness of our model compared to the decisions made by the league in terms of contract assignments. 

The goal of this project is to predict what a NFL player’s salary should be after their rookie contract (4 years) is over. Currently, there is no set metric to evaluate a rookie after their first 4 years and the contract is determined based on what the team thinks the player’s potential is. We aim to utilize machine learning methods to analyze data from previous rookies and predict what players should be making in the future.
## Methods
For this project we decided that we would have to create our own dataset since there were no existing datasets that included the attributes that we required to be able to perform our predictions. Therefore, we created a dataset for players in the NFL between the years of 2011-2022 by web scraping from pro-footbal-reference.com[7] to take the performance metrics for the positions of quarterback (QB), running back (RB), wide receiver (WR), and tight end (TE) on the offensive side. The features for each position can be seen in tables below. We then had to scrape[16] salary information from Spotrac.com[5] for each of these players, ensuring to include their contract information for their rookie contract as well as the contract information for their first non-rookie contract in the league. Contract information included: contract length, contract salary, percent of the cap, new contract length, new percent of cap, contract years left. The percent of the cap, new contract length, new percent of cap, contract year left variables were not publicly available so we had to create functions to make those variables.

After the data was collected it was cleaned so that it could be utilized for machine learning. Four data frames were created for each of the four positions (QB, WR, RB, TE). The final step in our data preparation process involved standardizing all the player’s stats. This was done by converting player stats to z scores for each year. This allowed the model to better contextualize the data. The final data sets can be viewed [here](https://github.com/r-gram/PlayerCompensationModel/tree/main/Data).


![Data Set Sizes](https://github.com/r-gram/PlayerCompensationModel/blob/main/Data/images/QBTD2CON.PNG?raw=true)
## Results
![QB Results](https://github.com/r-gram/PlayerCompensationModel/blob/main/Data/images/QB_Results.PNG?raw=true)

![RB Results](https://github.com/r-gram/PlayerCompensationModel/blob/main/Data/images/RB_Results.PNG?raw=true)

![TE Results](https://github.com/r-gram/PlayerCompensationModel/blob/main/Data/images/TE_Results.PNG?raw=true)

![WR Results](https://github.com/r-gram/PlayerCompensationModel/blob/main/Data/images/WR_Results.PNG?raw=true)

## How to Run
All code is in an easy-to-use Jupyter Notebook. To run, download the [Notebook](https://github.com/r-gram/PlayerCompensationModel/tree/main/modelsML/JNotebooks) and insure that all necessary packages are downloaded. 
Packages Needed:
- [FLAML](https://microsoft.github.io/FLAML/docs/Installation/)
- [Matplotlib](https://matplotlib.org/stable/users/installing/index.html)
- [Pandas](https://pandas.pydata.org/docs/getting_started/install.html)
- [NumPy](https://numpy.org/install/)
- [SciKit-Learn](https://scikit-learn.org/stable/install.html)

The data used to train the models can be found [here]https://github.com/r-gram/PlayerCompensationModel/tree/main/Data).

## Contributors
[Robert Gramlich](https://www.linkedin.com/in/robert-gramlich/)
[Sam Rioboli](https://www.linkedin.com/in/samrioboli/)
[Eric Loro](https://www.linkedin.com/in/erik-loro/)
[Cinah Pourhamidi](https://www.linkedin.com/in/cinah-p-0a6a17101/)

## Citations
[1]Draisey , T. (2016). The determinants of NFL player salaries - University of Northern Iowa. UNI ScholarWorks. Retrieved from https://scholarworks.uni.edu/cgi/viewcontent.cgi?article=1218&context=hpt
[2]Gosavi, P. (2022, April 29). Salary Cap Efficiency: A Study of the Relationship between a NFL Quarterback’ terback’s Salar s Salary and their T y and their Team’s Performance formance UCONN Library. Retrieved from
https://opencommons.uconn.edu/cgi/viewcontent.cgi?article=1890&context=srhonors_theses
[3]Mulholland, J. (2016). Optimizing the Allocation of Funds of an NFL Team under the Salary Cap, while Considering Player Talent . Penn Libraries. Retrieved from https://repository.upenn.edu/cgi/viewcontent.cgi?referer=&httpsredir=1&article=1018&context=joseph_wharton_scholars
[4]Mulholland, J., & Jensen, S. T. (n.d.). Predicting the future of free agent receivers and tight ends in the NFL. Italian Journal of Applied Statistics Vol. 30. Retrieved from http://www-stat.wharton.upenn.edu/~stjensen/papers/shanejensen.football.freeagents.2018.pdf
[5]Spotrac.com. (n.d.). Jalen Hurts. Spotrac.com. Retrieved February 10, 2023, from https://www.spotrac.com/nfl/philadelphia-eagles/jalen-hurts-47648/market-value/
[6]Jhonsen. (n.d.). Jhonsen/NFLplayersValuation: Project-2 at Metis Data Science Bootcamp. GitHub. Retrieved February 10, 2023, from https://github.com/jhonsen/NFLplayersValuation
[7]Pro-Football-Reference.com. (n.d.). Jalen Hurts. Pro-Football-Reference.com.
Retrieved February 10, 2023, from https://www.pro-football-reference.com/players/H/HurtJa00.htm
[8]AutoML.com. (n.d.). AutoML. AutoML.com. Retrieved February 10, 2023, from
https://www.automl.org/
[9]Jain, S. (2022). A Non-Linear Approach to Predict the Salary of NBA Athletes using Machine Learning Technique. IEEE Explore. Retrieved February 23, 2023, from https://ieeexplore.ieee.org/abstract/document/10041664?casa_token=2uWNHKswqmkAAAAA:-LpLbRU_kFFvwuXjw7d3Y1UsS5VwHBdTJLaJE-iIF_-qtg7ELIGyRDHLQn1ySv-ljATOqQ
[10]Task oriented automl. FLAML. (2023). Retrieved February 23, 2023, from
https://microsoft.github.io/FLAML/docs/Use-Cases/Task-Oriented-AutoML/#estimator-and-search-space
[11]Team, K. (n.d.). Keras Documentation: Keras API reference. Keras. Retrieved
February 21, 2023, from https://keras.io/api/
[12]Team, K. (n.d.). Keras documentation: Dense layer. Keras. Retrieved February 21, 2023, from https://keras.io/api/layers/core_layers/dense/
[13]Team, K. (n.d.). Keras Documentation: The sequential model. Keras. Retrieved February 21, 2023, from https://keras.io/guides/sequential_model/
[14]Brownlee, J. (2020, August 27). Deep learning models for multi-output regression. MachineLearningMastery.com. Retrieved February 21, 2023, from
https://machinelearningmastery.com/deep-learning-models-for-multi-output-regression/
[15]Spielberger, B. (2020, August 28). Introducing PFF contract projections: A new way to look at NFL contracts: NFL News, rankings and Statistics. PFF. Retrieved March 16, 2023, from https://www.pff.com/news/nfl-introducing-pff-contract-projections
[16] AdamAAdamA 34311 gold badge22 silver badges1111 bronze badges, et al.
“Beautiful Soup Scrape - Login Credentials Not Working.” Stack Overflow, 1 Dec. 1966, https://stackoverflow.com/a/60725158.
