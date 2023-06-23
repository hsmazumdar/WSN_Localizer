# Localize.py
# ***********************************************
# *     A new WSN Localizing Algorithm          *
# *                  by                         *
# *	         Himanshu Mazumdar                  *
# *	           Mrudang Mehta                    *
# *	      Date Start:- 28-May-2023              *
# *	     Update Date:- 19-June-2023             *
# ***********************************************
# **************************************************************
from platform import node
import tkinter as tk
from tkinter import colorchooser
from tkinter import simpledialog
import tkinter.simpledialog as simpledialog
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
import keyboard
import random
import os
import time
import threading
from random import randint
import math

# import WsnRoutPwr as rout

# **************************************************************
# Set the initial line thickness and color
node = []  # WsnNodes[] Localize at regular interval=> [ndx][sno,x,y,pow,state]
tx_delay = []  # transmit delay in mSec
packet = []  # [pktno,srcno,dstno,fromno,hopno,type]; type=>0:adm,1:msg,2:ack
packetold = []  # [pktno,srcno,dstno,fromno,hopno,type]
mynodes = []  # [ndx][n1,n2,n3,..,nn]; all nearest nodes n1,n2 in range txrange
pair = []  # list of nearest node paires of commen nearest nodes
nodexy = []  # localized nodes=>[ndx][sno,x,y,state]
screen_width = 0
screen_height = 0
distmax = 0
txrange = 100
avghops = 4
srcno = 0
dstno = 0
pkthopno = 0
fromno = 0
line_thickness = 1
line_color = "black"
nodemx = "100"
rout_speed = 0.1000
auto = False
loop = 0
drawing = False
go = True
nodeerr = []
gridX, gridY = 4, 3
ofsX, ofsY = 22, 110
test_acos = 0
test_sin = 0
test_cos = 0
area_min = 9999


# Function to open the popup window ***************************
def open_popup_max_nodes():
    global nodemx
    default_text = str(nodemx)
    text = simpledialog.askstring(
        "Enter Text", "Enter Max Nodes:", initialvalue=default_text
    )
    if text:
        nodemx = int(text)


# Function to open the popup window **************************
def open_popup_average_hops():
    global avghops
    if avghops > 7:
        avghops = 7
    if avghops < 2:
        avghops = 2
    default_text = str(avghops)
    text = simpledialog.askstring(
        "Enter Text", "Enter Average Hops:", initialvalue=default_text
    )
    if text:
        avghops = int(text)


# Populate node[] with (sno,x,y,pow,grp **********************
def GetRandomNodes(nods, gapx, wdt, gapy, hgt):
    global node, txrange, nodexy, gridX, gridY
    global screen_width, screen_height, ofsX, ofsY
    grds = gridX * gridY
    ndPerGrd = nods / grds
    nn = 0
    nnOld = 0
    grpSz = []
    sum1 = 0
    tst = 0
    for y in range(gridY):
        for x in range(gridX):
            sum1 = sum1 + ndPerGrd
            nn = int(sum1 + 0.5)
            grpSz.append(nn - nnOld)
            nnOld = nn
            tst = tst + grpSz[len(grpSz) - 1]
    dx = (screen_width - ofsX) / gridX
    dy = (screen_height - ofsY) / gridY
    no = 0
    arr1 = []
    for y in range(gridY):
        yc = int(y * dy)
        for x in range(gridX):
            xc = int(x * dx)
            for n in range(grpSz[no]):
                col1 = []
                point = [
                    xc + random.randrange(0, int(dx - 10)),
                    yc + random.randrange(0, int(dy - 10)),
                ]
                col1.append(point[0])  # x
                col1.append(point[1])  # y
                col1.append(no)  # sno
                col1.append(100)  # pow
                col1.append(0)  # state
                arr1.append(col1)
            no = no + 1
    arr1.sort()
    node = []  # class WsnNodes[]
    nodexy = []
    for i in range(nods):
        node.append([i, arr1[i][0], arr1[i][1], arr1[i][3], arr1[i][4]])
        dt = [node[i][0], 0.0, 0.0, 0]  # [sno, x, y, flg]
        nodexy.append(dt)
    brk = 123


