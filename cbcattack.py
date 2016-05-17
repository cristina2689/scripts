import sys
import random
import string
import time
from Crypto.Cipher import AES

IV = 'Hristos a inviat'
plaintext = dict()

def strxor(a, b): # xor two strings (trims the longer input)
  return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b)])

def hexxor(a, b): # xor two hex strings (trims the longer input)
  ha = a.decode('hex')
  hb = b.decode('hex')
  return "".join([chr(ord(x) ^ ord(y)).encode('hex') for (x, y) in zip(ha, hb)])

def bitxor(a, b): # xor two bit strings (trims the longer input)
  return "".join([str(int(x)^int(y)) for (x, y) in zip(a, b)])

def str2bin(ss):
  """
    Transform a string (e.g. 'Hello') into a string of bits
  """
  bs = ''
  for c in ss:
    bs = bs + bin(ord(c))[2:].zfill(8)
  return bs

def str2int(ss):
  """
    Transform a string (e.g. 'Hello') into a (long) integer by converting
    first to a bistream
  """
  bs = str2bin(ss)
  li = int(bs, 2)
  return li

def hex2bin(hs):
  """
    Transform a hex string (e.g. 'a2') into a string of bits (e.g.10100010)
  """
  bs = ''
  for c in hs:
    bs = bs + bin(int(c,16))[2:].zfill(4)
  return bs

def bin2hex(bs):
  """
    Transform a bit string into a hex string
  """
  bv = int(bs,2)
  return int2hexstring(bv)

def byte2bin(bval):
  """
    Transform a byte (8-bit) value into a bitstring
  """
  return bin(bval)[2:].zfill(8)

def int2hexstring(bval):
  """
    Transform an int value into a hexstring (even number of characters)
  """
  hs = hex(bval)[2:]
  lh = len(hs)
  return hs.zfill(lh + lh%2)
  
def check_cbcpad(c):
  """
  Oracle for checking if a given ciphertext has correct CBC-padding.
  That is, it checks that the last n bytes all have the value n.

  Args:
    c is the ciphertext to be checked. Note: the key is supposed to be
    known just by the oracle.

  Return 1 if the pad is correct, 0 otherwise.
  """
  ko = 'Sfantul Gheorghe'
  m = aes_dec_cbc(ko, c, IV)
  lm = len(m)
  lb = ord(m[lm-1])

  if lb > lm:
    return 0

  for k in range(lb):
    if ord(m[lm-1-k]) != lb:
      return 0

  return 1

def aes_enc(k, m):
  """
  Encrypt a message m with a key k in ECB mode using AES as follows:
  c = AES(k, m)

  Args:
    m should be a bytestring multiple of 16 bytes (i.e. a sequence of characters such as 'Hello...' or '\x02\x04...')
    k should be a bytestring of length exactly 16 bytes.

  Return:
    The bytestring ciphertext c
  """
  aes = AES.new(k)
  c = aes.encrypt(m)

  return c

def aes_dec(k, c):
  """
  Decrypt a ciphertext c with a key k in ECB mode using AES as follows:
  m = AES(k, c)

  Args:
    c should be a bytestring multiple of 16 bytes (i.e. a sequence of characters such as 'Hello...' or '\x02\x04...')
    k should be a bytestring of length exactly 16 bytes.

  Return:
    The bytestring message m
  """
  aes = AES.new(k)
  m = aes.decrypt(c)

  return m

def aes_enc_cbc(k, m, iv):
  """
  Encrypt a message m with a key k in CBC mode using AES as follows:
  c = AES(k, m)

  Args:
    m should be a bytestring multiple of 16 bytes (i.e. a sequence of characters such as 'Hello...' or '\x02\x04...')
    k should be a bytestring of length exactly 16 bytes.
    iv should be a bytestring of length exactly 16 bytes.

  Return:
    The bytestring ciphertext c
  """
  aes = AES.new(k, AES.MODE_CBC, iv)
  c = aes.encrypt(m)

  return c

def aes_dec_cbc(k, c, iv):
  """
  Decrypt a ciphertext c with a key k in CBC mode using AES as follows:
  m = AES(k, c)

  Args:
    c should be a bytestring multiple of 16 bytes (i.e. a sequence of characters such as 'Hello...' or '\x02\x04...')
    k should be a bytestring of length exactly 16 bytes.
    iv should be a bytestring of length exactly 16 bytes.

  Return:
    The bytestring message m
  """
  aes = AES.new(k, AES.MODE_CBC, iv)
  m = aes.decrypt(c)

  return m

def main():

  # Find the message corresponding to this ciphertext by using the cbc-padding attack
  c = '553b43d4b821332868fece8149eea14a2b0a98c7bed43cc1cf75f4e778cb315dc1d928d0340e0aab4900ca8af9adaee761e2affa3e9996d81483e950b913492b'
  ct = c.decode('hex')

  #Check correct padding
  print 'Oracle check of pad = ' + str(check_cbcpad(ct))

  # TODO: implement the CBC-padding attack to find the message corresponding to the above ciphertext
  # Note: you cannot use the key known by the oracle
  # You can use the known IV in order to recover the full message

  c0 = IV.encode('hex')
  c1 = c[0:32]
  c2 = c[32:64]
  c3 = c[64:96]
  c4 = c[96:128]
  # Second and fourth need range(256)
  # cbcattack(c3,c4)
  # cbcattack(c1,c2)
  # First and third need reversed(range(256))
  cbcattack(c0,c1)
  cbcattack(c2,c3)

#   Construct a ciphertext = c0 + guessed values + c1
#   1. For P[1] = 0x01 => ciphertext = c[0:15] + guessed + c1
#   2. Send it to the oracle and expect TRUE
#   3. Find real plaintext = c[16] ^ Intermediary[16]
#  plaintext = c[16] ^ 0x01 ^ guess
#
def cbcattack(c0,c1):
  intermediary = dict()
  plaintext = ''
  # one byte at a time
  for i in range(16,0,-1):
    first = c0[0:2 *(i-1)]
    last = ''
    const = int2hexstring(16 - i + 1) # 0x01, 0x02, ...
    # last bytes determined from previous calculus
    for lst_index in range(16, i, -1):
      last = hexxor(intermediary[lst_index], const) + last
    # brute guess the ith byte for P[i] = const
    for guess in reversed(range(256)):
   #for guess in range(256):
      mciphertext = first + int2hexstring(guess) + last + c1
      if len(mciphertext) != 64:
        print "length error", len(mciphertext)
      if check_cbcpad(mciphertext.decode('hex')) == 1:
        intermediary[i] = hexxor(int2hexstring(guess), const)
        plaintext = hexxor(intermediary[i], c0[2*i - 2:2*i]) + plaintext
        print plaintext.decode('hex')
        break
  print plaintext.decode('hex')

if __name__ == "__main__":
  main()
