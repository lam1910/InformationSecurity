import string


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


def getPrimes(n):
    print('Guessing p, q so that n = p * q. Since p and q are interchangeable, assume that p < q')
    threshold_prime = int(pow(n, 0.5))
    print('The smaller prime (p) has to be no larger than the square root of n, which is {0}. Because of that, we will '
          'find the prime number that in the range of 2 to the floor (natural part) of the square root of n, '
          'which is {1}.'.format(pow(n, 0.5), threshold_prime))
    list_of_p = listAllPrime(threshold_prime)

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


def findActualD(e, guess_p, guess_q):
    k = 1
    phin = (guess_p - 1) * (guess_q - 1)
    while True:
        if (k * phin + 1) % e == 0:
            return (k * phin + 1) // e


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

plaintext = 'retrieveagivenfieldvaluethekeyargumentwillbeeitheranintegerorastring'
letter = list(item for item in string.ascii_lowercase)
value = list(range(26))
mapping = dict(zip(letter, value))
mapped_message = encode('leak')
map_mes = \
    {mapped_message: 1092224042327489514445607071388446444904682493014591931546048713318488771547672717226439391049104}
encrypt = 111611
n = 581167
e = 11
org_d = 52691
org_p = 967
org_q = 601
print('Public key as (n, e) = ({0}, {1}).'.format(n, e))
print('Encrypted word: {}'.format(encrypt))
print('\tas an hexadecimal number: {}'.format(hex(encrypt)))
print('\tas text: {}'.format(toString(toCode(encrypt), mapping)))

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
d = findActualD(e, p, q)
print('d = {0}, original d = {1}.'.format(d, org_d))
if d != org_d:
    print('Wrong d. Check algorithms and input again.')
else:
    decrypted = decrypt(encrypt, d, n)
    if decrypted != mapped_message:
        print('Decrypted has unexpected error.')
    else:
        print('Due to the limitation of our machine, we have mapped that original message to {0} to be smaller than '
              'n = p * q = {1} * {2} = {3}.'.format(mapped_message, p, q, n))
        original_message = map_mes[decrypted]
        print('Message after remapped: {}'.format(original_message))
        print('\tas an hexadecimal number: {}'.format(hex(original_message)))
        chars = toCode(original_message)
        result = toString(chars, mapping)
        print('Final result of decryption: {}'.format(result))
        print('Original plain text: {}'.format(plaintext))
        if result != plaintext:
            print('Wrong encoding scheme. Check mapping between character and number again.')
        else:
            print('Successfully decrypt the coded message.')
