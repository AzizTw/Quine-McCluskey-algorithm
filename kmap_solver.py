from itertools import combinations
import re
global num_of_variables 
num_of_variables = int(input("Input num of variables: "))
def to_binary(num) -> str:
    """
    Returns the binary representation of the number in str format
    """
    binary_num = format(int(num), 'b')
    if len(binary_num) < num_of_variables:
        binary_num = "0" * (num_of_variables - len(binary_num)) + binary_num
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

def count_literals(sop):
    """
    Returns the number of literals in the sop
    """
    return sum([(len(implicant) - implicant.count("-")) for implicant in sop])

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
    implicants_all_sizes = [minterms if i == 0 else set() for i in range(len(list(minterms)[0])+1)]
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

def is_covering_all_minterms(sop: set, minterms: set):
    """
    Returns true if the sop covers all the minterms
    """
    covered_minterms = set()
    for implicant in sop:
        for minterm in minterms:
            if is_covered(minterm,implicant):
                covered_minterms.add(minterm)
    return covered_minterms == minterms

def get_all_min_sop_forms(prime_implicants,without_dont_cares):
    """
    Returns all the min sop forms
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
    if len(minterms_needed_to_get_covered) == 0:
        return [list(essential_prime_implicants)]
    #all combinations of sops
    #print all implicants that can cover the minterms
    usable_implicants = set()
    for implicant in prime_implicants:
        for minterm in minterms_needed_to_get_covered:
            if is_covered(minterm,implicant):
                usable_implicants.add(implicant)
                
    base_sop = list(essential_prime_implicants)
    possible_sops = []
    for i in range(1,len(minterms_needed_to_get_covered)+1):
        possible_sops.extend(list(combinations(usable_implicants,i)))
    
    sops = list()
    for tuble in possible_sops:
        sop = base_sop.copy()
        for implicant in tuble:
            sop.append(implicant)
        if is_covering_all_minterms(sop,without_dont_cares):
            sops.append(sop)
    min_sop_len = min([len(sop) for sop in sops])
    min_sops = []
    for sop in sops:
        if len(sop) == min_sop_len:
            min_sops.append(sop)
    return min_sops