#!/usr/bin/python3
from Crypto.PublicKey.RSA import construct
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import optparse
import base64
import gmpy
import re

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

DEFAULT_EXP = 65537

if __name__ == '__main__':
    
    parser = optparse.OptionParser()

    parser.add_option('-p', dest='p', help='prime', type='int')
    parser.add_option('-q', dest='q', help='prime', type='int')
    parser.add_option('-n', dest='n', help='modulus', type='int')
    parser.add_option('-d', dest='d', help='private exponent', type='int')
    parser.add_option('-e', dest='e', help='public exponent (default: %d)' % DEFAULT_EXP, type='int', default=DEFAULT_EXP)
    parser.add_option('-o', dest='filename', help='output filename')
    parser.add_option('-f', dest='format', help='output format (DER, PEM) (default: PEM)', type='choice', choices=['DER', 'PEM'], default='PEM')
    parser.add_option('-v', dest='verbose', help='also display CRT-RSA representation', action='store_true', default=False)

    try:
        (options, args) = parser.parse_args()
        privkey=None
        if options.p and options.q:
            if not gmpy.is_prime(options.p) or not gmpy.is_prime(options.q):
                raise ValueError("Supplied p and or supplied q is not a prime number!")
            print('Using (p, q) to initialise RSA instance\n')
            n = options.p * options.q
            if options.p != options.q:
                phi = (options.p - 1) * (options.q - 1)
            else:
                phi = (options.p ** 2) - options.p
            d = modinv(options.e, phi)
            privkey = construct((n, options.e, d))
        elif options.n and options.d:
            print('Using (n, d) to initialise RSA instance\n')
            privkey = construct((options.n, options.e, options.d))
        else:
            parser.print_help()
            parser.error('Either (p, q) or (n, d) needs to be specified')

        if privkey:
            print(f"n = {privkey.n}")
            print(f"e = {privkey.e}")
            print(f"d = {privkey.d}")
            print(f"p = {privkey.p}")
            print(f"q = {privkey.q}")
            keystring = privkey.exportKey()
            if options.format == 'DER':
                pemkey = serialization.load_pem_private_key(
                    keystring,
                    None,
                    default_backend()
                )
                derkey = pemkey.private_bytes(
                    serialization.Encoding.DER,
                    serialization.PrivateFormat.TraditionalOpenSSL,
                    serialization.NoEncryption()
                )
                keystring = derkey
            if options.filename:
                print(f"Saving key in {options.format} format to file {options.filename}.")
                tf = open(options.filename, 'wb')
                tf.write(keystring)
                tf.close()


    except optparse.OptionValueError as e:
        parser.print_help()
        parser.error(e.msg)