# Draw node[] with sno ****************************************
def draw_nodes():
    global nodemx, screen_width, screen_height, distmax, txrange, distmax, nodeerr
    global gridX, gridY, ofsX, ofsY
    nodeerr = []
    mxnodes = int(nodemx)
    canvas.delete("all")
    nods = mxnodes
    GetRandomNodes(nods, 10, screen_width - ofsX, 10, screen_height - ofsY)
    draw_grid()
    for i in range(len(node)):
        draw_this_node(i, "blue", 2, "white")
        nodeerr.append(0)
    canvas.pack()
    distmax = math.sqrt(screen_width * screen_width + screen_height * screen_height)
    txrange = distmax / avghops
    populate_mynodes()
    a = 123


# Draw Grid ***************************************************
def draw_grid():
    global nodemx, screen_width, screen_height, gridX, gridY, ofsX, ofsY
    gapx = (screen_width - ofsX) / gridX
    gapy = (screen_height - ofsY) / gridY
    for x in range(gridX + 1):
        xl = x * gapx
        canvas.create_line(
            xl, 0, xl, screen_height - 1, width=1, fill="#CCCCCC"
        )  # draw line
    for y in range(gridY + 1):
        yl = y * gapy
        canvas.create_line(
            0, yl, screen_width - 1, yl, width=1, fill="#CCCCCC"
        )  # draw line


# Re-Draw Nodes ***********************************************
def re_draw_nodes():
    global nodemx, nodexy
    mxnodes = int(nodemx)
    canvas.delete("all")
    # populate_mynodes()
    # nods = mxnodes
    for i in range(len(node)):
        draw_this_node(i, "blue", 2, "white")
        nodexy[i][1] = 0  # [ndx][sno,x,y,state]
        nodexy[i][2] = 0  # [ndx][sno,x,y,state]
        nodexy[i][3] = 0  # [ndx][sno,x,y,state]
    canvas.pack()
    a = 123


# Draw One Node node[ndx] of width wdt ************************
def draw_this_node(ndx, col, wdt, bcol):
    global node
    r = True
    canvas.create_oval(
        node[ndx][1],
        node[ndx][2],
        node[ndx][1] + 20,
        node[ndx][2] + 20,
        fill=bcol,
        width=wdt,
        outline=col,
    )
    canvas.create_text(
        node[ndx][1] + 10,
        node[ndx][2] + 10,
        text=str(node[ndx][0]),
        fill="red",
        font=("Helvetica 10 bold"),
    )
    return r


# Draw One Node nodexy[ndx] of width wdt **********************
def draw_this_nodexy(ndx, col, wdt, bcol):
    global node
    r = True
    canvas.create_oval(
        nodexy[ndx][1],
        nodexy[ndx][2],
        nodexy[ndx][1] + 20,
        nodexy[ndx][2] + 20,
        fill=bcol,
        width=wdt,
        outline=col,
    )
    canvas.create_text(
        nodexy[ndx][1] + 10,
        nodexy[ndx][2] + 10,
        text=str(nodexy[ndx][0]),
        fill="red",
        font=("Helvetica 10 bold"),
    )
    return r


# get distance between n1,n2 ***********************************
def distance_n1_n2(n1, n2):
    d1x = node[n1][1]
    d1y = node[n1][2]
    d2x = node[n2][1]
    d2y = node[n2][2]
    dst2 = math.sqrt((d1x - d2x) * (d1x - d2x) + (d1y - d2y) * (d1y - d2y))
    dst2 = round(dst2, 3)
    return dst2
    a = 123


