# rsatool3

## Description
python 3 script to recover / generate a RSA private key given the two prime numbers used (p, q) OR the modulus and private exponent used (n, d).

Original credits to the script author found here https://github.com/ius/rsatool

Problem I had with it was it was very old and used python2 so I made a more modern python 3 version. Also minor problem in it that required downgrading to `pyasn1==0.4.5`.

Anyways, this should fix those minor issues. 

**Tested on python 3.6, 3.7, and 3.8**

**Tested on Ubuntu 18.04 and 20.04**

Can output to PEM and DER formats.

## Requirements
I had to install:

```bash
sudo apt install libgmp3-dev
sudo python3 -m pip install gmpy
```

## Usage:

To output in PEM format given the two prime numbers used to create the RSA key (p, q):

`python3 rsatool3.py -f PEM -o key.pem -p 1230<REDACTED_FOR_SPACE>9521 -q 2921<REDACTED_FOR_SPACE>409`

To output in DER format given the modulus (n) and private exponent (d) used (both passed as decimal/integers):

`python3 rsatool3.py -f DER -o key.der -n 2372<REDACTED_FOR_SPACE>2089 -d 4326<REDACTED_FOR_SPACE>2433`
