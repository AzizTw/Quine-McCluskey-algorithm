import re

def to_binary(num) -> str:
    binary_num = format(int(num), 'b')
    if len(binary_num) < 4:
        binary_num = "0" * (4 - len(binary_num)) + binary_num
    return binary_num


def parse_minterms(input):
    minterms = re.findall(r'\d+',input.split("Sum")[1])
    dont_cares = re.findall(r'\d+',input.split("Sum")[2])

    dont_cares = [(to_binary(dont_care)) for dont_care in dont_cares]
    #append dont_cares to minterms
    without_dont_cares = [to_binary(minterm) for minterm in minterms]
    all_minterms = without_dont_cares + dont_cares
    return set(all_minterms), set(without_dont_cares)


def differ_by_one_bit(num1, num2):
    differ_count = 0
    final_num = ""
    for i, bit in enumerate(str(num1)):
        if bit != num2[i]:
            differ_count += 1
            final_num = final_num + "-"
        else:
            final_num += bit

    return final_num if differ_count == 1 else None


def translate_implicant(implicant):
    returned_implicant = ""
    for i, bit in enumerate(implicant):
        if bit == "0":
            returned_implicant += chr(ord('A') + i) + "'"
        elif bit == "1":
            returned_implicant += chr(ord('A') + i)
    return returned_implicant

# determines if a minterm is covered by a prime implicant
def is_covered(minterm,implicant):
    is_covered = True
    for i, bit in enumerate(minterm):
        if implicant[i] == "-":
            continue
        elif implicant[i] != bit:
            is_covered = False
            break
    return is_covered


def get_essential_prime_implicants(prime_implicants,without_dont_cares):
    essential_prime_implicants = set()
    for minterm in without_dont_cares:
        times_covered = 0
        essential_implicant = ""
        for implicant in prime_implicants:
            if is_covered(minterm,implicant):
                essential_implicant = implicant
                times_covered += 1
        if times_covered == 1:
            essential_prime_implicants.add(essential_implicant)
    return essential_prime_implicants

def find_prime_implicants(terms):
    size_one_implicants = terms
    size_two_implicants = set()
    size_four_implicants = set()
    size_eight_implicants = set()
    size_sixteen_implicants = set()
    prime_implicants = set()
    implicants_all_sizes = [size_one_implicants,size_two_implicants,
                            size_four_implicants,size_eight_implicants,size_sixteen_implicants]
    for i, size in enumerate(implicants_all_sizes):
        for implicant1 in size:
            used_once = False
            for implicant2 in size:
                differ = differ_by_one_bit(implicant1, implicant2)
                if differ:
                    used_once = True
                    implicants_all_sizes[i+1].add(differ)           
            if not used_once:
                prime_implicants.add(implicant1)
    return prime_implicants

def get_all_sop_forms(prime_implicants,without_dont_cares):
    essential_prime_implicant = get_essential_prime_implicants(prime_implicants,without_dont_cares)
    print(essential_prime_implicant)

terms, without_dont_cares = parse_minterms(" Sum(m(0, 3, 5, 6, 8, 9, 10, 12, 14, 15)) + Sum(d(4, 11)).")
prime_implicants = find_prime_implicants(terms)
essential_prime_implicants = get_essential_prime_implicants(prime_implicants,without_dont_cares)


print(f'Terms = {terms}')
print(f'Prime implicants: {prime_implicants}')
print(f'Essential prime implicants: {essential_prime_implicants}')

for i, essential_prime_implicant in enumerate(essential_prime_implicants):
    print(f'Essential prime implicant {i+1} = {translate_implicant(essential_prime_implicant)}')


