import re

class Point(object):
    def __init__ (self, x, y):
        self.x = float(x)
        self.y = float(y)
    def __str__ (self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

class Line(object):
    def __init__ (self, src, dst):
        self.src = src
        self.dst = dst

def intersect (l1, l2):
    x1, y1 = l1.src.x, l1.src.y 
    x2, y2 = l1.dst.x, l1.dst.y
    x3, y3 = l2.src.x, l2.src.y
    x4, y4 = l2.dst.x, l2.dst.y

    xnum = ((x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4))
    yden = ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
    
    ynum = (x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4)
    yden = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
 
    if yden != 0 and yden != 0:
        xcoor =  xnum / yden
        ycoor = ynum / yden
        if  onSegment(x1, x2, xcoor, y1, y2, ycoor) and onSegment(x3, x4, xcoor, y3, y4, ycoor):
            return (xcoor,ycoor)
    else:
        return 0

def onSegment(x1, x2, xcoor, y1, y2, ycoor):
    if min(x1, x2) <= xcoor and xcoor <= max(x1, x2) and min(y1, y2) <= ycoor and ycoor <= max(y1, y2):
        return True
    else:
        return False    

def overlap_1(l1,l2):#still
    x1, y1 = l1.src.x, l1.src.y 
    x2, y2 = l1.dst.x, l1.dst.y
    x3, y3 = l2.src.x, l2.src.y
    x4, y4 = l2.dst.x, l2.dst.y
    xden_new = (x3-x1)*(y2-y4) - (x2-x4)*(y3-y1)
    xden_new_2 = (x4-x1)*(y3-y2) - (x3-x2)*(y4-y1) 
    if xden_new == 0 and xden_new_2 == 0:
        return True
    else:
        return False

def ValidStreetName(street_name):
    if street_name == "":
        return False
    if all(x.isalpha() or x.isspace() for x in street_name):
        return True
    return False

def getPoint(vertex_stri_list):
    vertex_integer_list = []
    pattern = re.compile(r'\((\-?\d+),(\-?\d+)\)')  # ('x','y')
    vertex_stri_list = pattern.findall(vertex_stri_list)
    for i in range(0,len(vertex_stri_list)):#(x,y)
      vertex_integer_list.append((float(vertex_stri_list[i][0]),float(vertex_stri_list[i][1]))) 
    return vertex_integer_list

def reshapeGroup(re_intersect_group):#merge some more than one intersection group
    new_intersect_group = []
    tmp = []

    for j in range(len(re_intersect_group) - 1):
        for i in range(j+1, len(re_intersect_group)):
            if re_intersect_group[j][0] == re_intersect_group[i][0] and re_intersect_group[j][-1] == re_intersect_group[i][-1]:
                for m in re_intersect_group[j]:
                    tmp.append(m)
                for n in re_intersect_group[i]:
                    if n not in tmp:
                        tmp.append(n)
                    else:
                        continue
                del re_intersect_group[i]
                del re_intersect_group[j]
                new_intersect_group.append(sorted(tmp))
                tmp = []
                break
        if j == len(re_intersect_group) - 2:
            break
        
    for i in new_intersect_group:
        re_intersect_group.append(i)
    return re_intersect_group

def getEdge():
         
    road_vertex_list = []
    for i in road_dic:
        road_vertex_list.append(road_dic[i])
   
    intersect_group = []
    for i in range(len(road_vertex_list)):
        for j in range(i+1, len(road_vertex_list)):
            for m in range(len(road_vertex_list[i]) - 1):
                l1 = Line(Point(road_vertex_list[i][m][0], road_vertex_list[i][m][1]), Point(road_vertex_list[i][m+1][0], road_vertex_list[i][m+1][1]))
                for n in range(len(road_vertex_list[j])-1):
                    l2 = Line(Point(road_vertex_list[j][n][0], road_vertex_list[j][n][1]), Point(road_vertex_list[j][n+1][0], road_vertex_list[j][n+1][1]))
                    if intersect(l1, l2):#when two lines intersect
                        intersect_point = intersect(l1, l2) 
                        if [road_vertex_list[i][m], intersect_point, road_vertex_list[i][m+1]] not in intersect_group:
                            intersect_group.append([road_vertex_list[i][m], intersect_point, road_vertex_list[i][m+1]])
                        if [road_vertex_list[j][n], intersect_point, road_vertex_list[j][n+1]] not in intersect_group:
                            intersect_group.append([road_vertex_list[j][n], intersect_point, road_vertex_list[j][n+1]])                       
                    elif overlap_1(l1,l2):#when two lines overlap
                            four_nodes = [road_vertex_list[i][m], road_vertex_list[i][m+1], road_vertex_list[j][n], road_vertex_list[j][n+1]]
                            four_nodes = sorted(four_nodes)
                            intersect_group.append([four_nodes[0], four_nodes[1], four_nodes[2], four_nodes[3]])
                    else:
                        continue

    #loop until there is no change of intersect_group to make it a perfect format                   
    tmp=[]
    n=1
    while (not(tmp == intersect_group)):
        tmp=[]
        tmp=tmp+intersect_group
        intersect_group=reshapeGroup(intersect_group)
    
    pos = []
    for i in intersect_group:
        for j in i:
            if j not in pos:
                pos.append(j)
                
    output_v = {}
    id=1
    for i in pos:
        output_v[id] = i
        id=id+1
    
    print "V = {"
    for key, value in output_v.items():
        print ' ' + str(key) + ': '+'('+ str("{0:.2f}".format(value[0])) + ',' + str("{0:.2f}".format(value[1])) + ')'
    print "}"
                
    output_edges = []
        
    for i in range(len(intersect_group)):
        for j in range(len(intersect_group[i])-1): 
            
            u = list(output_v.keys())[list(output_v.values()).index(intersect_group[i][j])]
            v = list(output_v.keys())[list(output_v.values()).index(intersect_group[i][j+1])]
            
            if u != v:
                output_edges.append((u, v))
   
    output_edges = list(set(output_edges))
        
    print "E = {"
    for i in range(len(output_edges)): 
        if i == len(output_edges)-1:
            print ' <' + str(output_edges[i][0]) + ',' + str(output_edges[i][1]) + '>'
        else:
            print ' <' + str(output_edges[i][0]) + ',' + str(output_edges[i][1]) + '>,'
            
    print '}'

road_dic = {}

def main():
    while True:
        input = raw_input()
        
        if '"' in input:     
            input_list = input.split('"')

        if input == '':
            print "Error: empty input!"
        elif input[0]=='g' :
            getEdge()
        elif input[0]=='a':
            pattern = r'a \"(.+?)\" (( ?\(\-?\d+,\-?\d+\))+)\s*$'
            matchObj = re.match(pattern, input)
            if  matchObj==None or not ValidStreetName(input_list[1]):
                print "Error: invalid input!"
            else: 
                one_road_vertex=getPoint(input_list[2])
                if input_list[1].lower() not in road_dic:
                    road_dic[input_list[1].lower()] = one_road_vertex
                else:
                    print "Error: street name already exists!"            
        elif input[0]=='c':
            pattern = r'c \"(.+?)\" (( ?\(\-?\d+,\-?\d+\))+)\s*$'
            matchObj = re.match(pattern, input)
            if  matchObj==None or not ValidStreetName(input_list[1]):
                print "Error: invalid input! Please check again!"
            else:
                one_road_vertex=getPoint(input_list[2])
                if input_list[1].lower() in road_dic:
                    road_dic[input_list[1].lower()] = one_road_vertex
                else:
                    print "Error: 'c' specified for a street that does not exist!"                
        elif input[0]=='r':
            pattern = r'r \"(.+?)\"'
            matchObj = re.match(pattern, input)
            if  matchObj==None or not ValidStreetName(input_list[1]):
                print "Error: invalid input!"
            else: 
                    if input_list[1].lower() in road_dic:
                        del road_dic[input_list[1].lower()]
                    else:
                        print "Error: 'r' specified for a street that does not exist!"
        else:
            print "Error: invalid input!"   
           
if __name__ == '__main__':
    main()

