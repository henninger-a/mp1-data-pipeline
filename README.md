# Description

This pipeline sets up logging, defines command line arguments, and validates, loads, and cleans data. The pipeline is organized with a package called src which contains the modules with functions used in the pipeline, pipeline.py which coordinates how the pipeline is run, fixtures with contains test data, config with contains the yaml configuration file, venv which sets up the virtual environment, and gitignore which determines which files are saved to git. When data is run through the pipeline first logging is set up and the input validated to make sure it exists, this is handled in the utils.py module. Next, the data is loaded according to whatever file type was inputted into the program, this is handled in the data_loaders.py module. Then the data is validated, making sure that required columns are present and that all numeric columns actually are, this is handled by the data_validator.py module. After this the data is processed, with duplicate, missing, and outlier values being dealt with as determined in the config file, this is handled by the data_processor.py module. Finally, a cleaning report is generated containing information about the data before and after, and the cleaned data is saved, which is handled by the data_output.py module.

# Example Command

```bash
$ python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

# Output

```text
12:10:55 INFO     src.utils — Input file validated: 'fixtures/sample_data.csv'
12:10:55 INFO     src.utils — Input file validated: 'config/config.yaml'
12:10:55 INFO     src.data_loaders — Loaded CSV file: fixtures\sample_data.csv (100 rows)
12:10:55 INFO     src.data_loaders — Loaded YAML file: config\config.yaml
12:10:55 WARNING  src.data_validator — Removed 2 row(s) from rating with invalid numerical values
12:10:55 DEBUG    src.data_validator — Valid Rows: 98, Rows Removed: 2
12:10:55 INFO     __main__ — Rows Before Validation: 100 Rows After Validation: 98
12:10:55 DEBUG    src.data_processor — Removed 2 duplicate row(s)
12:10:55 DEBUG    src.data_processor — Dropped 2 row(s) with missing values
12:10:55 DEBUG    src.data_processor — Method: iqr, Threshold: 1.5, Rows removed: 2
12:10:55 INFO     __main__ — Processing Complete: 100 → 92 rows
12:10:55 DEBUG    src.data_output — Rows Saved: 92, Output Path: None
12:10:55 INFO     __main__ — Saved cleaned data to output/clean.csv
Cleaning Report: {'rows_before': 100, 'rows_after': 92, 'rows_removed': 8, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}
```