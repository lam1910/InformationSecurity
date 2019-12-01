import string


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


def getPrimes(n):
    print('Guessing p, q so that n = p * q. Since p and q are interchangeable, assume that p < q')
    threshold_prime = int(pow(n, 0.5))
    print('The smaller prime (p) has to be no larger than the square root of n, which is {0}. Because of that, we will '
          'find the prime number that in the range of 2 to the floor (natural part) of the square root of n, '
          'which is {1}.'.format(pow(n, 0.5), threshold_prime))
    list_of_p = listAllPrime(2, threshold_prime)

    for p in list_of_p:
        if n % p == 0:
            return [p, n // p]


def encode(message):
    result = 0
    for i in range(len(message)):
        result += mapping[message[i]] * pow(26, (len(message) - i - 1))
    return result


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


def findActualD(k = 17, p = 2, q = 3, max_x = 20000):
    phiN = (p - 1) * (q - 1)
    x = 1
    while (x <= max_x):
        if (1 + x * phiN) % k == 0:
            return (1 + x * phiN)//k
        x += 1

    return -1


# calculate the totient function for any n
def phi(n):
    result = n  # Initialize result as n

    # Consider all prime factors
    # of n and for every prime
    # factor p, multiply result with (1 - 1 / p)
    p = 2
    while (p * p <= n):

        # Check if p is a prime factor.
        if (n % p == 0):

            # If yes, then update n and result
            while (n % p == 0):
                n = n // p
            result = result * (1.0 - (1.0 / (float)(p)))
        p = p + 1

    # If n has a prime factor
    # greater than sqrt(n)
    # (There can be at-most one
    # such prime factor)
    if (n > 1):
        result = result * (1.0 - (1.0 / (float)(n)))

    return (int)(result)


# square and multiply method
def decrypt(code, d, n):
    result = 1
    new_mes = code % n
    new_d = str(bin(d))
    k = 0
    for i in range(-1, -len(new_d) - 1, -1):
        if new_d[i] == '1':
            result *= pow(new_mes, pow(2, k))
        k += 1
    return result % n


def toCode(encode_mes):
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

plaintext = 'it is in the bag'
letter = list(item for item in string.ascii_lowercase)
value = list(range(26))
mapping = dict(zip(letter, value))

encrypt = 'ncx ryg gzm pcf bwj'
n = 13199
e = 17
org_d = 761
org_p = 67
org_q = 197
print('Public key as (n, e) = ({0}, {1}).'.format(n, e))
print('Encrypted word: {}'.format(encrypt))
list_of_token = encrypt.split(' ')
encrypt_num = ''
encrypt_hex = ''

for token in list_of_token:
    encrypt_num += str(encode(token))
    encrypt_hex += str(hex(encode(token)))
    if list_of_token.index(token) != len(list_of_token) - 1:
        encrypt_num += ' '
        encrypt_hex += ' '

print('\tAs a list number separated by space: {}'.format(encrypt_num))
print('\tAs a list of hexadecimal values: {}'.format(encrypt_hex))

list_of_encrypt = encrypt_num.split(' ')
list_of_encrypt = list(int(list_of_encrypt[i]) for i in range(len(list_of_encrypt)))

p, q = getPrimes(n)
print('p = {0}, q = {1}. Original p from encryption = {2}, original q from encryption = {3}'.format(p, q, org_p, org_q))
if org_p > org_q:
    print('But since p and q are interchangeable, we can change the value of p and q.')
    tmp = q
    q = p
    p = tmp
    print('Now p = {}, q = {}.'.format(p, q))
else:
    print('Which is correct.')

phiN = (p - 1) * (q - 1)
print('We will determine d by using the extended Euclidean algorithms.')
d = findActualD(e, p, q, 20000)
print('d = {0}, original d = {1}.'.format(d, org_d))
if d != org_d:
    print('Wrong d. Check algorithms and input again.')
else:
    list_of_decrypt = list(decrypt(list_of_encrypt[i], d, n) for i in range(len(list_of_encrypt)))
    list_of_words = list(toString(toCode(list_of_decrypt[i]), mapping) for i in range(len(list_of_decrypt)))
    result = ''
    for word in list_of_words:
        result += word
        if list_of_words.index(word) != len(list_of_words) - 1:
            result += ' '
    print('Final result of decryption: {}'.format(result))
    print('Original plain text: {}'.format(plaintext))
    if result != plaintext:
        print('Wrong encoding scheme. Check mapping between character and number again.')
    else:
        print('Successfully decrypt the coded message.')
