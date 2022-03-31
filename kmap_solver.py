import re

def to_binary(num) -> str:
    """
    Returns the binary representation of the number in str format
    """
    binary_num = format(int(num), 'b')
    if len(binary_num) < 4:
        binary_num = "0" * (4 - len(binary_num)) + binary_num
    return binary_num


#Only for easier testing only
def parse_minterms(input):
    minterms = re.findall(r'\d+',input.split("Sum")[1])
    dont_cares = re.findall(r'\d+',input.split("Sum")[2])

    dont_cares = [(to_binary(dont_care)) for dont_care in dont_cares]
    #append dont_cares to minterms
    without_dont_cares = [to_binary(minterm) for minterm in minterms]
    all_minterms = without_dont_cares + dont_cares
    return set(all_minterms), set(without_dont_cares)


def differ_by_one_bit(minterm1, minterm2):
    """
    Returns the implicant that differs by one bit from minterm1 and minterm2
    """
    differ_count = 0
    final_num = ""
    for bit1, bit2 in zip(minterm1, minterm2):
        if bit1 != bit2:
            differ_count += 1
            final_num = final_num + "-"
        else:
            final_num += bit1

    return final_num if differ_count == 1 else None


def translate_implicant(implicant):
    """
    Returns the implicant as a literal form
    Ex:
        1--1 -> AD
        01-- -> A'B
        --1- -> C'
    """

    # if it covers all the minterms
    if implicant.count("-") == len(implicant):
        return "1"
    returned_implicant = ""
    for i, bit in enumerate(implicant):
        if bit == "0":
            returned_implicant += chr(ord('A') + i) + "'"
        elif bit == "1":
            returned_implicant += chr(ord('A') + i)
    return returned_implicant


def is_covered(minterm,implicant):
    """
    Returns true if the minterm is covered by the implicant
    """
    is_covered = True
    for minterm_bit, implicant_bit in zip(minterm,implicant):
        if implicant_bit == "-":
            continue
        elif implicant_bit != minterm_bit:
            is_covered = False
            break
    return is_covered


def get_essential_prime_implicants(prime_implicants,without_dont_cares):
    """
    Returns the essential prime implicants
    given the prime implicants and minterms without dont cares
    """
    essential_prime_implicants = set()
    implicant_to_minterms, minterm_to_implicants = get_coverage_dicts(prime_implicants,without_dont_cares)

    for minterm, prime_implicants in minterm_to_implicants.items():
        #If the minterm is covered by only one prime implicant, it is essential
        if len(prime_implicants) == 1:
            essential_prime_implicant = prime_implicants.pop()
            essential_prime_implicants.add(essential_prime_implicant)


    
    # essential_prime_implicants = set()
    # for minterm in without_dont_cares:
    #     times_covered = 0
    #     essential_implicant = ""
    #     for implicant in prime_implicants:
    #         if is_covered(minterm,implicant):
    #             essential_implicant = implicant
    #             times_covered += 1
    #     if times_covered == 1:
    #         essential_prime_implicants.add(essential_implicant)
    # print(f'Set 1 and Set 2 are equal : {essential_prime_implicants1 == essential_prime_implicants}')
    return essential_prime_implicants

def get_coverage_dicts(prime_implicants,without_dont_cares):
    """
    Returns a dictionary of the form {prime_implicant: [minterms_covered]}
    """
    # {prime implicant : minterms that are covered by it}
    implicant_to_minterms = {implicant:set() for implicant in prime_implicants}
    # {minterm : set of implicants that cover it}
    minterm_to_implicants = {minterm:set() for minterm in without_dont_cares}
    for minterm in without_dont_cares:
        for implicant in prime_implicants:
            if is_covered(minterm,implicant):
                implicant_to_minterms[implicant].add(minterm)
                minterm_to_implicants[minterm].add(implicant)
    return implicant_to_minterms, minterm_to_implicants

def get_prime_implicants(minterms):
    prime_implicants = set()
    # a list of sets for each implicant size: 1,2,4,8,16
    implicants_all_sizes = [minterms if i == 0 else set() for i in range(5)]
    for i, size in enumerate(implicants_all_sizes):
        for implicant1 in size:
            used_once = False
            for implicant2 in size:
                differ = differ_by_one_bit(implicant1, implicant2)
                if differ:
                    used_once = True
                    implicants_all_sizes[i+1].add(differ)
            if not used_once:
                #Cannot be expanded further, i.e. Prime Implicant   
                prime_implicants.add(implicant1)
    return prime_implicants

#  ------ Not finished ---------
def get_all_min_sop_forms(prime_implicants,without_dont_cares):
    """
    Returns a set of all minimum SOP forms
    """
    possible_sops = []
    minterms_needed_to_get_covered = without_dont_cares.copy()
    essential_prime_implicants = get_essential_prime_implicants(prime_implicants,without_dont_cares)
    implicant_to_minterms, minterm_to_implicants = get_coverage_dicts(prime_implicants,without_dont_cares)
    # determining the minterms that are covered by essential prime implicants
    for essential_prime_implicant in essential_prime_implicants:
        for minterm in implicant_to_minterms[essential_prime_implicant]:
            if minterm in minterms_needed_to_get_covered:
                minterms_needed_to_get_covered.remove(minterm)
    print(f'Minterms needed to get covered: {minterms_needed_to_get_covered}')
    #all combinations of sops
    

    
    print(f'possible sops: {possible_sops}')


# terms, without_dont_cares = parse_minterms("F(a, b, c, d) = Sum(m(4,8,11,10,12,15)) + Sum(d(9,14))")
terms, without_dont_cares = parse_minterms("Let F(a, b, c, d) = Sum(m(1, 2, 3, 4, 6, 9, 13, 14, 15)) + Sum(d(11))")
# terms, without_dont_cares = parse_minterms("Let F(a, b, c, d) = Sum(m(1, 2, 3, 4, 6, 9, 13, 14, 15,0,5,7,12,8,10,11)) + Sum(d())")
prime_implicants = get_prime_implicants(terms)
essential_prime_implicants = get_essential_prime_implicants(prime_implicants,without_dont_cares)


print(f'Terms = {terms}')
print(f'Prime implicants: {prime_implicants}')
print(f'Essential prime implicants: {essential_prime_implicants}')

for i, essential_prime_implicant in enumerate(essential_prime_implicants):
    print(f'Essential prime implicant {i+1} = {translate_implicant(essential_prime_implicant)}')

for i, prime_implicant in enumerate(prime_implicants):
    print(f'Prime implicant {i+1} = {translate_implicant(prime_implicant)}')

print(f'SOP forms: {get_all_min_sop_forms(prime_implicants,without_dont_cares)}')




