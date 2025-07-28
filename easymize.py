# from collections import defaultdict
# from bisect  import bisect_right

def tobin(num , bits):
    binary_str = ""
    for i in range(bits - 1 , -1 , -1):
        k = num>>i
        if k&1:
            binary_str += '1'
        else:
            binary_str += '0'
    return binary_str

# def groupbyOnes(parameters):
#     group = defaultdict(set)
#     for s in parameters:
#         one_count = s.count('1')
#         group[one_count].add(s)
#     return group

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

variables = int(input("Enter the number of variables: "))
size = int(input('Enter the number of parameters to add: '))
parameters = list(int(input('Enter the non-duplicate parameter: ')) for _ in range(size))
parameters = list(tobin(num , variables) for num in parameters)
# group = groupbyOnes(parameters)
# print('Group: ' , group)
ans = []
leftout = []
def minimize(parameters):
    leftout.clear() 
    global ans
    while parameters:
        seen = set()
        stk = []
        # Stores the terms that has been used to merge into another term
        used = set()
        for i in range(len(parameters)):
            for j in range(i + 1, len(parameters)):
                valid = validBits(parameters[i], parameters[j])
                if valid:
                    if valid not in seen:
                        # construct the new table for later iteration
                        stk.append(valid)
                        seen.add(valid)
                    # Add the used terms that turned out to be valid
                    used.add(parameters[i])
                    used.add(parameters[j])
        # Add all uncombined parameters to leftout
        for term in parameters:
            # Add the uncombined terms into the leftout
            if term not in used:
                leftout.append(term)
        # If there are no terms that can be merged and hence the stack is empty then copy the last calculated list that is parameter in this case
        if not stk:
            ans[:] = parameters
            break
        # Assign the new stack to the prameters for further minimization
        parameters[:] = sorted(set(stk))

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
    # Only supported for max 4 variables.
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

minimize(sorted(parameters))
valid_list = ans + leftout
dissolveLeftout(valid_list)
print(generateAnswer(ans))