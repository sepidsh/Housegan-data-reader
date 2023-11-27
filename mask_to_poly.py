import numpy as np
from shapely import geometry as geo

cts = [[[1,1,0],[1,1,0],[0,0,0]], [[1,1,1],[1,1,1],[1,1,0]], [[0,0,1],[0,1,1],[0,1,1]], [[0,0,0],[0,1,1],[1,1,1]]]
cts = [[np.rot90(c, 0), np.rot90(c,1), np.rot90(c,2), np.rot90(c,3)] for c in cts]
cts = np.array(cts)
def is_contour(tmp, x):
    c = tmp[x[0]-1:x[0]+2, x[1]-1:x[1]+2]
    if(np.sum(c) not in [4,5,8]):
        return False
    for i in range(4):
        for j in range(4):
            if(np.array_equal(c , cts[j,i,:,:])):
                return True
    return False

def corner_type(tmp, c):
    c = tmp[c[0]-1:c[0]+2, c[1]-1:c[1]+2]

    for i in range(4):
        if(np.array_equal(c, cts[0,i])):
            return (i+2)%4
    for i in range(4):
        if(np.array_equal(c, cts[1,i])):
            return (i+1)%4
    for i in range(4):
        if(np.array_equal(c, cts[2,i])):
            return (i)%4
    for i in range(4):
        if(np.array_equal(c, cts[3,i])):
            return (i)%4
    assert False, "Corner type is not supported"

def preprocess(tmp):
    p1 = np.array([[0,1,1],[0,1,0],[0,0,0]])
    p2 = np.array([[1,1,0],[0,1,0],[0,0,0]])
    p3 = np.array([[1,1,1],[0,1,1],[0,0,1]])
    p4 = np.array([[1,1,1],[1,1,1],[1,0,1]])
    pts = np.transpose(np.where(tmp > 0))
    for p in pts:
        c = tmp[p[0]-1:p[0]+2, p[1]-1:p[1]+2]
        if(np.sum(c) not in [3,8,6]):
            continue
        for i in range(4):
            if(np.array_equal(c, np.rot90(p1,i))):
                tmp[p[0],p[1]]=0
            elif(np.array_equal(c, np.rot90(p2,i))):
                tmp[p[0],p[1]]=0
            elif(np.array_equal(c, np.rot90(p3,i))):
                tmp[p[0],p[1]]=0
            elif(np.array_equal(c, np.rot90(p4,i))):
                tmp[p[0]-1:p[0]+2, p[1]-1:p[1]+2] = 1

def sort_points(tmp, pts):
    points = [pts[0]]
    temp = pts[0]
    while(len(pts)>len(points)):
        ct = corner_type(tmp, temp)
        offset = [0,0]
        if(ct==3):
            candids = [p for p in pts if(p[0]==temp[0] and p[1]<temp[1])]
            diff = np.array([temp[1]-p[1] for p in candids])
            candid = candids[np.argmin(diff)]
            if(candid[0]-temp[0]!=0):
                offset[0] = temp[0] - candid[0]
        if(ct==0):
            candids = [p for p in pts if(p[1]==temp[1] and p[0]>temp[0])]
            diff = np.array([p[0]-temp[0] for p in candids])
            candid = candids[np.argmin(diff)]
            if(candid[1]-temp[1]!=0):
                offset[1] = temp[1] - candid[1]
        if(ct==1):
            candids = [p for p in pts if(p[0]==temp[0] and p[1]>temp[1])]
            diff = np.array([p[1]-temp[1] for p in candids])
            candid = candids[np.argmin(diff)]
            if(candid[0]-temp[0]!=0):
                offset[0] = temp[0] - candid[0]
        if(ct==2):
            candids = [p for p in pts if(p[1]==temp[1] and p[0]<temp[0])]
            diff = np.array([temp[0]-p[0] for p in candids])
            candid = candids[np.argmin(diff)]
            if(candid[1]-temp[1]!=0):
                offset[1] = temp[1] - candid[1]
        temp = candid
        points = points + [temp+offset]
    points = np.array(points)
    return points;


def get_polygon(mask):
    preprocess(mask)
    pts = np.transpose(np.where(mask>0))
    #print("point is",pts) 
    pts = [x for x in pts if is_contour(mask, x)]
    pts = sort_points(mask, pts)
    poly = geo.Polygon(pts)
    return poly

