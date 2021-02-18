import random

def check_move(p,char,current):
    for move in p:
        if(move[0] == current and (move[1].find(char) == 0)):
            current = move[1].strip(char)
            return [True, current]

    return [False,current]

def check(p,string):
    path = []
    current = 'S'
    path.append(current)
    for c in string:
        [good, next] = check_move(p,c,current)
        if(good):
            current = next
            path.append(current)
        else:
            return [False,path]
    if(current == ""):
        return [True,path]
    else:
        return [False,path]


def main():

    #Read from file
    stream = open("grammar.txt","r")

    vn = ((stream.readline().strip()).split(' '))
    vt = ((stream.readline().strip()).split(' '))
    p = [];
    for line in stream:
        p.append(line.strip().split(' '))

    stream.close();
    
    #Print grammar
    print("VN = ",vn)
    print("VT = ",vt)
    print("P = {")
    for i in p:
        print(i[0], "->", i[1])
    print("}")
    

    #Generate words
    word_list = []
    for i in range(20):
        word = ""
        current = "S"
        good = True
        next = "S"
        counter = 0
        chr = vt[random.randint(0,len(vt)-1)]
        next_counter = i;
        while(counter < 100 and next != ""):
            [good, next] = check_move(p,chr,current)
            
            while(not good or (next_counter > 0 and next == "")):
                if(next == ""):
                    next_counter -= 1
                chr = vt[random.randint(0,len(vt)-1)]
                [good, next] = check_move(p,chr,current)
            word += chr;
            counter += 1
            current = next;
        if(next == "" and not word in word_list):
            word_list.append(word);

    for word in word_list:
        print(word)

    #Input string to check
    #asdf = "aababaabb"
    asdf = input("Input word:")
    [valid, path] = check(p,asdf)
    if(valid):
        print("Word is valid")
        for str in path:
            if(len(str) != 0):
                print(str,"->",end = " ")
            else:
                print("end")
    else:
        print("Word is invalid")
    #asdf.strip()


main()





#S A B C
#a b
#S aA
#A bS
#A aB
#B bC
#C aA
#C b
