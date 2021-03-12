import os
import csv
import pandas as pd
import json
from pydash import py_ as _
import glob
import shutil
import re
from pprint import pprint

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRIMARY_FILE = 'en.json'
EXCEL_FILE = 'translation_origin.xlsx'


def _get_full_path():
    full_paths = []
    files_in_path = sorted([file_name for file_name in os.listdir(BASE_DIR)
                            if re.match(r'^[a-z]{2}\.json$', file_name)])

    for file in files_in_path:
        path_single = os.path.join(BASE_DIR, file)
        full_paths.append(path_single)
    return full_paths


def _get_jsons(paths):
    full_json_vo = {}
    for path in paths:
        file_name = path[path.rfind('/')+1:]
        with open(path) as json_file:
            json_data = json.load(json_file)
            full_json_vo[file_name] = json_data
    return full_json_vo


def get_keys(obj, prev_key=None, keys=[]):
    if type(obj) != type({}):
        keys.append(prev_key)
        return keys
    new_keys = []
    for k, v in obj.items():
        if prev_key is not None:
            new_key = "{}.{}".format(prev_key, k)
        else:
            new_key = k
        new_keys.extend(get_keys(v, new_key, []))
    return new_keys


def _generate_original_csv(json_dt_list, all_keys: list):
    writer = pd.ExcelWriter(EXCEL_FILE, engine='xlsxwriter')
    df = pd.DataFrame({'path_key': all_keys,
                       'en': _get_value_from_jon(json_dt_list[0], all_keys),
                       'jp': _get_value_from_jon(json_dt_list[1], all_keys),
                       'ko': _get_value_from_jon(json_dt_list[2], all_keys)
                       })
    df.to_excel('./translation_origin.xlsx', sheet_name='origin_resource', index=False)


def _get_value_from_jon(json, keys):
    val_list = []
    for key in keys:
        val_list.append(_.get(json, key, ''))
    return val_list
#
# def _verify_keys_in_jsons(all_json_list:list):
#
#     for lang_json in all_json_list:
#         print(pass)


def _verify_json_into(json_data):
    primary_all_keys = {}

    try:
        if PRIMARY_FILE in json_data and primary_all_keys == {}:
            en_key = json_data.get(PRIMARY_FILE)
            primary_all_keys[PRIMARY_FILE] = [*get_keys(en_key)]

        for key in json_data:
            if key != PRIMARY_FILE:
                single_lang = [*get_keys(key)]
                if (primary_all_keys[PRIMARY_FILE] == single_lang).all():
                    pass
                else:
                    list(set(primary_all_keys[PRIMARY_FILE]) - set(single_lang))




    except Exception as e:
        raise e



def main():
    paths = _get_full_path()
    json_data_vo = _get_jsons(paths)
    pprint(json_data_vo)
    # get_all_keys = [*get_keys(json_data_list[0])]
    # _generate_original_csv(json_data_list, get_all_keys)


if __name__ == '__main__':
    main()