# *********************************************
def find_triangle_point_c(AB, BC, AC, x_a, y_a, x_b, y_b):
    global test_acos, test_sin, test_cos
    dy = y_b - y_a
    dx = x_b - x_a
    ang_ab = math.atan2(dy, dx)
    nu = AC * AC + AB * AB - BC * BC
    dn = 2 * AB * AC
    ang_a = 0
    test_acos = 0
    test_sin = 0
    test_cos = 0
    if abs(dn) > abs(nu):
        test_acos = nu / dn
        ang_a = math.acos(nu / dn)
    else:
        a = 123
    # a*a=b*b+c*c-2*b*c*cos(ang_bc) =>Algo
    # 2*a*b*cos(ang_bc)=(b*b+c*c-a*a)
    # ang_bc=acos((b*b+c*c-a*a)/(2*a*b)
    ang_ac = ang_ab + ang_a
    cosac = math.cos(ang_ac)
    sinac = math.sin(ang_ac)
    test_cos = cosac
    test_sin = sinac
    x_c = x_a + AC * math.cos(ang_ac)
    y_c = y_a + AC * math.sin(ang_ac)
    AB2 = math.sqrt((x_b - x_a) * (x_b - x_a) + (y_b - y_a) * (y_b - y_a))
    AC2 = math.sqrt((x_c - x_a) * (x_c - x_a) + (y_c - y_a) * (y_c - y_a))
    BC2 = math.sqrt((x_c - x_b) * (x_c - x_b) + (y_c - y_b) * (y_c - y_b))
    a = 123
    return [round(x_c, 1), round(y_c, 1)]


# **************************************************************
def update_nodexy_from_node(n):
    nodexy[n][1] = node[n][1]
    nodexy[n][2] = node[n][2]
    nodexy[n][3] = 1
    draw_this_node(n, "blue", 4, "white")


# **************************************************************
def update_nodexy(n, x, y):
    nodexy[n][1] = x
    nodexy[n][2] = y
    nodexy[n][3] = 1


# **************************************************************
def localize_nodes():
    global node, nodexy, go, slow_steps
    n1, n2, n3 = random_big_triangle_from_node()
    update_nodexy_from_node(n1)  # 1st (x,y) values given from node n1
    update_nodexy_from_node(n2)  # 2nd (x,y) values given from node n2
    update_nodexy_from_node(n3)  # 3rd (x,y) values given from node n3
    x1 = nodexy[n1][1] + 10
    y1 = nodexy[n1][2] + 10
    x2 = nodexy[n2][1] + 10
    y2 = nodexy[n2][2] + 10
    x3 = nodexy[n3][1] + 10
    y3 = nodexy[n3][2] + 10
    canvas.create_line(x1, y1, x2, y2, width=3, fill="red")  # draw line
    canvas.create_line(x1, y1, x3, y3, width=3, fill="red")  # draw line
    canvas.create_line(x2, y2, x3, y3, width=3, fill="red")  # draw line
    cn = 0
    nobad = -1
    while True:
        # time.sleep(0.1)
        if slow_steps.get() == 1:
            time.sleep(1.0)
        r = random_big_triangle_from_nodexy(nobad)  # [p1, p2, p3, p4] where p4 unknown
        if r == None:  # all nodes localized
            for i in range(len(nodexy)):
                # time.sleep(0.1)
                nd = nodexy[i]
                if nd[3] == 1:
                    draw_this_nodexy(nd[0], "blue", 2, "#00FFFF")
            break  # over
        [n1, n2, n3, n0] = r
        der = validate_location(n1, n2, n3, n0)
        if der > 10:
            a = 123
            if der == 1000:
                ts = math.sqrt(test_sin * test_sin + test_cos * test_cos)
                print(n0, area_min, test_acos, test_sin, test_cos, ts)
                # time.sleep(1)
        if cn < 2:
            nobad = n0
        else:
            nobad = -1
    a = 123


