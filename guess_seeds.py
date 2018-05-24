import random
from electrum import util, keystore, bitcoin, Network
import argparse
import sys
import threading
import os
import time
from time import sleep
from electrum.util import json_encode, print_msg
import json

n = Network()
n.start()

MAX_THREADS=25
TARGET_ADDR="37XTVuaWt1zyUPRgDDpsnoo5ioHk2Da6Fs"
# How many of the address indexes to try. Default to just /0.
# i.e. last digit in derivation path: m/49'/0'/0'/0/0
MAX_ADDR_IDX=1


# Array of BIP39 words to use
SEED_ARRAY=["ability", "able", "add", "agree", "air", "almost", "attack", "cash", "code", "coin", "come", "course", "define", "early", "easily", "else", "end", "entire", "fee", "find", "gap", "help", "issue", "just", "know", "law", "like", "main", "model", "modify", "must", "need", "network", "next", "now", "old", "one", "online", "open", "order", "paper", "place", "pool", "post", "power", "problem", "process", "proof", "provide", "race", "rely", "risk", "run", "sign", "since", "size", "speed", "split", "stay", "still", "system", "tail", "trust", "try", "use", "want", "way", "zero"]


def my_shuffle(array):
    random.shuffle(array)
    return array
    
    
def combinations(n, list, combos=[]):
    # initialize combos during the first pass through
    if combos is None:
        combos = []

    if len(list) == n:
        # when list has been dwindeled down to size n
        # check to see if the combo has already been found
        # if not, add it to our list
        if combos.count(list) == 0:
            combos.append(list)
            combos.sort()
        return combos
    else:
        # for each item in our list, make a recursive
        # call to find all possible combos of it and
        # the remaining items
        for i in range(len(list)):
            refined_list = list[:i] + list[i+1:]
            combos = combinations(n, refined_list, combos)
        return combos
        
def deriveAddresses(line, xprv, i):
    xprv2, _xpub = bitcoin.bip32_private_derivation(xprv, "", str(i))
    btc_addr = xpub2btc(_xpub)
    if (TARGET_ADDR.lower()):
        privkey = xprv2btc(xprv2)
        if (TARGET_ADDR.lower() == btc_addr.lower()):
            print("FOUND PUZZLE PRIZE: " + privkey)
            win = open("SOLVED.txt", "a")
            win.write("WINNING SEED: "+line + "\n")
            win.write("ADDRESS: "+btc_addr + "\n")
            win.write("PRIVKEY: "+privkey + "\n")

        BALANCE=0
        g = open("VALID.csv", "a")
        # Get balance from electrum network
        h = n.synchronous_get(('blockchain.address.get_balance',[btc_addr]))
        if (h['confirmed']+h['unconfirmed'] >= 1):
            # write to BALANCES.txt file if it has a balance - makes it easier to find
            bal = open("BALANCES.txt", "a")
            bal.write("SEED: "+line + "\n")
            bal.write("ADDRESS: "+btc_addr + "\n")
            bal.write("PRIVKEY: "+privkey + "\n")
            bal.write("BALANCE: "+str(h['confirmed']+h['unconfirmed'])+"sats\n")
        g.write(btc_addr+','+line+','+privkey+','+str(h['confirmed']+h['unconfirmed'])+'sats\n')
        g.close()
        
        print("[BALANCE] - "+btc_addr+" has "+str(h['confirmed']+h['unconfirmed'])+"BTC")
    sys.stdout.flush()

def checkPassphrase(line):
    passw = ""

    seed = util.bh2u(keystore.bip39_to_seed(line, passw))
    seed = util.bfh(seed)
    xprv, _xpub = bitcoin.bip32_root(seed, "standard")
    xprv, _xpub = bitcoin.bip32_private_derivation(xprv, "", "49'")
    xprv, _xpub = bitcoin.bip32_private_derivation(xprv, "", "0'")
    xprv, _xpub = bitcoin.bip32_private_derivation(xprv, "", "0'")
    xprv, _xpub = bitcoin.bip32_private_derivation(xprv, "", "0")
    for i in range(MAX_ADDR_IDX):
        deriveAddresses(line, xprv, i)

def xpub2btc(xpub):
    _xtype, _depth, _fp, _cn, _c, K = bitcoin.deserialize_xpub(xpub)
    return bitcoin.pubkey_to_address("p2wpkh-p2sh", util.bh2u(K))

def xprv2btc(xprv):
    _xtype, _depth, _fp, _cn, _c, k = bitcoin.deserialize_xprv(xprv)
    privkey = bitcoin.serialize_privkey(k, True, "p2wpkh-p2sh")
    return privkey

def main():
    SEED_COUNTER=0
    VALID_SEED_COUNT=0

    TOTAL_COUNTER=0
    SEED_START_TIME=time.time()
    while True:
        # GENERATE NEW SEED PHRASE
        word=""
        WORD_COUNT=0
        SEED_TO_TEST=''
        for suit in my_shuffle(SEED_ARRAY):
            if (WORD_COUNT <= 24): 
                word=word+" "+suit
                WORD_COUNT+= 1
            if (WORD_COUNT == 24): 
                line = word
                threads = []                
                SEED_COUNTER+=1
                if (SEED_COUNTER >= 1000):
                    TOTAL_COUNTER+=SEED_COUNTER
                    SEED_COUNTER=0
                    TIME_SINCE=time.time()-SEED_START_TIME
                    print("[BRUTEFORCE] Checked "+str(TOTAL_COUNTER)+" seeds and found "+str(VALID_SEED_COUNT)+" valid seeds in "+str(TIME_SINCE)+" seconds." )

         
                (checksum_ok, wordlist_ok) = keystore.bip39_is_checksum_valid(line)
                if not wordlist_ok:
                    print("       Unknown words!" + line, file=sys.stderr)
                    continue
                if not checksum_ok:
                    #print("       Checksum NOT OK!" + line, file=sys.stderr)
                    continue
                #print("       Check passed. Queued:  " + line)
                VALID_SEED_COUNT+=1

                t = threading.Thread(target=checkPassphrase, args=(line,))
                threads.append(t)
                t.start()

                if len(threads) == MAX_THREADS:
                    for t in threads:
                        t.join()

                    threads.clear()

if __name__ == "__main__":
    main()
