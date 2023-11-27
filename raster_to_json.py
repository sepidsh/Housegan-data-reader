import json
import argparse
import numpy as np
# import matplotlib.pyplot as plt
from shapely.geometry import Polygon
# from descartes.patch import PolygonPatch
from read_dd import read_data

import warnings


def raster_to_json(line, print_door_warning):
    """ convert extracted data from rasters to housegan ++ data format :  extract rooms type, bbox, doors, edges and neigbour rooms
                
    """
    # fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1)
    bbox_x1=[]
    bbox_y1=[]
    bbox_x2=[]
    bbox_y2=[]
    walls=[]

    room_type,poly,doors_, walls,out=read_data(line)

    d=[]
    all_doors=[]
    for i in range(1,len(doors_)+1):
        if((i)%4==0 ) & (i+1!=1):
            d.append(doors_[i-1])
            all_doors.append(d)
            d=[]
        elif(i==1):
            d=[]
        if(i%4!=0):
            d.append(doors_[i-1])
    kh=0
    al_dr=0
    for hd in range(len(all_doors)):
        dr_t=[]
        dr_in=[]
        doors=all_doors[hd]
        d_t=2
        t_x=abs(doors[0][1]-doors[1][1])
        t_y=abs(doors[0][0]-doors[3][0])
        ss=t_x
        if(t_x>t_y):
           d_t=1
           ss=t_y
        elif(t_x<t_y):
           d_t=3
        for pmc in range(5):
            for dw in range(len(doors)):      
                for nw in range(len(walls)) :
                    if(walls[nw][5]==17):
                        continue
                    if(walls[nw][5]==15):
                        continue
                    if (d_t<=2) &(doors[dw][0]-doors[dw][2]<=1)& (walls[nw][0]-walls[nw][2]<=1)& (abs(doors[dw][0]-walls[nw][0])<=(ss-1)) & (abs(doors[dw][2]-walls[nw][2])<=(ss-1)): 
                        l=doors[dw][1]
                        r=doors[dw][3]
                        if(l>r):
                            t=l
                            l=r
                            r=t
                        l_=walls[nw][1]
                        r_=walls[nw][3]
                        if(l_>r_):
                            t=l_
                            l_=r_
                            r_=t
                        if (((r-r_)<=pmc )& (pmc>=(l_-l))) :
                            if(len(dr_in)<2):
                                if(walls[nw][6] not in dr_t):
                                    dr_t.append(walls[nw][6])
                                    dr_in.append(nw)
                               
                    elif (d_t>=2)& (doors[dw][1]-doors[dw][3]<=1)& (walls[nw][1]-walls[nw][3]<=1) &(abs(doors[dw][1]-walls[nw][1])<=(ss-1)) & (abs(doors[dw][3]-walls[nw][3])<=(ss-1)): 
                        l=doors[dw][0]
                        r=doors[dw][2]
                        if(l>r):
                            t=l
                            l=r
                            r=t
                        l_=walls[nw][0]
                        r_=walls[nw][2]
                        if(l_>r_):
                            t=l_
                            l_=r_
                            r_=t
                        if(((r-r_)<=pmc )& (pmc>=(l_-l))):
                            if(len(dr_in)<2):
                                if(walls[nw][6] not in dr_t):
                                    dr_t.append(walls[nw][6])
                                    dr_in.append(nw)
        if(len(dr_t)==2):
            walls[dr_in[0]][8]=walls[dr_in[1]][5]
            walls[dr_in[0]][7]=walls[dr_in[1]][6]    
            walls[dr_in[1]][8]=walls[dr_in[0]][5]
            walls[dr_in[1]][7]=walls[dr_in[0]][6]  
            al_dr=al_dr+1
                
        else:
            if print_door_warning:
                print("sometime not 2 dooor",hd,doors)		
    
        assert(len(dr_t)<=2)
  

    assert(al_dr==(len(all_doors)-1))
    
    
    omn=[]
    tr=0
    en_pp=0
    for nw in range(len(walls)-(len(all_doors)*4),len(walls)):
        if(tr%4==0):
            omn=[]
        tr=tr+1
        for kw in range(len(walls)-(len(all_doors)*4)+1):
            if(walls[kw][5]==17)&(walls[nw][5]==17):
                continue		
            if(walls[kw][5]==15)&(walls[nw][5]==15):
                continue		
            if(walls[kw][5]==15)&(walls[nw][5]==17):
                continue		
            for pmc in range (5):
                if(abs(walls[kw][0]-walls[nw][0])<=(ss-1)) & (abs(walls[kw][2]-walls[nw][2])<=(ss-1)):
                    l=walls[kw][1]
                    r=walls[kw][3]
                    if(l>r):
                        t=l
                        l=r
                        r=t
                    l_=walls[nw][1]
                    r_=walls[nw][3]
                    if(l_>r_):
                        t=l_
                        l_=r_
                        r_=t
                    if(pmc>=r_-r )& (l-l_<=pmc) &( nw!=kw):
                        if(walls[nw][5]==17) &(walls[nw][8]==0)& (walls[kw][6] not in omn):
                            walls[nw][8]=walls[kw][5]
                            walls[nw][7]=walls[kw][6]    
                            omn.append(walls[kw][6])
                        if(walls[nw][5]==15) &(walls[nw][8]==0):
                            walls[nw][8]=walls[kw][5]
                            walls[nw][7]=walls[kw][6] 
                            en_pp=1 
                 
                if(abs(walls[kw][1]-walls[nw][1])<=(ss-1)) & (abs(walls[kw][3]-walls[nw][3])<=(ss-1)):
                    l=walls[kw][0]
                    r=walls[kw][2]
                    if(l>r):
                        t=l
                        l=r
                        r=t
                    l_=walls[nw][0]
                    r_=walls[nw][2]
                    if(l_>r_):
                        t=l_
                        l_=r_
                        r_=t
                    if(pmc>=r_-r )& (l-l_<=pmc) &( nw!=kw):
                        if(walls[nw][5]==17) & (walls[nw][8]==0)& (walls[kw][6] not in omn):
                            walls[nw][8]=walls[kw][5]
                            walls[nw][7]=walls[kw][6]    
                            omn.append(walls[kw][6])
                
                        if(walls[nw][5]==15) & (walls[nw][8]==0):
                            walls[nw][8]=walls[kw][5]
                            walls[nw][7]=walls[kw][6]    
                            en_pp=1
         
                    
    for i in range(1):
        for iw in range(len(walls)):
            tp_out=-1
            dif_x=10
            dif_y=10

            type_out=0
        for jw in range(len(walls)):
            if(walls[iw][0]==walls[iw][2]):
                if (walls[jw][0]!=walls[jw][2]):
                    continue
                if ((walls[iw][0]-walls[jw][0])==(walls[iw][2]- walls[jw][2])):
                    rnp=walls[jw][1]
                    fnp=walls[jw][3]
                    rmp=walls[iw][1]
                    fmp=walls[iw][3]
                    if( rnp<fnp):
                        t=fnp
                        fnp=rnp
                        rnp=t
                    if(rmp<fmp):
                        t=fmp
                        fmp=rmp
                        rmp=t
                    if(abs(rmp)<=abs(rnp))| (abs(fmp)<=abs(fnp)):
                        dif_x_temp=walls[iw][0]-walls[jw][0]
                        if(abs(dif_x)>abs(dif_x_temp)) & (iw!=jw):
                            dif_x=dif_x_temp
                            tp_out=walls[jw][6]
                            type_out=walls[jw][5]
                          
            elif(walls[iw][1]==walls[iw][3]):
                if ((walls[iw][1]-walls[jw][1])==(walls[iw][3]- walls[jw][3])) :           
                    rnp=walls[jw][0]
                    fnp=walls[jw][2]
                    rmp=walls[iw][0]
                    fmp=walls[iw][2]
                    if( rnp<fnp):
                        t=fnp
                        fnp=rnp
                        rnp=t
                    if(rmp<fmp):
                        t=fmp
                        fmp=rmp
                        rmp=t
                    if(abs(rmp)<=abs(rnp))| (abs(fmp)<=abs(fnp)):
                        dif_y_temp=walls[iw][1]-walls[jw][1]
                        if(abs(dif_y)>abs(dif_y_temp))&( iw!=jw ):
                            dif_y=dif_y_temp
                            tp_out=walls[jw][6]
                            type_out=walls[jw][5]
      
    km=0
    assert(en_pp==1) #throwing out really strange layouts
    
    
    lenx=1.0
    leny=1.0
    min_x=0.0
    min_y=0.0
    bboxes=[]  
    edges=[]
    ed_rm=[]
    info=dict()

    #  The edges for the graph
    for w_i in range(len(walls)):
        edges.append([((walls[w_i][0]-min_x)/lenx),((walls[w_i][1]-min_y)/leny),((walls[w_i][2]-min_x)/lenx),((walls[w_i][3]-min_y)/leny),walls[w_i][5],walls[w_i][8]])
        if(walls[w_i][6]==-1):
            ed_rm.append([walls[w_i][7]])
        elif(walls[w_i][7]==-1): 
            ed_rm.append([walls[w_i][6]])
        else:
            ed_rm.append([walls[w_i][6],walls[w_i][7]])
    
    #  The bbox for room masks
    for i in range(len(poly)):
        p=poly[i]
        pm=[]
        for p_i in range((p)):
            pm.append(([edges[km+p_i][0],edges[km+p_i][1]]))
        km=km+p
        polygon = Polygon(pm)
        # plot_coords(ax, polygon.exterior, alpha=0)
        bbox=np.asarray(polygon.bounds)
        bboxes.append(bbox.tolist())
     
        
        # patch = PolygonPatch(polygon, facecolor=semantics_cmap["bedroom"], alpha=0.7)
        # ax.add_patch(patch)
   
    info['room_type'] = room_type
    info['boxes'] = bboxes
    info['edges'] = edges
    info['ed_rm'] = ed_rm

    # print(bboxes)
   
    fp_id = line.split("/")[-1].split(".")[0]
  
    ### saving json files
    with open(f"rplan_json/{fp_id}.json","w") as f:
         json.dump(info, f)




def parse_args():
    parser = argparse.ArgumentParser(description="Structured3D 3D Visualization")
    parser.add_argument("--path", required=True,
                        help="dataset path", metavar="DIR")
    return parser.parse_args()


def main():
    args = parse_args()
    line=args.path

    try:
        raster_to_json(line, print_door_warning=False)
    except (AssertionError, ValueError, IndexError) as e:
        fp_id = line.split("/")[-1].split(".")[0]

        with open(f"failed_rplan_json/{fp_id}", "w") as f:
            f.write(str(e))

if __name__ == "__main__":

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main()
