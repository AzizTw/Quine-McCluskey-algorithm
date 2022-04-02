from kmap_solver import *

terms, without_dont_cares = parse_minterms(input("Enter function: "))
prime_implicants = get_prime_implicants(terms)
essential_prime_implicants = get_essential_prime_implicants(prime_implicants,without_dont_cares)
implicant_to_minterms, minterm_to_implicants = get_coverage_dicts(prime_implicants,without_dont_cares)
sops = get_all_min_sop_forms(prime_implicants,without_dont_cares)
4
print(f'Terms = {terms}')
print(f'Prime implicants: {prime_implicants}')
print(f'Essential prime implicants: {essential_prime_implicants}')

for i, essential_prime_implicant in enumerate(essential_prime_implicants):
    print(f'Essential prime implicant {i+1} = {translate_implicant(essential_prime_implicant)}')

for i, prime_implicant in enumerate(prime_implicants):
    print(f'Prime implicant {i+1} = {translate_implicant(prime_implicant)}')

print(f'SOP forms: {get_all_min_sop_forms(prime_implicants,without_dont_cares)}')

print(sops)
for i,sop in enumerate(sops):
    print(f'SOP {i+1}: {" + ".join(list(map(translate_implicant,sop)))}')

print(f'F has {len(essential_prime_implicants)} essential prime implicants')
print(f'F has {len(prime_implicants)} prime implicants')
print(f'The simplest SOP form has {count_literals(sops[0])} literals')
print(f'The number of minimal SOP forms of F is {len(sops)}')