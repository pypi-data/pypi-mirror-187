# topsis_rupanshi_102017010
TopsisPy is a Python Package implementing [Topsis](https://en.wikipedia.org/wiki/TOPSIS) method used for multi-criteria decision analysis.
Topsis stands for 'Technique for Order of Preference by Similarity to Ideal Solution'.

## Installation
Install the Package using the command - 
```s
$ pip install topsis_rupanshi_102017010
```
## Usage
```s
python -m topsis_rupanshijain_102017010.topsis102017010 <InputDataFile> <Weights> <Impacts> <ResultFileName>
```

## Example
|   Fund Name  |   P1    |   P2    |   P3   |   P4    |   P5     |
|--------------|---------|---------|--------|---------|----------|
|   M1         |   0.94  |   0.88  |   3.8  |   40.8  |   11.61  |
|   M2         |   0.77  |   0.59  |   5.6  |   45.4  |   13.09  |
|   M3         |   0.8   |   0.64  |   7    |   57.7  |   16.54  |
|   M4         |   0.67  |   0.45  |   3.1  |   61.6  |   16.46  |
|   M5         |   0.89  |   0.79  |   5.9  |   67.7  |   18.82  |
|   M6         |   0.66  |   0.44  |   6.2  |   62.1  |   17.35  |
|   M7         |   0.73  |   0.53  |   6.6  |   34.5  |   10.59  |
|   M8         |   0.91  |   0.83  |   3.2  |   55.3  |   15.06  |
weights : [1, 1, 1, 2, 1]
impacts : [+, +, -, +, +]

**input:** 102017010.csv
```s
python3 -m topsis_rupanshijain_102017010.topsis102017010 102017010.csv "1,1,1,2,1" "+,+,-,+,+" 102017010-result.csv
```

**output:** 102017010-result.csv
|   Fund Name  |   P1    |   P2    |   P3   |   P4    |   P5     |   Performance Score    |   Rank  |
|--------------|---------|---------|--------|---------|----------|------------------------|---------|
|   M1         |   0.94  |   0.88  |   3.8  |   40.8  |   11.61  |   0.47123375880088600  |   6     |
|   M2         |   0.77  |   0.59  |   5.6  |   45.4  |   13.09  |   0.33633254123378100  |   7     |
|   M3         |   0.8   |   0.64  |   7.0  |   57.7  |   16.54  |   0.5217872008890350   |   5     |
|   M4         |   0.67  |   0.45  |   3.1  |   61.6  |   16.46  |   0.6239838869195070   |   3     |
|   M5         |   0.89  |   0.79  |   5.9  |   67.7  |   18.82  |   0.7322985618518600   |   1     |
|   M6         |   0.66  |   0.44  |   6.2  |   62.1  |   17.35  |   0.5354177643750590   |   4     |
|   M7         |   0.73  |   0.53  |   6.6  |   34.5  |   10.59  |   0.09985769514278550  |   8     |
|   M8         |   0.91  |   0.83  |   3.2  |   55.3  |   15.06  |   0.706943829440074    |   2     |

## Other notes
- The first column and first row are removed by the library before processing, in attempt to remove indices and headers. So make sure the csv follows the format as shown in sample.csv.
- Make sure the csv does not contain categorical values

## License

MIT

**Free Software, Hell Yeah!**