"""
"""

import json

input_dirs = ["data/base-blind-eval",
              "data/v20-blind-eval",]

output_dir = "data/base-v20-blind-eval"

if __name__ == "__main__":
    result = dict()
    for dir in input_dirs:
        with open(dir + "/properties", "r") as infile:
            print(dir)
            d = json.load(infile)
            print(len(d))
            result = {**result, **d}

    print(len(result))

    with open(output_dir + "/properties", "w") as outfile:
        json.dump(result, outfile)
