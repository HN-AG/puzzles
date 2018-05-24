# BIP39 Seed Bruteforce (Python 3).

## guess_pairs.py 
- Pairs up BIP39 words allowing for known pairs to be added randomly into every seed attempt.
- Balance checking using Electrum servers

## guess_seeds.py 
- Randomly creates a 24 words seed using the chosen array of BIP39 words
- Balance checking using Electrum servers

### Quick Start
```
sudo apt-get install git python3 python3-pip protobuf-compiler -y
pip3 install ecdsa pyaes pbkdf2 requests qrcode
git clone https://github.com/spesmilo/electrum.git
cd electrum
python3 setup.py install 
cd ..
git clone https://github.com/HN-AG/puzzles
cd puzzles/
python3 guess_pairs.py
```

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
### OR 

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
