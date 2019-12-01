import string
import random as rd
import math


def listAllPrime(floor = 2, givenNumber = 100):
    # Initialize a list
    primes = []
    for possiblePrime in range(floor, givenNumber + 1):  # Assume number is prime until shown it is not.
        isPrime = True
        for num in range(2, int(possiblePrime ** 0.5) + 1):
            if possiblePrime % num == 0:
                isPrime = False
                break

        if isPrime:
            primes.append(possiblePrime)

    return primes


def gcd(k, m):
    if k <= 0 or m <= 0:
        raise ValueError("Cannot calculate GCD for 0")
    else:
        while(k != m):
            if (k > m):
                k = k - m
            else:
                m = m - k
    return k


def lcm(k, m):
    g = gcd(k,m)
    return int(k * m / g)


def selectPossiblek(ceiling = 2000, p = 2, q = 3):
    list_of_k = listAllPrime(2, ceiling)
    phiN = (p - 1) * (q - 1)
    for num in list_of_k:
        if phiN % num == 0:
            del list_of_k[list_of_k.index(num)]
    return list_of_k


def selectActuald(k = 17, p = 2, q = 3, max_x = 20000):
    phiN = (p - 1) * (q - 1)
    x = 1
    while (x <= max_x):
        if (1 + x * phiN) % k == 0:
            return (1 + x * phiN)//k
        x += 1

    return -1


def encode(message):
    result = 0
    for i in range(len(message)):
        result += mapping[message[i]] * pow(26, (len(message) - i - 1))
    return result


# square and multiply method
def encrypt(message, e, n):
    result = 1
    new_mes = message % n
    new_e = str(bin(e))
    k = 0
    for i in range(-1, -len(new_e) - 1, -1):
        if new_e[i] == '1':
            result *= pow(new_mes, pow(2, k))
        k += 1
    return result % n


def toCode(encode_mes):
    if encode_mes == 0:
        return [0]
    else:
        len_mes = 0
        tmp = encode_mes
        list_of_char = []
        while pow(26, len_mes) <= tmp:
            len_mes += 1

        for i in range(len_mes - 1, -1, -1):
            list_of_char.append(tmp // pow(26, i))
            tmp = tmp % pow(26, i)

        return list_of_char


def toString(list_of_charcode, scheme):
    char = list(scheme.keys())
    result = ''
    for charcode in list_of_charcode:
        result += char[charcode]
    return result


letter = list(item for item in string.ascii_lowercase)
value = list(range(26))
mapping = dict(zip(letter, value))

input = 'It is in the bag'
input = input.lower()

list_of_token = input.split(' ')
list_of_encode = []

for token in list_of_token:
    result = 0
    if not token.isalpha():
        list_of_token[list_of_token.index(token)] = token[:-1]
        token = token[:-1]
        list_of_encode.append(encode(token))
    else:
        list_of_encode.append(encode(token))

print('The smaller prime of the two has to be no larger than the square root of product of them, which in turn has to '
      'be bigger than {} (biggest number of encoded message m)'.format(max(list_of_encode)))

print('Selecting prime p randomly from a list of all prime from 2 to {}'.format(int(pow(max(list_of_encode), 0.5))))
print('Selecting prime q randomly from a list of all prime '
      'from {0} to {1}'.format(int(pow(max(list_of_encode), 0.5)), max(list_of_encode)))
target_p = listAllPrime(2, int(pow(max(list_of_encode), 0.5)))
print('Since p, q are interchangeable, assume p < q. Choose p')
p = rd.choice(target_p)                 # p = 67
print('Minimum q so n = p * q > {0} will be {1}'.format(max(list_of_encode), max(list_of_encode) // p + 1))
print('We only need to find a prime number that is slightly bigger than {0}. So we just take the interval of '
      '1001 numbers from {1}'.format(max(list_of_encode) // p + 1, max(list_of_encode) // p + 1))
target_q = listAllPrime(max(list_of_encode) // p + 1, max(list_of_encode) // p + 1000)
q = target_q[0]                         # q = 197
print('Selection completed. We will use: p = {0}, q = {1}'.format(p, q))

n = p * q
phiN = (p - 1) * (q - 1)

print('Due to limitation of the machine, we cannot find all k satisfied the condition. We just find a small prime '
      'number that does not the divisor of totient function of (p * q)')
ks = selectPossiblek(500, p, q)
list_of_d = []
for k_tmp in ks:
    list_of_d.append(selectActuald(k_tmp, p, q, 20000))

k = ks[4]                           # k = 17
d = list_of_d[4]                    # d = 761

print('Selected k = {0} and d = {1}. They will be use as public key exponent and private key exponent '
      'respectively.'.format(k, d))
print('Selected e = {0}, which made the public key as (n, e) = ({1}, {2}).'.format(k, n, k))
print('Encrypting the message.')
print('Original message without case: {}'.format(input))
plaintext = ''
for token in list_of_token:
    plaintext += token
    if list_of_token.index(token) != len(list_of_token) - 1:
        plaintext += ' '

print('Message before encode: {}'.format(plaintext))

encoded = ''
hex_encoded = ''
for item in list_of_encode:
    encoded += str(item)
    hex_encoded += str(hex(item))
    if list_of_encode.index(item) != len(list_of_encode) - 1:
        encoded += ' '
        hex_encoded += ' '

print('After encode: {}'.format(encoded))
print('\tas a string of hexadecimal numbers: {}'.format(hex_encoded))
encrypted_words = []
for item in list_of_encode:
    encrypted_words.append(encrypt(item, k , n))

encrypted = ''
hex_encrypted = ''
text_encrypted = ''
for word in encrypted_words:
    encrypted += str(word)
    hex_encrypted += str(hex(word))
    text_encrypted += toString(toCode(word), mapping)
    if encrypted_words.index(word) != len(encrypted_words) - 1:
        encrypted += ' '
        hex_encrypted += ' '
        text_encrypted += ' '

print('After encrypted with RSA: {}'.format(encrypted))
print('\tas a string of hexadecimal numbers: {}'.format(hex_encrypted))
print('\tas text: {}'.format(text_encrypted))

print('')
print('____________________________________')
print('Possible weakness: Since a = 0, b = 1, word \"a\" or a single \'word\' \"b\" would not be encrypted at all '
      'and will appeared in the cipher as a or b')
print('Because c = m ^ e mod n.')
print('\tFor:')
print('\t\tc = ciphertext')
print('\t\tm = encoded plaintext')
print('\t\t(n, e) = public key')


