# WMF Fraud Pipeline

A very hacky but working implementation of data extraction, data pre-processing and model training pipeline for WMF fraud detection.

## Requirements
* Python 2.7
* Pip
* Libraries as described in requirements.txt. Strongly recommended that you use a virtualenv before doing pip install.

## Pipeline Steps - Importing a fresh/updated version of the model into the API
* We need to obtain 2 kinds of data for the classifier to work correctly - fraudulent and genuine.
* On `frdev`, run the queries given in the `data-extraction` folder using the following -
	1. Run `$ mysql < fraud-query.sql | sed "s/'/\'/;s/\t/\",\"/g;s/^/\"/;s/$/\"/;s/\n//g" > ../data/fraud-data.csv`
	2. Get the number of fraud rows returned by the command `$ wc -l ../data/fraud-data.csv`
	3. Open `genuine-query.sql` in a text editor, replace "$num" in the last line (limit clause) with the number of fraud rows.
	4. Save the file and now run `$ mysql < genuine-query.sql | sed "s/'/\'/;s/\t/\",\"/g;s/^/\"/;s/$/\"/;s/\n//g" > ../data/genuine-data.csv`
	5. Shift to the data folder, `$ cd ../data`
	6. Concatenate the 2 data files using - `$ cat fraud-data.csv < (tail -n+2 genuine-data.csv) > orig-data.csv`

* Once we have the combined data file, we need to pre-process it . Run `$ python feature-eng.py` This should generate a file called `data-eng.csv`.

* Nagivate to the model-training folder - `$ cd ../model-training`. Run `$ python model-train-gb.py`.

* Copy the contents of the private folder to the private folder in the API. Our new model is loaded!

## Running the API
* The steps are covered in the API README - https://github.com/saurabhbatra96/wmf-fd-api/blob/master/README.md#installation-and-usage

## Research and Findings