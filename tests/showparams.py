import sys
import json

if __name__ == '__main__':
    with open(sys.argv[1], encoding='utf-8') as f:
        params = json.load(f)

    print('Params:')
    print(params)
