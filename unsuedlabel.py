import argparse
import os
import pathlib
import re


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def in_which_file(main_path, label):
    for path in pathlib.Path(main_path).rglob('*.tex'):
        with open(path, 'r') as f:
            text = "".join(f.readlines())
        if re.search('label{' + label + '}', text):
            return os.path.basename(path)


def creates_list_of_labels(text):
    match = re.finditer("[ *][^%].*label{([0-9a-zA-Z_|:]*)}", text)
    tmp = [x.group(1) for x in match]
    return filter(lambda y: y.lstrip()[0] != "%", tmp)


def is_used(text, label):
    match = re.search("[^label|.]{"+label+"}", text)
    return match is not None


def create_totale_tex(path):
    if os.path.isdir(path):
        text = ""
        for path in pathlib.Path(path).rglob('*.tex'):
            with open(path, 'r') as f:
                text += "".join(f.readlines())
        return text
    else:
        raise Exception("NotADirectoryError")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', metavar='main-directory', type=dir_path, required=True)
    args = parser.parse_args()

    text = create_totale_tex(args.d)
    labels = creates_list_of_labels(text)
    for ll in labels:
        if not is_used(text, ll):
            path = in_which_file(args.d, ll)
            print("label {} defined in {} is not used!".format(ll, path))
