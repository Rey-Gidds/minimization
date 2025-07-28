from collections import defaultdict
from bisect  import bisect_right
from time import sleep

# Global declarations
group = {}
leftout = set()
seen = set()
ans = []
parameters = []
variables = 0

# Helper functions
def tobin(num , bits):
    binary_str = ""
    for i in range(bits - 1 , -1 , -1):
        k = num>>i
        if k&1:
            binary_str += '1'
        else:
            binary_str += '0'
    return binary_str

def groupbyOnes(parameters):
    group = defaultdict(list)
    for s in parameters:
        one_count = s.count('1')
        group[one_count].append(s)
    return group

def validBits(s , t):
    l1 = list(s)
    l2 = list(t)
    diff = 0
    for bit in range(len(l1)):
        if l1[bit] != l2[bit]:
            diff += 1
            # replace with the underscores
            l2[bit] = '_'
    # only valid for only one difference in target and source
    if diff == 1:
        return ''.join(l2)
    return False

def get_next_key(d, current_key):
    # gets the next key for the given current key to compare the current group with the next group
    keys = sorted(d.keys())
    idx = bisect_right(keys, current_key)
    return keys[idx] if idx < len(keys) - 1 else None

def minimize():
    global group
    leftout.clear()
    while True:
        merged = False
        any_merged = False
        for key in group.keys():
            current_group = key
            next_group = get_next_key(group , key)
            if next_group and group[current_group]:
                # if any single combination found update the any_merged to True
                merged = tabulation(current_group , next_group)
                if merged:
                    any_merged = True
        # if no combination is found , that's where we'll end the algorithm.
        if not any_merged:
            break

def tabulation(current_group , next_group):
    global group , leftout , seen
    # Stores the used terms to filter out the not used terms into the leftout array.
    used = set()
    # Stack to maintain the state of the new_terms being made for further iterations
    stk = []
    merged = False
    for s in group[current_group]:
        for cs in group[next_group]:
            new_term = validBits(s , cs)
            if new_term:
                if new_term not in seen:
                    stk.append(new_term)
                    seen.add(new_term)
                    merged = True
                used.add(s)
                used.add(cs)

    for term in parameters:
        # Add the uncombined terms into the leftout
        if term not in used:
            leftout.add(term)

    if stk:  
        # Update the group with the new stack for further iterations.
        group[current_group].clear()
        group[current_group].extend(stk)
        parameters[:] = sorted(set(stk))
    else:
        ans[:] = parameters
    print(f'current group: {current_group} => {group[current_group]} || next group: {next_group} => {group[next_group]}')
    sleep(0.5)
    return merged

# Follows mostly the same logic as the minimization function.
def dissolveLeftout(li):
    global ans
    changed = True
    # Set with all the answer and leftout terms
    valid_set = set(li)
    while changed:
        changed = False
        # Stores the new terms that are formed
        new_terms = set()
        # Stores the used terms that can be merged
        used = set()
        li = list(sorted(valid_set))
        for i in range(len(li)):
            for j in range(i + 1, len(li)):
                valid = validBits(li[i], li[j])
                if valid:
                    new_terms.add(valid)
                    used.add(li[i])
                    used.add(li[j])
                    changed = True
        # Update the valid set by removing the merged terms and adding the new terms generated
        valid_set = (valid_set - used).union(new_terms)
    # Make the answer list with the final valid set
    ans[:] = list(valid_set)


def generateAnswer(li):
    sum = ""
    alphabets = ''
    for i in range(variables):
        alphabets += chr(ord('A') + i)
    for s in li:
        product = ""
        for i in range(len(s)):
            if s[i] != '_':
                product += alphabets[i]
                if s[i] == '0':
                    product += "'"
        sum += product + ' + '
    # to remove the last '_+_' from the final answer
    return sum[:len(sum) - 3]

# Main function.
def main():
    global variables, parameters, group, seen, ans, leftout

    variables = int(input("Enter the number of variables: "))
    size = int(input("Enter the number of minterms: "))
    raw_params = list(int(input(f"Enter minterm {i + 1}: ")) for i in range(size))

    parameters = list(tobin(num, variables) for num in raw_params)
    group = groupbyOnes(parameters)
    seen.clear()
    ans.clear()
    leftout.clear()

    print("\n--- Minimizing ---")
    minimize()
    final_list = ans + list(leftout)
    dissolveLeftout(final_list)

    print("\n--- Final Answer ---")
    print("Implicants:", ans)
    print("SOP:", generateAnswer(ans))

# Run
if __name__ == "__main__":
    main()
