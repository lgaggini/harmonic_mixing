# harmonic_mixing

harmonic_mixing is a Python tool/package to find harmonic sequences/mixes in a list of alphanumeric musical keys, based on [Camelot Wheel system](https://mixedinkey.com/camelot-wheel/) and [Dj Studio Compatible Keys](https://dj.studio/blog/compatible-keys)

## Features
* CLI: read alphanumeric keys list directly from command-line
* Filtering by sequence: get only mixes which contain a specific sequence (eg. get only mixes which contain the 7A->8A->8B sequence)
* Filtering by safe transitions by default: get only mixes which contain safe transitions (same key, +1/-1 step) (if at least one is available)
* Sorting: sort found mixes
* Gap mode: allow a non harmonic gap in the found mixes which could be filled as you wish or could be leaved empty

## Install

### Git
```
git clone https://github.com/lgaggini/harmonic_mixing
pip install -r requirements.txt
```

## Usage
```
> python harmonic_mixing.py -h
usage: harmonic_mixing.py [-h] -k KEYS [-f FILTER] [-a] [-u] [-g] [-l {debug,info,warning,error,critical}]

harmonic_mixing, find harmonic mixes

options:
  -h, --help            show this help message and exit
  -k KEYS, --keys KEYS  comma splitted list of keys to be mixed
  -f FILTER, --filter FILTER
                        filter to get mixes with selected keys sequence
  -a, --all             no priority to safer mixes (default disabled)
  -u, --unsort          unsort mixes (default disabled)
  -g, --gaps            enables mix with gaps (default disabled)
  -l {debug,info,warning,error,critical}, --log-level {debug,info,warning,error,critical}
                        log level (default info)

```

### Examples

#### Safe mixes
```
python harmonic_mixing.py -k 4A,3A,2A,1A
2026-03-24 09:14:00 thule harmonic_mixing[126594] INFO finding mixes starting with 4A
2026-03-24 09:14:00 thule harmonic_mixing[126594] INFO finding mixes starting with 3A
2026-03-24 09:14:00 thule harmonic_mixing[126594] INFO finding mixes starting with 2A
2026-03-24 09:14:00 thule harmonic_mixing[126594] INFO finding mixes starting with 1A
2026-03-24 09:14:00 thule harmonic_mixing[126594] INFO [1A, 2A, 3A, 4A]
2026-03-24 09:14:00 thule harmonic_mixing[126594] INFO [2A, 1A, 3A, 4A]
2026-03-24 09:14:00 thule harmonic_mixing[126594] INFO [4A, 3A, 2A, 1A]
2026-03-24 09:14:00 thule harmonic_mixing[126594] INFO found 3/3 filtered valid mixes
```

#### Safe mixes filtered by 1A->2A sequence
```
python harmonic_mixing.py -k 4A,3A,2A,1A -f 1A,2A
2026-03-24 09:15:28 thule harmonic_mixing[127967] INFO finding mixes starting with 4A
2026-03-24 09:15:28 thule harmonic_mixing[127967] INFO finding mixes starting with 3A
2026-03-24 09:15:28 thule harmonic_mixing[127967] INFO finding mixes starting with 2A
2026-03-24 09:15:28 thule harmonic_mixing[127967] INFO finding mixes starting with 1A
2026-03-24 09:15:28 thule harmonic_mixing[127967] INFO filtering for [1A, 2A]
2026-03-24 09:15:28 thule harmonic_mixing[127967] INFO [1A, 2A, 3A, 4A]
2026-03-24 09:15:28 thule harmonic_mixing[127967] INFO found 1/3 filtered valid mixes
```

#### All mixes filtered by 1A->2A sequence
```
python harmonic_mixing.py -k 4A,3A,2A,1A -f 1A,2A -a
2026-03-24 09:16:48 thule harmonic_mixing[129203] INFO finding mixes starting with 4A
2026-03-24 09:16:48 thule harmonic_mixing[129203] INFO finding mixes starting with 3A
2026-03-24 09:16:48 thule harmonic_mixing[129203] INFO finding mixes starting with 2A
2026-03-24 09:16:48 thule harmonic_mixing[129203] INFO finding mixes starting with 1A
2026-03-24 09:16:48 thule harmonic_mixing[129203] INFO filtering for [1A, 2A]
2026-03-24 09:16:48 thule harmonic_mixing[129203] INFO [1A, 2A, 3A, 4A]
2026-03-24 09:16:48 thule harmonic_mixing[129203] INFO [1A, 2A, 4A, 3A]
2026-03-24 09:16:48 thule harmonic_mixing[129203] INFO found 2/5 filtered valid mixes
```

#### Safe Mixes with gaps
```
python harmonic_mixing.py -k 4A,3A,2A,1A -g
2026-03-24 09:18:27 thule harmonic_mixing[130909] INFO finding mixes starting with 4A
2026-03-24 09:18:27 thule harmonic_mixing[130909] INFO finding mixes starting with 3A
2026-03-24 09:18:27 thule harmonic_mixing[130909] INFO finding mixes starting with 2A
2026-03-24 09:18:27 thule harmonic_mixing[130909] INFO finding mixes starting with 1A
2026-03-24 09:18:27 thule harmonic_mixing[130909] INFO [1A, 2A, 3A, 4A]
2026-03-24 09:18:27 thule harmonic_mixing[130909] INFO [2A, 1A, 3A, 4A]
2026-03-24 09:18:27 thule harmonic_mixing[130909] INFO [2A, 3A, 4A, 'gap', 1A]
2026-03-24 09:18:27 thule harmonic_mixing[130909] INFO [2A, 3A, 4A, 'gap', 1A]
2026-03-24 09:18:27 thule harmonic_mixing[130909] INFO [3A, 2A, 1A, 'gap', 4A]
2026-03-24 09:18:27 thule harmonic_mixing[130909] INFO [3A, 2A, 1A, 'gap', 4A]
2026-03-24 09:18:27 thule harmonic_mixing[130909] INFO [3A, 4A, 'gap', 2A, 1A]
2026-03-24 09:18:27 thule harmonic_mixing[130909] INFO [3A, 4A, 'gap', 2A, 1A]
2026-03-24 09:18:27 thule harmonic_mixing[130909] INFO [4A, 3A, 2A, 1A]
2026-03-24 09:18:27 thule harmonic_mixing[130909] INFO found 9/9 filtered valid mixes
```
