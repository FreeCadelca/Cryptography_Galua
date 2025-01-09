ALPHABET = ['а'] + [chr(i) for i in list(range(32, 127))] + ['б', 'в', 'г', 'д']
A = {i: ALPHABET[i] for i in range(len(ALPHABET))}
A_ID = {A[i]: i for i in A.keys()}
m = len(ALPHABET)  # 100 символов = 10^2

print(A)