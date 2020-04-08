[![Build Status](https://travis-ci.com/etimoz/vanity-cosmos.svg?branch=master)](https://travis-ci.com/github/etimoz/vanity-cosmos)
[![codecov.io](https://codecov.io/gh/etimoz/vanity-cosmos/branch/master/graph/badge.svg)](https://codecov.io/gh/etimoz/vanity-cosmos)
# vanity-cosmos

> CLI tool for creating [Cosmos](https://cosmos.network) vanity addresses

## Features
* Generate Cosmos bech32 vanity addresses
* Specify a substring that the addresses must
    * start with
    * end with
    * contains
* Set minimum amount of letters (a-z) or digits (0-9) required in an address
* Set the number of addresses to generate
* Uses all CPU cores

## How to use

Look for an address that starts with "00000" (e.g. cosmos100000v3fpv4qg2a9ea6sj70gykxpt63wgjen2p)
```
python -m vanitycosmos --startswith 00000
```

Look for an address that ends with "8888" (e.g. cosmos134dck5uddzjure8pyprmmqat96k3jlypn28888)
```
python -m vanitycosmos --endswith 8888
```

Look for an address containing the substring "mystring" (e.g. cosmos1z39wmystringah22s5a3pyswtnjkx2w0hvn3rv)
```
python -m vanitycosmos --contains mystring
```

Look for an address consisting of letters only (e.g. cosmos1rfqkejeaxlxwtjxucnrathlzgnvgcgldzmuxxe)
```
python -m vanitycosmos --letters 38
```

Look for an address with at least 26 digits (e.g. cosmos1r573c4086585u084926726x535y3k2ktxpr88l)
```
python -m vanitycosmos --digits 26
```

Generate 5 addresses (the default is 1)
```
python -m vanitycosmos --n 5
```

Combine flags introduced above
```
python -m vanitycosmos --startswith 00000 --endswith 8888 --n 5
```
