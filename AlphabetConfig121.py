ALPHABET = ['а'] + [chr(i) for i in list(range(32, 127))] + [chr(i) for i in range(ord('б'), ord('ъ'))]
A = {i: ALPHABET[i] for i in range(len(ALPHABET))}
A_ID = {A[i]: i for i in A.keys()}
m = len(ALPHABET)  # 125 символов = 5^3

print(A, len(A))
