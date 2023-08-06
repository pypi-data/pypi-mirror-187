# GRL Merger
This is a package used to merge two GRL models into one consolidated GRL model. The GRL models have to be written in a textual-GRL form (TGRL).

## Installation

Run the following to install:

```python
pip install GRLMerger
```


## Usage

```python
from grlmerger import startGRLMerger

# The input files must be in the same directory
startGRLMerger('model_1.xgrl', 'model_2.xgrl')

# It generates the input models in xlsx format, merged model in xgrl format, and conflict cases in xlsx format.

# To print the conflict cases dataframe
print(trace_conflict_df)

# To print the merged model dataframe
print(merged_model_df)

# To print the merged actors dataframe
print(merged_actors_df)

# To print the merged links dataframe
print(merged_relations_df)

```
