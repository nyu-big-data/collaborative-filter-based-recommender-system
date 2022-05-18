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

<table>
<tbody>
<tr>
<th>Dataset</th>
<th>EvaluationSet</th>
<th>meanAveragePrecisionAtK</th>
<th>precisionAtK</th>
<th>ndcgAtK</th>
<th>recallAtK</th>
<th>RMSE</th>
<th>MAP</th>
<th>Hyperparameters</th>
</tr>
<tr>
<td>ml-latest-small</td>
<td>val</td>
<td>0.9867</td>
<td>0.8409</td>
<td>0.9916</td>
<td>0.6361</td>
<td>0.8703</td>
<td>0.9629</td>
<td>Rank: 50  RegParam: 0.1 </td>
</tr>
<tr>
<td>ml-latest</td>
<td>val</td>
<td>0.99845</td>
<td>0.65197</td>
<td>0.99906</td>
<td>0.76604</td>
<td>0.7313</td>
<td>0.9896</td>
<td>Rank: 150  RegParam: 0.05 </td>
</tr>
</tbody>
</table>


### LightFM

| Dataset         | Metric Name     | EvaluationSet   |     Value |
|:----------------|:----------------|:----------------|----------:|
| ml-latest-small | precision_at_k  | train           | 0.497377  |
| ml-latest-small | precision_at_k  | test            | 0.0586885 |
| ml-latest-small | auc_score       | train           | 0.997965  |
| ml-latest-small | auc_score       | test            | 0.894303  |
| ml-latest-small | recall_at_k     | train           | 0.090199  |
| ml-latest-small | recall_at_k     | test            | 0.0387905 |
| ml-latest-small | reciprocal_rank | train           | 0.711089  |
| ml-latest-small | reciprocal_rank | test            | 0.160884  |
| ml-latest       | precision_at_k  | train           | 0.497377  |
| ml-latest       | precision_at_k  | test            | 0.0586885 |
| ml-latest       | auc_score       | train           | 0.997965  |
| ml-latest       | auc_score       | test            | 0.894303  |
| ml-latest       | recall_at_k     | train           | 0.090199  |
| ml-latest       | recall_at_k     | test            | 0.0387905 |
| ml-latest       | reciprocal_rank | train           | 0.711089  |
| ml-latest       | reciprocal_rank | test            | 0.160884  |
