import click
import pandas as pd
import json
from utility import AttributeCombination as AC
import numpy as np


@click.command()
@click.option("--injection-info", '-i', help='injection_info.csv file')
@click.option("--predict", '-p', help='output json file')
@click.option("--config", '-c', help='config json file')
@click.option("--output-path", '-o', help="output path", default="./output.csv")
def main(*args, **kwargs):
    evaluate(*args, **kwargs)


def evaluate(injection_info, predict, config, output_path, verbose=True, return_detail=False):
    injection_info = pd.read_csv(injection_info)
    with open(predict, 'r') as f:
        predict = json.load(f)
    with open(config, 'r') as f:
        config = json.load(f)
    injection_info.set_index(['timestamp'], inplace=True)
    for idx, item in enumerate(predict):
        try:
            label = predict[idx]['label'] = AC.batch_from_string(
                injection_info.loc(axis=0)[int(item['timestamp']), 'set'],
                attribute_names=config['columns']
            )
            try:
                ret = AC.batch_from_string(
                    item['root_cause'].replace('|', ';'),
                    attribute_names=config['columns']
                )
                pred = predict[idx]['pred'] = ret
            except Exception as e:
                print(item, e)
                continue
            _fn = len(label)
            _tp, _fp = 0, 0
            for rc_item in pred:
                if rc_item in label:
                    _fn -= 1
                    _tp += 1
                else:
                    _fp += 1
        except KeyError:
            continue
        predict[idx]['tp'] = _tp
        predict[idx]['fp'] = _fp
        predict[idx]['fn'] = _fn
        predict[idx]['cuboid_layer'] = len(list(label)[0].non_any_values)
        predict[idx]['num_elements'] = len(label)
        predict[idx]['significance'] = injection_info.loc(axis=0)[int(item['timestamp']), 'significance']
        if verbose:
            print("========================================")
            print(f"timestamp:{item['timestamp']}")
            print(f"label:{AC.batch_to_string(label)}")
            print(f"pred :{AC.batch_to_string(pred)}")
            print(f"tp: {_tp}, fp: {_fp}, fn: {_fn}")
        del predict[idx]['root_cause']
    df = pd.DataFrame.from_records(predict)
    total_fscore = 2 * np.sum(df.tp) / (2 * np.sum(df.tp) + np.sum(df.fp) + np.sum(df.fn))
    total_precision = np.sum(df.tp) / (np.sum(df.tp) + np.sum(df.fp))
    total_recall = np.sum(df.tp) / (np.sum(df.tp) + np.sum(df.fn))
    df_total = pd.DataFrame.from_dict(
        {"tp": [np.sum(df.tp)],
         "fp": [np.sum(df.fp)],
         "fn": [np.sum(df.fn)],
         "F1-Score": [total_fscore],
         "Precision": [total_precision],
         "Recall": [total_recall],
         'Time Cost (s)': [np.mean(df['elapsed_time'])],
         'time_std': [np.std(df['elapsed_time'])],
         'Total Time Cost (s)': [np.sum(df['elapsed_time'])],
         'length': len(predict),
         # 'time_list': df['elapsed_time'].values,
         }
    )
    if verbose:
        print(df_total)
    if output_path is not None:
        df_total.to_csv(output_path, index=False)
    if verbose:
        print(total_fscore, total_precision, total_recall)
    if return_detail:
        return df
    return df_total


if __name__ == '__main__':
    main()


