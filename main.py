def main():
    import sys
    from kmap_solver import KMap
    from argparse import ArgumentParser, BooleanOptionalAction

    parser = ArgumentParser(description="find prime implicants, essential prime implicants, and all minimum sum of products forms.")

    parser.add_argument('-i', '--interactive', action=BooleanOptionalAction,
            default=False)

    args = parser.parse_known_args()[0]

    # maybe split this if block into its own function? I'm
    # reluctent to to change the structure of main though
    if not args.interactive and len(sys.argv) > 1:
        parser.add_argument('num_of_variables', metavar='v', type=int,
                choices=range(27), help='Number of variables in the kmap')

        args = parser.parse_known_args()[0]
        bit_limit = ((2**args.num_of_variables)-1)

        parser.add_argument('minterms', metavar='m', type=int,
                nargs='+', choices=range(bit_limit+1), help='Minterms')

        # don't cares are optional
        parser.add_argument('-d', '--dont-cares', metavar='d', nargs='*',
                type=int, help="Don't cares", choices=range(bit_limit+1))

        args = parser.parse_args();
        num_of_variables = args.num_of_variables
        minterms = set(args.minterms)
        dont_cares = set(args.dont_cares) if args.dont_cares is not None else set()

    else:
        num_of_variables = int(input("Enter the number of variables (Between 0 to 26): "))
        bit_limit = ((2**num_of_variables)-1)
        minterms = set(map(int, input(f"Enter the minterms (Between 0 to {bit_limit}): ").split()))
        dont_cares = set(map(int, input(f"Enter the dont cares (Between 0 to {bit_limit}): ").split()))

    intersection = minterms & dont_cares
    if(intersection):
        raise ValueError(f"minterms and dont_cares are not disjoint {intersection}")


    my_kmap = KMap(num_of_variables, minterms, dont_cares)

    PIs = list(map(my_kmap.translate_implicant, my_kmap.get_prime_implicants()))
    EPIs = list(map(my_kmap.translate_implicant, my_kmap.get_essential_prime_implicants()))
    sops = my_kmap.get_all_min_sop_forms()

    print("\nRESULTS:\n")

    if len(EPIs) == 0:
        print("No essential prime implicants")
    else:
        for i, EPI in enumerate(EPIs):
            print(f'EPI {i+1} = {EPI}')


    print()
    for i, PI in enumerate(PIs):
        print(f'PI {i+1} = {PI}')

    print()
    for i, sop in enumerate(sops):
        print(f'SOP {i+1}: {" + ".join(list(map(my_kmap.translate_implicant,sop)))}')

    print()


if __name__ == "__main__":
    main()
