import math

# forgot to save problem statement

# standing in a room with a guard. you shoot a laser gun that bounces around the room up to a certain distance
# can end up hitting yourself as well. Given a starting position and ending position, calculate all the distinct directions
# that you can shoot at and still hit the guard, while avoiding hitting yourself


# SOLUTION

def answer(dimensions, captain_position, badguy_position, distance):
    
    dic = {}
    forbidden = {}

    # 0 bounce 
    b0 = (badguy_position[0]-captain_position[0],badguy_position[1]-captain_position[1])
    if dist(b0[0], b0[1]) <= distance:
        c = gcd(abs(b0[0]),abs(b0[1]))
        b0 = (b0[0]/c,b0[1]/c)
        dic[b0] = dist(b0[0], b0[1])
    else:
        return len(dic)
    
    # 1 bounce
    b = ["T","B","L","R"]
    for direction in b:
        x = badguy_position[0]-captain_position[0]
        y = badguy_position[1]-captain_position[1]
        x2 = 0
        y2 = 0
        
        if direction == "T":
            y = dimensions[1]-captain_position[1]+dimensions[1]-badguy_position[1]
            y2 = dimensions[1]-captain_position[1]+dimensions[1]-captain_position[1]
        elif direction == "B":
            y = - captain_position[1] - badguy_position[1]
            y2 = - captain_position[1] - captain_position[1]
        elif direction == "L":
            x = - captain_position[0] - badguy_position[0]
            x2 = - captain_position[0] - captain_position[0]
           
        elif direction == "R":
            x = dimensions[0]-captain_position[0]+dimensions[0]-badguy_position[0]
            x2 = dimensions[0]-captain_position[0]+dimensions[0]-captain_position[0]
            
        
        dist_x2y2 = dist(x2, y2)
        d = gcd(abs(x2),abs(y2))
        x2,y2 = x2/d,y2/d
        if (x2,y2) not in forbidden:
            forbidden[(x2,y2)] = dist_x2y2
        
        dist_xy = dist(x, y)
        if dist(x, y) <= distance:
            c = gcd(abs(x),abs(y))
            x,y = x/c,y/c
            if (x,y) not in dic:
                dic[(x,y)] = dist_xy
                
 

    
    
    
    # multiple bounce
    b = [["T",""],["B",""],["","L"],["","R"]]  
    
    for i in xrange(0,200):
        # 5:end produce 1 each
        for i in xrange(4,len(b)):
            if b[i][1][len(b[i][1])-1] == "L":
                b[i][1] += "R"
            else:
                b[i][1] += "L"
        # 1 and 2 produce 4 more
        b.append([b[0][0],"L"])
        b.append([b[0][0],"R"])
        b.append([b[1][0],"L"])
        b.append([b[1][0],"R"])
        # 1 and 2 get extended
        if b[0][0][len(b[0][0])-1] == "T":
            b[0][0] += "B"
        else:
            b[0][0] += "T"
        if b[1][0][len(b[1][0])-1] == "T":
            b[1][0] += "B"
        else:
            b[1][0] += "T" 
        # 3 and 4 get extended
        if b[2][1][len(b[2][1])-1] == "L":
            b[2][1] += "R"
        else:
            b[2][1] += "L"
        if b[3][1][len(b[3][1])-1] == "R":
            b[3][1] += "L"
        else:
            b[3][1] += "R" 
    
        # convert configuration to coordinates
        none = bool(1)
        for config in b:
            x = badguy_position[0]-captain_position[0]
            y = badguy_position[1]-captain_position[1]
            x2 = 0
            y2 = 0
        
            # even
            if len(config[0])%2==0 and len(config[0])>0:
                # starts with T
                if config[0][0]=="T":
                    y = dimensions[1]-captain_position[1] + (len(config[0])-1)*dimensions[1] + badguy_position[1]
                    y2 = dimensions[1]-captain_position[1] + (len(config[0])-1)*dimensions[1] + captain_position[1]
                # starts with B
                else:
                    y = -captain_position[1] - (len(config[0])-1)*dimensions[1] + badguy_position[1] - dimensions[1]
                    y2 = -captain_position[1] - (len(config[0])-1)*dimensions[1] + captain_position[1] - dimensions[1]
            # odd
            elif len(config[0])%2!=0 and len(config[0])>0:
                # starts with T
                if config[0][0]=="T":
                    y = dimensions[1]-captain_position[1] + (len(config[0])-1)*dimensions[1] + dimensions[1] - badguy_position[1]
                    y2 = dimensions[1]-captain_position[1] + (len(config[0])-1)*dimensions[1] + dimensions[1] - captain_position[1]
                # starts with B
                else:
                    y = -captain_position[1] - (len(config[0])-1)*dimensions[1] - badguy_position[1]
                    y2 = -captain_position[1] - (len(config[0])-1)*dimensions[1] - captain_position[1]
            
            # even
            if len(config[1])%2==0 and len(config[1])>0 :
                # starts with R
                if config[1][0]=="R":
                    x = dimensions[0]-captain_position[0] + (len(config[1])-1)*dimensions[0] + badguy_position[0]
                    x2 = dimensions[0]-captain_position[0] + (len(config[1])-1)*dimensions[0] + captain_position[0]
                # starts with L
                else:
                    x = -captain_position[0] - (len(config[1])-1)*dimensions[0] + badguy_position[0] - dimensions[0]
                    x2 = -captain_position[0] - (len(config[1])-1)*dimensions[0] + captain_position[0] - dimensions[0]
            # odd
            elif len(config[1])%2!=0 and len(config[1])>0 :
                # starts with R
                if config[1][0]=="R":
                    x = dimensions[0]-captain_position[0] + (len(config[1])-1)*dimensions[0] + dimensions[0] - badguy_position[0]
                    x2 = dimensions[0]-captain_position[0] + (len(config[1])-1)*dimensions[0] + dimensions[0] - captain_position[0]
                # starts with L
                else:
                    x = -captain_position[0] - (len(config[1])-1)*dimensions[0] - badguy_position[0]
                    x2 = -captain_position[0] - (len(config[1])-1)*dimensions[0] - captain_position[0]
                    
            dist_x2y2 = dist(x2, y2)
            d = gcd(abs(x2),abs(y2))
            x2,y2 = x2/d,y2/d
            if (x2,y2) not in forbidden:
                forbidden[(x2,y2)] = dist_x2y2        
                    
            dist_xy = dist(x, y)
            if dist(x,y) <= distance:
                c = gcd(abs(x),abs(y))
                x,y = x/c,y/c
                if (x,y) not in dic:
                    dic[(x,y)] = dist_xy
                none = bool(0)
            
        if none:
            break
    
    toremove = []
    for (a,b) in dic:
        if (a,b) in forbidden:
            if forbidden[(a,b)] < dic[(a,b)]:
                print((a,b))
                toremove.append((a,b))
    for key in toremove:
        dic.pop(key,None)
    #print(dic)
    #print(dic)
    #print(forbidden)
        
    return len(dic)

def dist(a,b):
    return math.sqrt(pow(a,2)+pow(b,2))

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


dimensions = [300, 275]
captain_position = [150, 150]
badguy_position = [185, 100]
distance = 500

dimensions = [3, 2]
captain_position = [1, 1]
badguy_position = [2, 1]
distance = 4

#dimensions = [300, 2]
#captain_position = [1, 1]
#badguy_position = [2, 1]
#distance = 200

answer(dimensions, captain_position, badguy_position, distance)
