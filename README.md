# Squeeze
Implementation and datasets for ISSRE 2019 REG paper 'Generic and Robust Localization of Multi-Dimensional Root Cause'.

## Requirements

1.  Install `pipenv`

    I use [pipenv](https://github.com/pypa/pipenv) to manage the requirements.

    If you're on MacOS, you can install Pipenv easily with Homebrew:

    ```
    $ brew install pipenv
    ```

    Or, if you're using Debian Buster+:

    ```
    $ sudo apt install pipenv
    ```
    
    Otherwise, refer to the [documentation](https://docs.pipenv.org/en/latest/install/#installing-pipenv) for instructions.

2.  Sync the environments.

    ``` bash
    pipenv sync
    ```

3.  Activate the virtualenv

    ``` bash
    pipenv shell
    ```



For those prefer `pip`,  `pipenv` supports exporting requirements into a `requirements.txt` for `pip`.

## Datasets

Datasets `A, B0, B1, B2, B3, B4, D` in Table VII are on [Tsinghua Cloud](https://cloud.tsinghua.edu.cn/d/6e1e5adebe6a4a3cbd66/).
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

## Example

An example data is placed in `data/` ( sampled from `B0/B_cuboid_layer_1_n_ele_1`).

Run this command:

```
python run_algorithm.py --name B_cuboid_layer_1_n_ele_1 --input-path data --output-path output/
```

Then the results are summarized in `output/B_cuboid_layer_1_n_ele_1.json`:

```json
[
    {
        "timestamp": 1451019300,
        "elapsed_time": 4.80116605758667,
        "root_cause": "logstream_isp=ALIBABA"
    }
]
```



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