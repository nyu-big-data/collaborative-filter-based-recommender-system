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
<td>0.1674</td>
<td>0.2657</td>
<td>0.3071</td>
<td>0.2146</td>
<td>2.8901</td>
<td>2.6847</td>
</tr>
<tr>
<td>Baseline (basic)</td>
<td>ml-latest-small</td>
<td>test</td>
<td>0.1332</td>
<td>0.2497</td>
<td>0.3097</td>
<td>0.2513</td>
<td>2.7168</td>
<td>2.5017</td>
</tr>
<tr>
<td>Baseline (enhanced)</td>
<td>ml-latest-small</td>
<td>val</td>
<td>0.1162</td>
<td>0.2306</td>
<td>0.2797</td>
<td>0.1875</td>
<td>0.9102</td>
<td>0.7173</td>
</tr>
<tr>
<td>Baseline (enhanced)</td>
<td>ml-latest-small</td>
<td>val</td>
<td>0.1053</td>
<td>0.2125</td>
<td>0.2581</td>
<td>0.2077</td>
<td>0.9265</td>
<td>0.7279</td>
</tr>
</tbody>
</table>

### ALS Model
We tried the following hypermeters:
regularizationParams = [.01, .05, .1, .2]
latentRanks = [10, 50, 100, 150]
|data |map@K |precision@K|ndcg@K|recall@K|RMSE  |MAE   |
|-----|------|-----------|------|--------|------|------|
|small|0.0039|0.0454     |0.0413|0.0163  |0.9631|0.7525|
|large|0.0021|0.0338     |0.0253|0.0099  |0.861 |0.6797|



### LightFM

|Dataset|evalset|precision@K|auc   |recall@K|reciprocal rank|
|-------|-------|-----------|------|--------|---------------|
|small  |train  |0.3366     |0.9979|0.4642  |0.7111         |
|small  |test   |0.0448     |0.8943|0.2395  |0.1609         |
|large  |train  |0.3918     |0.9617|0.0616  |0.82           |
|large  |test   |0.0311     |0.8538|0.0311  |0.278          |

