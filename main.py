from kmap import KMap
num_of_variables = int(input("Enter the number of variables: "))
minterms = set(map(int, input("Enter the minterms: ").split()))
dont_cares = set(map(int, input("Enter the dont cares: ").split()))

my_kmap = KMap(num_of_variables, minterms, dont_cares)

PIs = list(map(my_kmap.translate_implicant, my_kmap.get_prime_implicants()))
EPIs = list(map(my_kmap.translate_implicant, my_kmap.get_essential_prime_implicants()))
sops = my_kmap.get_all_min_sop_forms()

print("\nRESULTS:\n")

for i, PI in enumerate(PIs):
    print(f'PI {i+1} = {PI}')

print()
for i, EPI in enumerate(EPIs):
    print(f'EPI {i+1} = {EPI}')

print()
for i, sop in enumerate(sops):
    print(f'SOP {i+1}: {" + ".join(list(map(my_kmap.translate_implicant,sop)))}')