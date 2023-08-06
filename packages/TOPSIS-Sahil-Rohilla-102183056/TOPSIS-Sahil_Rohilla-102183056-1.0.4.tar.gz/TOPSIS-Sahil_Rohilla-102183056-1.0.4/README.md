**TOPSIS_102183056**

TOPSIS method for multiple-criteria decision making (MCDM)

**What is TOPSIS?**

Technique for Order Preference by Similarity to Ideal Solution (TOPSIS) originated in the 1980s as a multi-criteria decision making method. TOPSIS chooses the alternative of shortest Euclidean distance from the ideal solution, and greatest distance from the negative-ideal solution.


## 🔗 Usage
topsis data.csv "1,1,1,1" "+,+,-,+" result.csv

## 🔗 Input File(data.csv)

Model	Correlation	R2	RMSE	Accuracy

M1	0.79	0.62	1.25	60.89

M2	0.66	0.44	2.89	63.07

M3	0.56	0.31	1.57	62.87

M4	0.82	0.67	2.68	70.19

M5	0.75	0.56	1.3	80.39

## 🔗 Output File(result.csv)

Model	Correlation	R2	RMSE	Accuracy	Topsis_score	Rank

M1	0.79	0.62	1.25	60.89	0.7722	2

M2	0.66	0.44	2.89	63.07	0.2255	5

M3	0.56	0.31	1.57	62.87	0.4388	4

M4	0.82	0.67	2.68	70.19	0.5238	3

M5	0.75	0.56	1.3	80.39	0.8113	1
