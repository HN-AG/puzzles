import random
from electrum import util, keystore, bitcoin, Network
import argparse
import sys
import threading
import os
import time
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
SEED_ARRAY=["agree", "air", "cash", "define", "else", "end", "find", "gap", "just", "law", "must", "now", "old", "online", "order", "pool", "post", "problem", "proof", "rely", "risk", "run", "sign", "stay", "trust", "try", "zero"]
#You can throw out at least half of the words in the picture
#Think in pairs
#Code easily, attack early
#Lost transaction costs almost users
#00212121
#Try +1
#Almost open
#Bonus clue: To triumph, one must look within. To infinity, and beyond. When you are close to home, X marks the spot. (from here)
KNOWN_PAIR_ARRAY=["code easily", "attack early", "almost open"]

#WE NEED ANOTHER 18 WORDS

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
        #g.write("SEED: "+line + "\n")
        #g.write("ADDRESS: "+btc_addr + "\n")
       # g.write("PRIVKEY: "+privkey + "\n")
        # Get balance from electrum network
        h = n.synchronous_get(('blockchain.address.get_balance',[btc_addr]))
        if (h['confirmed']+h['unconfirmed'] >= 1):
            #g.write("BALANCE: "+str(h['confirmed']+h['unconfirmed'])+"sats\n")
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
        PAIRED_LIST=""
        WORD_COUNT=0
        SEED_TO_TEST=''
        for suit in my_shuffle(SEED_ARRAY):
            if (WORD_COUNT <= 18): 
                word=word+" "+suit
                WORD_COUNT+= 1
            if (WORD_COUNT == 18): 
            
            
            
                #pair up the shuffled words  
                CHOSEN_WORDS=word.split()
                PAIRED_LIST=[]
                PAIRED_LIST.append('code easily')
                PAIRED_LIST.append('attack early')
                PAIRED_LIST.append('almost open')
                PAIRED_LIST.append(CHOSEN_WORDS[0]+' '+CHOSEN_WORDS[1])
                PAIRED_LIST.append(CHOSEN_WORDS[2]+' '+CHOSEN_WORDS[3])
                PAIRED_LIST.append(CHOSEN_WORDS[4]+' '+CHOSEN_WORDS[5])
                PAIRED_LIST.append(CHOSEN_WORDS[6]+' '+CHOSEN_WORDS[7])
                PAIRED_LIST.append(CHOSEN_WORDS[8]+' '+CHOSEN_WORDS[9])
                PAIRED_LIST.append(CHOSEN_WORDS[10]+' '+CHOSEN_WORDS[11])
                PAIRED_LIST.append(CHOSEN_WORDS[12]+' '+CHOSEN_WORDS[13])
                PAIRED_LIST.append(CHOSEN_WORDS[14]+' '+CHOSEN_WORDS[15])
                PAIRED_LIST.append(CHOSEN_WORDS[16]+' '+CHOSEN_WORDS[17])
                # Now shuffle the pairs  and generate seed phrase
                PAIRED_WORDS=""
                PAIRED_WORD_COUNT=0
 
                for PAIR in my_shuffle(PAIRED_LIST):
                    if (PAIRED_WORD_COUNT <= 12): 
                        PAIRED_WORDS=PAIRED_WORDS+" "+PAIR
                        PAIRED_WORD_COUNT+= 1
                    if (PAIRED_WORD_COUNT == 12): 
                        line = PAIRED_WORDS
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
