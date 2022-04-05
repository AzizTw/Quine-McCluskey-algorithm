from itertools import combinations

class KMap:
    def __init__(self, num_of_vars: int, minterms: set, dont_cares: set):
        """
        Initializes the KMap object
        """
        self.num_of_vars = num_of_vars
        # minterms and dont cares are converted to binary
        self.minterms = set(map(self.to_binary, minterms))
        self.dont_cares = set(map(self.to_binary, dont_cares))
        self.minterms_and_dont_cares = self.minterms.union(self.dont_cares)
        self.prime_implicants = self.get_prime_implicants()
        self.implicant_to_minterms, self.minterm_to_implicants = self.get_coverage_dicts()
        self.essential_prime_implicants = self.get_essential_prime_implicants()

    def to_binary(self, num) -> str:
        """
        Returns the binary representation of the number in str format
        """
        binary_num = format(int(num), 'b')
        if len(binary_num) < self.num_of_vars:
            # 0 extension to the left
            binary_num = "0" * (self.num_of_vars - len(binary_num)) + binary_num
        return binary_num

    def differ_by_one_bit(self, minterm1, minterm2):
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

    def translate_implicant(self, implicant):
        """
        input: implicant in binary form of any length
        output: the implicant as a literal form in string format
        Ex:
            1-1 -> AC
            01-- -> A'B
            1--01 -> AD'E
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
    

    def count_literals(self, sop):
        """
        Returns the number of literals in the sop
        """
        return sum([(len(implicant) - implicant.count("-")) for implicant in sop])

    def is_covered(self, minterm,implicant):
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

    def get_coverage_dicts(self):
        """
        Returns a two dictionaries of the form:
            {prime_implicant: [minterms_covered]}
            {minterm: [prime implicants that cover it]}
        """
        # {prime implicant : minterms that are covered by it}
        implicant_to_minterms = {implicant:set() for implicant in self.prime_implicants}
        # {minterm : set of implicants that cover it}
        minterm_to_implicants = {minterm:set() for minterm in self.minterms}
        for minterm in self.minterms:
            for implicant in self.prime_implicants:
                if self.is_covered(minterm,implicant):
                    implicant_to_minterms[implicant].add(minterm)
                    minterm_to_implicants[minterm].add(implicant)
        return implicant_to_minterms, minterm_to_implicants
    
    def get_prime_implicants(self):
        prime_implicants = set()
        # a list of sets for each implicant size: 1,2,4,8,16
        implicants_all_sizes = [self.minterms_and_dont_cares if i == 0 else set() for i in range(self.num_of_vars+1)]
        for i, size in enumerate(implicants_all_sizes):
            for implicant1 in size:
                used_once = False
                for implicant2 in size:
                    differ = self.differ_by_one_bit(implicant1, implicant2)
                    if differ:
                        used_once = True
                        implicants_all_sizes[i+1].add(differ)
                if not used_once:
                    #Cannot be expanded further, i.e. Prime Implicant   
                    prime_implicants.add(implicant1)
        return prime_implicants
    
    def get_essential_prime_implicants(self):
        """
        Returns the essential prime implicants
        given the prime implicants and minterms without dont cares
        """
        essential_prime_implicants = set()
        for minterm, prime_implicants in self.minterm_to_implicants.items():
            #If the minterm is covered by only one prime implicant, it is essential
            if len(prime_implicants) == 1:
                essential_prime_implicants = essential_prime_implicants.union(prime_implicants)

        return essential_prime_implicants
    
    def is_covering_all_minterms(self,possible_min_sop):
        """
        Returns true if the possible_min_sop covers all the minterms
        """
        covered_minterms = set()
        for implicant in possible_min_sop:
            for minterm in self.minterms:
                if self.is_covered(minterm,implicant):
                    covered_minterms.add(minterm)
        return covered_minterms == self.minterms

    # Can be optimized more
    def get_all_min_sop_forms(self):
        """
        Returns all the min possible_min_sop forms
        """
        #determining the minterms that are not covered by essential prime implicants
        minterms_not_covered = self.minterms.copy()
        for essential_prime_implicant in self.essential_prime_implicants:
            for minterm in self.implicant_to_minterms[essential_prime_implicant]:
                if minterm in minterms_not_covered:
                    minterms_not_covered.remove(minterm)

        #If they are all covered, return the essential prime implicants, as they are the only valid sop.
        if len(minterms_not_covered) == 0:
            return [list(self.essential_prime_implicants)]

        #find all combinations of prime implciants that cover all the minterms
        else:
            usable_implicants = set()
            for minterm in minterms_not_covered:
                for prime_implicant in self.minterm_to_implicants[minterm]:
                    usable_implicants.add(prime_implicant)
                        
            combinations_of_implicants = list()
            for i in range(1,len(minterms_not_covered)+1):
                #generate all combinations of prime implicants, of length 1 to len(minterms_not_covered)
                combinations_of_implicants.extend(list(combinations(usable_implicants,i)))
            
            min_sops = list()
            min_sop_len = 0
            for combination in combinations_of_implicants:
                possible_min_sop = list(self.essential_prime_implicants)
                possible_min_sop.extend(combination)
                if self.is_covering_all_minterms(possible_min_sop):
                    if min_sop_len == 0:    
                        min_sop_len = self.count_literals(possible_min_sop)
                        min_sops.append(possible_min_sop)
                    elif self.count_literals(possible_min_sop) == min_sop_len:   
                        min_sops.append(possible_min_sop)
            return min_sops