# **************************************************************
def validate_location(n1, n2, n3, n0):
    global nodeerr
    r1 = localize_nodes_from_n1_n2_n3(n1, n2, n0)
    r2 = localize_nodes_from_n1_n2_n3(n2, n3, n0)
    r3 = localize_nodes_from_n1_n2_n3(n1, n3, n0)
    rxy = []
    d1 = round(math.sqrt(r1[0][0] * r1[0][0] + r1[0][1] * r1[0][1]))
    rxy.append([d1, r1[0][0], r1[0][1]])
    d2 = round(math.sqrt(r1[1][0] * r1[1][0] + r1[1][1] * r1[1][1]))
    rxy.append([d2, r1[1][0], r1[1][1]])
    d3 = round(math.sqrt(r2[0][0] * r2[0][0] + r2[0][1] * r2[0][1]))
    rxy.append([d3, r2[0][0], r2[0][1]])
    d4 = round(math.sqrt(r2[1][0] * r2[1][0] + r2[1][1] * r2[1][1]))
    rxy.append([d4, r2[1][0], r2[1][1]])
    d5 = round(math.sqrt(r3[0][0] * r3[0][0] + r3[0][1] * r3[0][1]))
    rxy.append([d5, r3[0][0], r3[0][1]])
    d6 = round(math.sqrt(r3[1][0] * r3[1][0] + r3[1][1] * r3[1][1]))
    rxy.append([d6, r3[1][0], r3[1][1]])
    # print(rxy)
    cn = 0
    for i in range(len(rxy)):
        di = rxy[i][1]
        ji = -1
        for j in range(len(rxy)):
            if i != j:
                dj = rxy[j][1]
                if di == dj:
                    ji = j
                    cn = cn + 1
                    if cn >= 3:
                        break
        if cn >= 3:
            break
    if cn == 1:
        a = 123
    if cn == 2:
        if len(nodeerr) == 0:
            nodeerr = []
            for en in range(len(node)):
                nodeerr.append(0)
        nodeerr[n0] = nodeerr[n0] + 1
        if nodeerr[n0] > 100:
            cn = 3
        a = 123
    derr = 1000
    if cn >= 3:  # Localized here ***************************************
        nodexy[n0][1], nodexy[n0][2] = [rxy[ji][1], rxy[ji][2]]  # localize n0 node
        nodexy[n0][3] = 1  # set localized status
        derr = math.sqrt(  # localization error derr
            (rxy[ji][1] - node[n0][1]) * (rxy[ji][1] - node[n0][1])
            + (rxy[ji][2] - node[n0][2]) * (rxy[ji][2] - node[n0][2])
        )
        x1 = nodexy[n1][1] + 10  # connect localized node n0
        y1 = nodexy[n1][2] + 10  # using 3 lines from respective
        x2 = nodexy[n2][1] + 10  # source nodes n1, n2, n3
        y2 = nodexy[n2][2] + 10
        x3 = nodexy[n3][1] + 10
        y3 = nodexy[n3][2] + 10
        x0 = nodexy[n0][1] + 10
        y0 = nodexy[n0][2] + 10
        canvas.create_line(x1, y1, x0, y0, width=1, fill="blue")  # draw line
        canvas.create_line(x2, y2, x0, y0, width=1, fill="blue")  # draw line
        canvas.create_line(x3, y3, x0, y0, width=1, fill="blue")  # draw line
        if derr != 0.0:
            a = 123
            derr = 1000
    return derr


# **************************************************************
def random_big_triangle_from_nodexy(nobad):
    global node, nodexy, mynodes, area_min
    ndsel1 = []
    ndsel2 = []
    for i in range(len(nodexy)):
        if nodexy[i][3] == 1:
            ndsel1.append(i)  # list localized nodes in ndsel1[]
        else:
            ndsel2.append(i)  # list un-localized nodes in ndsel2[]
    if len(ndsel2) == 0:
        return  # Over return NIl
    buf = []
    for i in range(len(ndsel2)):  # search
        i2 = ndsel2[i]
        if nodexy[i2][3] == 0:
            mynds = mynodes[i2]
            cmn = 0
            row = []
            for j in range(len(mynds)):
                nd = mynds[j][0]

                if nodexy[nd][3] == 1:
                    cmn = cmn + 1
                    row.append(nd)
            if cmn >= 3:
                buf.append([i2, row])
                a = 123
    if len(buf) == 0:
        return
    nr = randint(0, len(buf) - 1)
    n0 = buf[nr][0]
    mr = buf[nr][1]
    [n1, n2, n3] = get_random_3_nodes(mr)
    area_min = test_set_n1_n2_n3_n0(n1, n2, n3, n0)
    draw_this_node(n0, "blue", 2, "yellow")
    return [n1, n2, n3, n0]


# **************************************************************
def test_set_n1_n2_n3_n0(n1, n2, n3, n0):
    area1 = get_area(n1, n2, n0)
    area2 = get_area(n2, n3, n0)
    area = min(area1, area2)
    area3 = get_area(n3, n1, n0)
    area = min(area, area3)
    return area  # return minimum area


# **************************************************************
def get_random_3_nodes(mr):
    for i in range(len(mr) * len(mr)):
        s1 = randint(0, len(mr)) - 1
        s2 = randint(0, len(mr)) - 1
        tmp = mr[s1]
        mr[s1] = mr[s2]
        mr[s2] = tmp
    return [mr[0], mr[1], mr[2]]


