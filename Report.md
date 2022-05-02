### Baseline Popularity


### ALS Model
[Small-Dataset]
We tried the below hypermeters:
regularizationParams = [.01, .05, .1, .2]
latentRanks = [10, 50, 100, 150]

Best Model - Rank: 50  RegParam: 0.1  
[Metrics]
 - RMSE: 0.8739 
 - Ranking Metrics (Mean average precision): 0.9612

[Large-Dataset]
regularizationParams = [.01, .05, .1, .2]
latentRanks = [10, 50, 100, 150]
Best Model - Rank: 150  RegParam: 0.05
[Metrics]
 - rmse 0.7153376384085554
 - Ranking Metrics (Mean average precision): 0.907697335721004