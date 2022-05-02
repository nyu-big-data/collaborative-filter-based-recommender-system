### Baseline Popularity

<table>
<tbody>
<tr>
<th>Model</th>
<th>Dataset</th>
<th>EvaluationSet</th>
<th>meanAveragePrecisionAtK</th>
<th>precisionAtK</th>
<th>ndcgAtK</th>
<th>recallAtK</th>
<th>RMSE</th>
<th>MAE</th>
</tr>
<tr>
<td>Baseline (basic)</td>
<td>ml-latest-small</td>
<td>val</td>
<td>0.1674193470873681</td>
<td>0.2657575757575758</td>
<td>0.30717186305586314</td>
<td>0.214635171587694</td>
<td>2.8900682424959547</td>
<td>2.6847254988141294</td>
</tr>
<tr>
<td>Baseline (basic)</td>
<td>ml-latest-small</td>
<td>test</td>
<td>0.13321330108620183</td>
<td>0.2497222222222223</td>
<td>0.30966303059594186</td>
<td>0.2512609472993407</td>
<td>2.716885155902375</td>
<td>2.5017895715351215</td>
</tr>
<tr>
<td>Baseline (enhanced)</td>
<td>ml-latest-small</td>
<td>val</td>
<td>0.11626666040246612</td>
<td>0.23060606060606068</td>
<td>0.27970893328293994</td>
<td>0.18752662891535993</td>
<td>0.9102298086888437</td>
<td>0.7173907756647717</td>
</tr>
<tr>
<td>Baseline (enhanced)</td>
<td>ml-latest-small</td>
<td>val</td>
<td>0.10531710427057707</td>
<td>0.21250000000000005</td>
<td>0.2581285662043938</td>
<td>0.20779147043731516</td>
<td>0.9265907297592388</td>
<td>0.7279776166058616</td>
</tr>
</tbody>
</table>



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
