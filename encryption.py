import string
import random as rd


def listAllPrime(givenNumber):
    # Initialize a list
    primes = []
    for possiblePrime in range(2, givenNumber + 1):  # Assume number is prime until shown it is not.
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


def selectPossiblek(ceiling = 2000):
    list_of_k = []
    for k in range(2, ceiling):
        if gcd(k, phiN) == 1:
            list_of_k.append(k)
    return list_of_k


def selectActualkd(ceiling = 2000, max_x = 20000):
    list_of_k = selectPossiblek(ceiling)
    while (len(list_of_k) > 0):
        k = list_of_k[0]
        x = 1
        while (x <= max_x):
            if (1 + x * phiN) % k == 0:
                return [k, (1 + x * phiN)//k]
            x += 1
        del list_of_k[0]

    return [0, 0]


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

input = 'Retrieve a given field value. The key argument will be either an integer or a string.'
input = input.lower()

list_of_token = input.split(' ')

for token in list_of_token:
    result = 0
    if not token.isalpha():
        list_of_token[list_of_token.index(token)] = token[:-1]
        token = token[:-1]

plaintext = ''.join(token for token in list_of_token)
encoded = encode(plaintext)
small_value = encode('leak')

print('Selecting prime p, q randomly from a list of all prime from 0 to 1000')
target = listAllPrime(1000)
# p, q = rd.choices(target, k = 2)        # p = 967, q = 601
p = 967
q = 601
print('Selection completed. We will use: p = {0}, q = {1}'.format(p, q))

n = p * q
phiN = (p - 1) * (q - 1)

k ,d = selectActualkd(400000, 100000)           # for p = 967, q = 601, have k = 11, d 52691
print('Selected k = {0} and d = {1}. They will be use as public key exponent and private key exponent '
      'respectively.'.format(k, d))
print('Selected e = {0}, which made the public key as (n, e) = ({1}, {2}).'.format(k, n, k))
print('Encrypting the message.')
print('Original message without case: {}'.format(input))
print('Message before encode: {}'.format(plaintext))
print('After encode: {}'.format(encoded))
print('\tas an hexadecimal number: {}'.format(hex(encoded)))
print('Since the message has to be in the range of (0, {0}). We will mapped encoded message as {1} (encode value of '
      'plaintext leak)'.format(n, small_value))
encrypted = encrypt(small_value, k, n)
message_after_map = toString(toCode(small_value), mapping)
print('Message after mapping {0} to {1} would be: {2}'.format(encoded, small_value, message_after_map))
print('After encrypted with RSA: {}'.format(encrypted))
print('\tas an hexadecimal number: {}'.format(hex(encrypted)))
print('\tas text: {}'.format(toString(toCode(encrypted), mapping)))
