# coding:utf-8

import sys
import utils
#in this demo, if not found the nonce(its not possible), just pass it in case some errors happen.
from errors import NonceNotFoundError

class ProofOfWork(object):
    """
    pow 
    """
    _N_BITS = 4
    MAX_BITS = 256
    MAX_SIZE = sys.maxsize #The fixed difficulty value.
    def __init__(self, block, n_bits=_N_BITS):
        self._n_bits = n_bits
        self._target_bits = 1 << (self.MAX_BITS - n_bits)#The target difficult value is a fixed value, not automatic.
        self._block = block

    def _prepare_data(self, nonce):
        #data_lst is the dataset of the block header.
        data_lst = [str(self._block.block_header.prev_block_hash),#the previous block's hash.
                    str(self._block.block_header.hash_merkle_root),#this block's merkle tree_root.
                    str(self._block.block_header.timestamp),#the timestamp.
                    str(self._block.block_header.height),#height.
                    str(nonce)]#the nonce that meet the demand of the previous block.
        return utils.encode(''.join(data_lst))

    def run(self):
        nonce = 0
        found = False#if find the nonce, this value will be True
        hash_hex = None
        print('Mining a new block')
        while nonce < self.MAX_SIZE:
            data = self._prepare_data(nonce)
            #using the hash function to get the hash value with the certain nonce.
            hash_hex = utils.sum256_hex(data)
            #transfer the value to hex.
            hash_val = int(hash_hex, 16)
            #output the result:
            sys.stdout.write("data: %s\n" % data)
            sys.stdout.write("try nonce == %d\thash_hex == %s \n" % (nonce, hash_hex))
            if (hash_val < self._target_bits):
                found = True
                break
            #if the nonce is not meet the demand, nonce++, until find the correct nonce that make hash value < the target value.
            nonce += 1 
        if found: 
            print('Found nonce == %d' % nonce)
        else:
            print('Not Found nonce')
            raise NonceNotFoundError('nonce not found')
        return nonce, hash_hex#The final result.

    def validate(self):
        """
        validate the block
        """
        data = self._prepare_data(self._block.block_header.nonce)
        print("data:"+str(data))
        hash_hex = utils.sum256_hex(data)#Hash the block, using SHA-256
        hash_val = int(hash_hex, 16)#The hash value is hex.
        print(hash_hex)
        return hash_val < self._target_bits #Hash value must < the target value.