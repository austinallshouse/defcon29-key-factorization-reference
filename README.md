# Reference Implementation of Distributable RSA Factorization

This is a reference implementation accompanying the DEF CON 29 talk: [The mechanics of compromising low entropy RSA keys](https://defcon.org/html/defcon-29/dc-29-speakers.html#allshouse).

The algorithm is based on that described in [Weak Keys Remain Widespread in Network Devices](https://www.cis.upenn.edu/~nadiah/papers/weak-keys/weak-keys.pdf).

The `data/` directory contains 2500 distinct RSA moduli distributed among 5 files.  6 of the moduli are factorable due the presence of a shared factor in a separate batch.

```bash
python3 multi_batch_gcd.py data/batch_1.txt data/batch_2.txt data/batch_3.txt data/batch_4.txt data/batch_5.txt > answers.txt
```

The code is provided for illustrative purposes and will not be performant for real-world applications.