# **************************************************************
def random_big_triangle_from_nodexy_Org2(nobad):
    global node, nodexy, mynodes
    ndsel1 = []
    ndsel2 = []
    for i in range(len(nodexy)):
        if nodexy[i][3] == 1:
            ndsel1.append(i)  # list localized nodes in ndsel1[]
        else:
            ndsel2.append(i)  # list un-localized nodes in ndsel2[]
    if len(ndsel2) == 0:
        return  # Over return NIl
    # select an un-localize node having max localized nodes
    areamx = 0
    nmx1 = -1
    nmx2 = -1
    nmx3 = -1
    dstmx = 0
    p1, p2, p3, p3 = -1, -1, -1, -1
    ni = -1
    temp = []
    for i in range(100):  # search 10 times for max area
        rn1 = randint(0, len(ndsel1) - 1)  # localized nodes ndsel1
        n1 = ndsel1[rn1]  # rand from localized nodes n1
        mynd1 = mynodes[n1]  # neighbours of n1 are mynd1
        nx = len(mynd1) - 1  # nx is furthest neighbour of n1
        n2 = -1
        for i2 in range(nx):
            n2 = mynd1[nx - i2][0]  # sel furthest neighbour of n1
            if nodexy[n2][3] == 1:  # status of n2 localization
                break
        if n2 >= 0:
            mynd2 = mynodes[n2]
            cmnnds = get_common_nodes2(
                mynd1, mynd2
            )  # common nodes of mynd1 & mynd2 in cmnnds
            n3 = -1
            nx = len(cmnnds) - 1
            for j in range(nx):
                n3 = cmnnds[nx - j]  # n3 is furthest neighbour of n1 & n2
                if nodexy[n3][3] == 1:  # status of n3 localization
                    break
            if n3 >= 0:
                temp = []
                cmnnds = get_common_nodes3(n1, n2, n3)
                for k in range(len(cmnnds)):
                    nk = cmnnds[k]
                    d1 = distance_n1_n2(nk, n1)
                    d2 = distance_n1_n2(nk, n2)
                    d3 = distance_n1_n2(nk, n3)
                    dmn = min(d1, d2)
                    dmn = min(dmn, d3)
                    if dstmx < dmn:
                        dstmx = dmn
                        p1, p2, p3, p4 = n1, n2, n3, nk
                        temp.append(ni)
                a = 123
            else:
                a = 123
        else:
            a = 123

    return [p1, p2, p3, p4]


# **************************************************************
def plot_update_localized_nodes():
    re_draw_nodes()
    for i in range(len(nodexy)):
        nd = nodexy[i]
        if nd[3] == 1:
            draw_this_node(nd[0], "blue", 2, "#00FFFF")
    a = 123


# **************************************************************
def localize_nodes_from_n1_n2_n3(n1, n2, n3):
    global node, nodexy
    AB = distance_n1_n2(n1, n2)
    BC = distance_n1_n2(n2, n3)
    AC = distance_n1_n2(n1, n3)
    x_a = node[n1][1]
    y_a = node[n1][2]
    x_b = node[n2][1]
    y_b = node[n2][2]
    xc1, yc1 = find_triangle_point_c(AB, BC, AC, x_a, y_a, x_b, y_b)  # 1
    xc2, yc2 = find_triangle_point_c(AB, AC, BC, x_b, y_b, x_a, y_a)  # 1
    r = [xc1, yc1], [xc2, yc2]
    return r


# Populate my nearest mynodes **********************************
def populate_mynodes():
    global node, srcno, dstno, mynodes, txrange
    mynodes = []
    for i in range(len(node)):
        buf1 = []
        for j in range(len(node)):
            if i != j:
                buf2 = []
                d = distance_n1_n2(i, j)
                buf2.append(d)
                buf2.append(j)
                buf1.append(buf2)
        buf1.sort()
        mynds = []
        for k in range(len(buf1)):
            if buf1[k][0] <= txrange:
                nd = []
                nd.append(buf1[k][1])
                nd.append(buf1[k][0])
                mynds.append(nd)
        mynodes.append(mynds)
    a = 123


