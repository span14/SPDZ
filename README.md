# SPDZ

Really simple and coarse SPDZ simulation implementation. It supports `+/-/*/()` operation only. 

## Setup
Create a mathemetical equation in `expression.conf` file like `(x1+y1)+10-x2*y2`. Then specify variable value in both `party_x.json` and `party_y.json` files

## Run
`python spdz_2party.py`

## Description
This is a really simple implementation of SPDZ. It relys on the additive secret sharing scheme and the beaver triple to complete the above mathematical operations. 