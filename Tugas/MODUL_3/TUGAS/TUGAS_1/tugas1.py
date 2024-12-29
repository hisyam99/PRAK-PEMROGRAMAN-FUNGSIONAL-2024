from functools import reduce

def arithmetic_geometric_sequence(a, d, r, n):
    if n == 1:
        return [a]
    else:
        sequence = arithmetic_geometric_sequence(a, d, r, n - 1)
        next_term = (a + (n - 1) * d) * (r ** (n - 1))
        sequence.append(next_term)
        return sequence

def add(x, y):
    return x + y

def main():
    print("Masukkan parameter untuk menghitung baris aritmetika-geometri.")
    
    a = int(input("Masukkan suku pertama (a): "))
    d = int(input("Masukkan beda aritmetika (d): "))
    r = int(input("Masukkan rasio geometri (r): "))
    n = int(input("Masukkan jumlah suku (n): "))

    sequence = arithmetic_geometric_sequence(a, d, r, n)
    print("Baris Aritmetika-Geometri:", sequence)

    sum_of_sequence = reduce(add, sequence)
    print("Jumlah Deret (Sum of Sequence):", sum_of_sequence)

main()