# **************************************************************
def find_nearesr_node(x, y):
    global node
    dmn = distmax
    nmn = -1
    for i in range(len(node)):
        d = abs(node[i][1] - x) + abs(node[i][2] - y)
        if dmn > d:
            dmn = d
            nmn = node[i][0]

    return nmn


# Mouse event handlers *****************************************
def on_mouse_press3(event):
    global mouse_position
    x, y = event.x, event.y
    mouse_position = (x, y)


# Mouse event handlers ****************************************
def on_mouse_press(event):
    global drawing, nodexy, mouse_position
    x, y = event.x, event.y
    mouse_position = (x, y)


# **************************************************************
def on_mouse_release(event):
    global drawing, go
    drawing = False
    go = False


# **************************************************************
def on_mouse_move(event):
    if drawing:
        global mouse_position
        x, y = event.x, event.y
        mouse_position = (x, y)


# **************************************************************
def get_area(n1, n2, n3):
    a = distance_n1_n2(n1, n2)
    b = distance_n1_n2(n1, n3)
    c = distance_n1_n2(n2, n3)
    s = (a + b + c) / 2.0
    ss = s * (s - a) * (s - b) * (s - c)
    area = 0
    if ss >= 0:
        area = math.sqrt(ss)
    return area


# Get random 3 nodes of big triangle****************************
def random_big_triangle_from_node():
    global node, nodexy, mynodes
    nomx = 0
    ndmx = len(node)
    n1 = random.randrange(0, ndmx - 1)  # sel a rand node n1
    mynd1 = mynodes[n1]  # list of nearest nodes of n1 in mynd1
    n2 = mynd1[len(mynd1) - 1][0]  # n2 is furthest node in mynd1
    mynd2 = mynodes[n2]  # list of nearest nodes of n2 in mynd2
    buf = get_common_nodes2(mynd1, mynd2)  # get list of common nodes in buf
    areamx = 0
    n3mx = -1
    for i in range(len(buf)):  # search node to form biggest area as n3
        n3 = buf[i]
        area = get_area(n1, n2, n3)
        if areamx < area:
            areamx = area
            n3mx = n3
    n3 = n3mx
    return [n1, n2, n3]


# **************************************************************
def get_common_nodes2(nds1, nds2):
    global node, nodexy, mynodes
    nds = []
    for i in range(len(node)):
        nds.append(0)
    for i in range(len(nds1)):
        nds[nds1[i][0]] = nds[nds1[i][0]] + 1
    for i in range(len(nds2)):
        nds[nds2[i][0]] = nds[nds2[i][0]] + 1
    buf = []
    for i in range(len(nds)):
        if nds[i] == 2:
            buf.append(i)
    return buf


# **************************************************************
def get_common_nodes3(ii, jj, kk):
    global node, nodexy, mynodes
    nds = []
    for n in range(len(node)):
        nds.append(0)
    for i in range(len(mynodes[ii])):
        ni = mynodes[ii][i][0]
        if nodexy[ni][3] == 0:
            nds[ni] = nds[ni] + 1
    for j in range(len(mynodes[jj])):
        nj = mynodes[jj][j][0]
        if nodexy[nj][3] == 0:
            nds[nj] = nds[nj] + 1
    for k in range(len(mynodes[kk])):
        nk = mynodes[kk][k][0]
        if nodexy[nk][3] == 0:
            nds[nk] = nds[nk] + 1
    # cmnmx = 0
    cmnnds = []
    for n in range(len(nds)):
        if nds[n] == 3:
            cmnnds.append(n)
            # cmnmx = cmnmx + 1
    a = 123
    return cmnnds


# **************************************************************
def open_file():
    global node, nodexy, txrange
    flnm = filedialog.askopenfilename(
        initialdir="",
        filetypes=(("WSN File", "*.wsn"), ("all files", "*.*")),
        title="Load WSN file (*.wsn)",
    )
    file1 = open(flnm, "r")
    wrd = file1.readline().removesuffix("\n").split(",")
    flnm = wrd[0]
    sz = int(wrd[1])
    node = []
    nodexy = []
    for i in range(sz):
        wrd = file1.readline().removesuffix("\n").split(",")
        row = []
        row.append(int(wrd[0]))  # sno
        row.append(int(wrd[1]))  # x
        row.append(int(wrd[2]))  # y
        row.append(int(wrd[3]))  # pow
        row.append(int(wrd[4]))  # state
        node.append(row)
        dt = [int(wrd[0]), 0.0, 0.0, 0]  # [sno, x, y, flg]
        nodexy.append(dt)
    file1.close()
    distmax = math.sqrt(screen_width * screen_width + screen_height * screen_height)
    txrange = distmax / avghops
    populate_mynodes()
    re_draw_nodes()


