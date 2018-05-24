# guess_pairs.py 
A BIP39 Seed Bruteforce script for cryptogreetings puzzle

### Dependencies
```
sudo apt-get install python3 python3-pip protobuf-compiler
pip3 install ecdsa pyaes pbkdf2 requests qrcode
```
### To install electrum use:
```
git clone https://github.com/spesmilo/electrum.git
cd electrum
python3 setup.py install 
```
## OR 

```
git clone https://github.com/spesmilo/electrum.git
cd electrum
pip3 install .[full]
```

### Enter your selection of BIP39 words into SEED_ARRAY
```
SEED_ARRAY=["agree", "air", "cash", "define", "else", "end", "find", "gap", "just", "law", "must", "now", "old", "online", "order", "pool", "post", "problem", "proof", "rely", "risk", "run", "sign", "stay", "trust", "try", "zero"]
```

### Enter any known pairs into KNOWN_PAIR_ARRAY
```
KNOWN_PAIR_ARRAY=["code easily", "attack early", "almost open"]
```

Original Script Credit: https://gist.github.com/kenprice/1a3c5009f5fdd8c801bba6620b779307

## Donations: 1KbuagPbX9bRDzvRCky58L8jVRbj9mnR92
