# TOPSIS Package in Python

Submitted by: Kartik Madan

Roll no: 102003565

---

## TOPSIS

TOPSIS is an acronym that stands for Technique of Order Preference Similarity to the Ideal Solution and is a pretty straightforward MCDA method. As the name implies, the method is based on finding an ideal and an anti-ideal solution and comparing the distance of each one of the alternatives to those.

---

## How to use

The package topsis-kartik-102003565 can be run though the command line as follows:

```
>> pip install topsis-kartik-102003565
```

```
>>python topsis data.csv "1,1,1,1" "+,+,-,+" result
```

## Sample Input

The decision matrix should be constructed with each row representing a Model alternative, and each column representing a criterion like Accuracy, R2, Root Mean Squared Error, Correlation, and many more.

<table><thead><tr><th>Fund Name</th><th>P1</th><th>P2</th><th>P3</th><th>P4</th></tr></thead><tbody><tr><td>M1</td><td>250</td><td>16</td><td>12</td><td>5</td></tr><tr><td>M2</td><td>200</td><td>16</td><td>8</td><td>3</td></tr><tr><td>M3</td><td>300</td><td>32</td><td>16</td><td>4</td></tr><tr><td>M4</td><td>275</td><td>32</td><td>8</td><td>4</td></tr><tr><td>M5</td><td>225</td><td>16</td><td>16</td><td>2</td></tr></tbody></table>

<br>
Weights `weights` is not already normalised will be normalised later in the code.

Information of benefit positive(+) or negative(-) impact criteria should be provided in `impacts`.
<br>

## Sample Output

The output that generated from the following input will be:

<table><thead><tr><th>Model</th><th align="right">P1</th><th align="center">P2</th><th>P3</th><th>P4</th><th>Topsis Score</th><th>Rank</th></tr></thead><tbody><tr><td>M1</td><td align="right">250</td><td align="center">16</td><td>12</td><td>5</td><td>0.534277</td><td>3</td></tr><tr><td>M2</td><td align="right">200</td><td align="center">16</td><td>8</td><td>3</td><td>0.308368</td><td>5</td></tr><tr><td>M3</td><td align="right">300</td><td align="center">32</td><td>16</td><td>4</td><td>0.691632</td><td>1</td></tr><tr><td>M4</td><td align="right">275</td><td align="center">32</td><td>8</td><td>4</td><td>0.534737</td><td>2</td></tr><tr><td>M5</td><td align="right">225</td><td align="center">16</td><td>16</td><td>2</td><td>0.401046</td><td>4</td></tr></tbody></table>

<br>
The output file contains columns of input file along with two additional columns having **Topsis_score** and **Rank** .
Here the ranks are given as rank 1 is the best solution according to the weights and impacts given and rank 5 is the worst solution.

---
