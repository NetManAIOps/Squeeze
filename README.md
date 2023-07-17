# Squeeze
Implementation and datasets for ISSRE 2019 REG paper 'Generic and Robust Localization of Multi-Dimensional Root Cause'.

## Requirements
At least `python>=3.6, <3.7` is required. Though Python should be backward-compatible, there is no built wheel for some requirements like SciPy for a higher Python version.
``` bash
pip install -r requirements.txt
```

## Datasets

Datasets `A, B0, B1, B2, B3, B4, D` in Table VII are on [Zenodo](https://zenodo.org/record/8153367) (updated on 2023-07-17).
The ground truth root cause sets are in `injection_info.csv` in each subfolder.

## Usage

```
$python run_algorithm.py --help
Usage: run_algorithm.py [OPTIONS]

  :param name: :param input_path: :param output_path: :param num_workers:
  :param kwargs: :return:

Options:
  --name TEXT            name of this setting
  --input-path TEXT      will read data from {input_path}/{name}
  --output-path TEXT     if {output_path} is a dir, save to
                         {output_path}/{name}.json; otherwise save to
                         {output_path}
  --num-workers INTEGER  num of processes
  --derived              means we should read {timestamp}.a.csv and
                         {timestamp}.b.csv
  --help                 Show this message and exit.
```

``` 
$python run_evaluation.py --help
Usage: run_evaluation.py [OPTIONS]

Options:
  -i, --injection-info TEXT  injection_info.csv file
  -p, --predict TEXT         output json file
  -c, --config TEXT          config json file
  -o, --output-path TEXT     output path
  --help                     Show this message and exit.
```

The config json file should contain the attribute names, e.g.:

```
{
  "columns": [
    "a", "b", "c", "d"
  ]
}
```



## Example

1.  Download `B3.tgz` and extract `B3.tgz` into `B3`.

2.  Run this command:

```
python run_algorithm.py --name B_cuboid_layer_2_n_ele_2 --input-path B3 --output-path output/ --num-workers 10
```

​	Then the results are summarized in `output/B_cuboid_layer_2_n_ele_2.json`:

```json
[
    {
        "timestamp": 1450653900,
        "elapsed_time": 10.794443607330322,
        "root_cause": "b=b31&d=d2;a=a1&b=b11"
    },
    {
        "timestamp": 1450666800,
        "elapsed_time": 15.272005081176758,
        "root_cause": "b=b21&c=c1;a=a4&b=b9&c=c4"
    },
    {
        "timestamp": 1450667700,
        "elapsed_time": 15.22673487663269,
        "root_cause": "b=b11&c=c4;a=a2&d=d1"
    },
    ...
]
```

3.  Run evaluation scripts

``` bash
python run_evaluation.py -i B3/B_cuboid_layer_2_n_ele_2/injection_info.csv -p output/B_cuboid_layer_2_n_ele_2.json -c columns.json
```

`columns.json` should contain all the attributes.

```
{
  "columns": [
    "a", "b", "c", "d"
  ]
}
```

Then we get the output (F1-score, precision, recall):

```
......
0.7858942065491183 0.7918781725888325 0.78
```

## Known Issues
This version of codes is faithful to the published version.
However, two known severe issues are harming the localization performance.
1. The calculation of `_a1` and `_a2` in `squeeze/squeeze.py:184` is incorrect, which is not following the description in the paper.
   It should be corrected as follows
   ``` python
    reduced_data_p, _ = self.get_derived_dataframe(
        frozenset(elements[:partition]), cuboid=cuboid,
        reduction="sum", return_complement=True,
        subset_indices=np.concatenate([indices, self.normal_indices]))
    if len(reduced_data_p):
        _a1, _a2 = data_p.predict.values * (
                reduced_data_p.real.item() / reduced_data_p.predict.item()
        ), data_n.predict.values
    else:
        # print(elements[:partition], data_p, reduced_data_p)
        assert len(data_p) == 0
        _a1 = 0
        _a2 = data_n.predict.values   
   ```
2. The calculation of `score_weight` in `squeeze/suqeeze.py:256` may produce negative values, which will cause incorrect localization results. Different from 1, the calculation here is faithful to the paper. See https://github.com/NetManAIOps/Squeeze/issues/6

See also our [extended version](https://github.com/netmanaiops/psqueeze)

## Citation

```
@inproceedings{squeeze,
  title={Generic and Robust Localization of Multi-Dimensional Root Causes},
  author={Li, Zeyan and Luo, Chengyang and Zhao, Yiwei and Sun, Yongqian and Sui, Kaixin and Wang, Xiping and Liu, Dapeng and Jin, Xing and Wang, Qi and Pei, Dan},
  booktitle={2019 IEEE 30th International Symposium on Software Reliability Engineering (ISSRE)},
  year={2019},
  organization={IEEE}
}
```