# **************************************************************
def save_file():
    flnm = asksaveasfile(
        initialfile="LocalizeHsm.txt",
        defaultextension=".txt",
        filetypes=[("All Files", "*.*"), ("WSN File", "*.wsn")],
        title="Save WSN file (*.wsn)",
    )
    file2 = open(flnm.name, "w")
    sz = len(node)  # node: [ndx][sno,x,y,pow,state]
    pag = flnm.name + "," + str(sz) + "\n"
    for i in range(sz):
        line = node[i]
        pag += (
            str(line[0])  # sno
            + ","
            + str(line[1])  # x
            + ","
            + str(line[2])  # y
            + ","
            + str(line[3])  # pow
            + ","
            + str(line[4])  # state
            + "\n"
        )
    file2.writelines(pag)
    file2.close()


# **************************************************************
def on_resize(event):
    # Get the new size of the form
    global canvas, screen_width, screen_height
    canvas.config(width=event.width - 4, height=event.height - 4)
    screen_width, screen_height = event.width, event.height


# **************************************************************
def main_menu():
    global window, canvas, screen_width, screen_height, slow_steps
    global gridX, gridY

    # window = tk.Tk()
    window.title("WSN Localizing-HSM")
    # Configure the resize event handler
    window.bind("<Configure>", on_resize)

    # Create a Canvas widget
    # screen_width = window.winfo_screenwidth() / 1
    # screen_height = window.winfo_screenheight() / 1
    screen_width, screen_height = 800, 600
    ofsX, ofsY = 0, 0

    canvas = tk.Canvas(window, width=screen_width, height=screen_height)
    canvas.pack()

    # Maximize the window
    # window.state("zoomed")

    # Create a menu bar
    menubar = tk.Menu(window)
    window.config(menu=menubar)

    # Create the file menu
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)

    # Create the tool menu
    tool_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Tool", menu=tool_menu)

    # Create the checkbox within the sub-menu
    slow_steps = tk.IntVar()
    slow_steps.set(0)

    # Add options to the file menu
    file_menu.add_command(label="Max Nodes ", command=lambda: open_popup_max_nodes())
    file_menu.add_command(label="Avg Hops ", command=lambda: open_popup_average_hops())
    file_menu.add_command(label="Draw Nodes (cnt+d)", command=lambda: draw_nodes())
    file_menu.add_command(label="ReDraw Nodes (cnt+r)", command=lambda: re_draw_nodes())
    file_menu.add_command(
        label="Localize Nodes (cnt+z)", command=lambda: localize_nodes()
    )
    file_menu.add_separator()
    file_menu.add_command(label="Open", command=lambda: open_file())
    file_menu.add_command(label="Save", command=lambda: save_file())
    file_menu.add_separator()
    file_menu.add_command(label="Exit (cnt+x)", command=window.quit)

    # Add options to the tool menu
    tool_menu.add_checkbutton(label="Slow", variable=slow_steps)

    # register the hotkey using the keyboard library
    # keyboard.add_hotkey("ctrl+n", open_popup_max_nodes)
    keyboard.add_hotkey("ctrl+d", draw_nodes)
    keyboard.add_hotkey("ctrl+r", re_draw_nodes)
    keyboard.add_hotkey("ctrl+z", localize_nodes)
    keyboard.add_hotkey("ctrl+x", window.quit)

    # Bind the mouse event handlers to the canvas
    canvas.bind("<ButtonPress-3>", on_mouse_press3)
    canvas.bind("<ButtonPress-1>", on_mouse_press)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)
    canvas.bind("<B1-Motion>", on_mouse_move)

    # Run the main loop
    window.mainloop()


# Start the program ********************************************
window = tk.Tk()
print(os.path.dirname(__file__))
main_menu()


# **************************************************************
