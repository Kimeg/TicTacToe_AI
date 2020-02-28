import numpy as np

template = [(i,j) for i in range(3) for j in range(3)]
turns = {True:'max', False:'min'}
sign = {True:1, False:-1}
record = {}
tol = 1


def h(record, maximizing):
    x = {k:0 for k in range(3)}
    y = {k:0 for k in range(3)}
    for pos in record[turns[not maximizing]]:
        x[pos[0]] += 1
        y[pos[1]] += 1

    if max(x.values())==3 or max(y.values())==3 or checkDiag(record, maximizing):
        return -1*sign[maximizing]  
    return 0

def checkDiag(record, maximizing):
    count = 0
    count2 = 0
    for pos in record[turns[not maximizing]]:
        if pos[0] == pos[1]:
            count += 1
            if pos[0] == 1:
                count2 += 1
        if abs(pos[0] - pos[1]) == 2:
            count2 += 1

    if count2==3 or count==3:
        return True
    return False

def genList():
    record = {'max':[] ,'min':[]}
    i = input()
    j = input()
    pos = (int(i), int(j))
    record['max'].append(pos)
    return record

def addtoList(pos, record, maximizing, depth):
    child = update(record, pos, maximizing, depth)
    return child

def update(record, pos, maximizing, depth):
    child = {'max':[] ,'min':[]}

    for key in child:
        for p in record[key]:

            child[key].append(p)

        if key == turns[maximizing]:
            child[turns[maximizing]].append(pos)
    return child

def genChildren(record, maximizing, depth):
    children = []

    for pos in template:
        if pos in record['max'] or pos in record['min']:
            continue
        
        child = addtoList(pos, record, maximizing, depth)
        children.append(child)
    return children 

def visualhelper(record):
    s = '\n -------------\n'
    for i, pos in enumerate(template):
        if i%3==0 and i > 0: 
            s+=' |\n'
            s+= ' -------------\n'

        if pos in record['max']:
            s += ' | O'
        elif pos in record['min']:
            s += ' | X'
        else:
            s += ' |  '
    s += ' |'
    s += '\n -------------\n'
    print(s)
    return

def visualize(record, score, depth=None):
    if depth==None:
        visualhelper(record)
        #print(score)
    #elif depth==tol:
    #    visualhelper(record)
    return

def countMarks(record):
    s = 0
    for key in record:
        s += len(record[key])
    return s

def userAdd(record):
    i = input()
    j = input()
    pos = (int(i), int(j))
    if not pos in record['max']:
        record['max'].append(pos)
    return record

def Minimax(record, depth, maximizing):
    s = h(record, maximizing)
    visualize(record, s, depth)

    if countMarks(record) == 9 or not s == 0:
        return s, record

    children = genChildren(record, maximizing, depth)

    _sign = sign[maximizing]
    score = _sign * 9999 * -1

    scores = {} 
    for child in children:
        _score, _updated =  Minimax(child, depth+1, not maximizing)           
        scores[_score] = child

        if _sign*score < _sign*_score:
            score = _score

    return score, scores[score]

def main():
    record = genList()
    MAX = 0; MIN = 0
    while(MAX==0 and MIN==0):
        score, record = Minimax(record, 0, False)

        MAX = h(record, True)
        MIN = h(record, False)

        visualize(record, score)

        record = userAdd(record) 

        if countMarks(record)==9:
            break
    return

main()
