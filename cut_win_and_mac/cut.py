#_*_encoding:utf-8_*_
#!/usr/bin/env python 
#coding=utf-8 

#/**
# * Created by Crh.
# * User: Crh
# * Date: 15-12-2
# * Time: 下午2:00
# */
# -- 大图切小图 --

# python /Users/rains/PycharmProjects/untitled/切图工具/cut.py

        
import json
import os
import shutil
import xlrd
import sys
import Tkinter
import tkMessageBox
import tkFileDialog 
from Tkinter import *
reload(sys)
sys.setdefaultencoding( "utf-8" )

#!/usr/bin/env python  
import Image  
import sys
import ImageDraw, ImageFont, ImageFilter   

listData = []
width = 0
height = 0
twoBox = []

bx0 = 0
by0 = 0
bx1 = 0
by1 = 0

allsum = 0

Direction = [ [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0] ]

top = Tkinter.Tk()
var1=StringVar()
var2=StringVar()
var3=StringVar()

def isDigits(my_str):
    isNumber = True
    try:
        int(my_str)
        isNumber = True
    except ValueError:
        isNumber = False

    try:
        float(my_str)
        isNumber = True
    except ValueError:
        isNumber = False

    return isNumber

# 颜色
def rndColor():
    return (255, 0, 0, 200)

def getPath( str ):
    for i in xrange(0,99999999):
        print i
        if os.path.exists( str + "/%d"%i ) == False:
            os.mkdir(str + "/%d"%i)
            return "/%d"%i
    return "/-1"       

# 判断九宫格位置有没有透明像素点
def setpoint( x, y ):
    global listData
    global Direction
    for i in xrange(0,len(Direction)):
        if isMinOrMax( x + Direction[i][0], y + Direction[i][1] ):
            if listData[ x + Direction[i][0] ][ y + Direction[i][1] ] == 0:
                return True
    return False

# 偏历二维数组递归找出每个小图的最小xy和最大xy,用于在大图定位切图
def TreeRecursive( x, y ):
    global twoBox
    global bx0
    global by0
    global bx1
    global by1
    global Direction
    twoBox[x][y] = 0
    if bx0 >= y:
        bx0 = y
    if bx1 <= y:
        bx1 = y
    if by0 >= x:
        by0 = x
    if by1 <= x:
        by1 = x
    for i in xrange(0,len(Direction)):
        if isMinOrMax( x + Direction[i][0], y + Direction[i][1] ):
            if twoBox[ x + Direction[i][0] ][ y + Direction[i][1] ] == 1:
                TreeRecursive( x + Direction[i][0], y + Direction[i][1] )
    
# 坐标是否到了边界 True没有到边界 False到了边界
def isMinOrMax( x, y):
    global width
    global height
    if y < 0:
        return False
    if y >= width:
        return False
    if x < 0:
        return False
    if x >= height:
        return False
    return True

def isMaxWidth( w, num ):
    global width
    global height
    if num > 0:
        if (w + num) >= width:
            return width
        else:
            return w + num
    if num < 0:
        if (w - num) <= 0:
            return 0
        else:
            return w - num
    return w

def isMaxHeight( h, num ):
    global width
    global height
    if num > 0:
        if (h + num) >= height:
            return height
        else:
            return h + num
    if num < 0:
        if (h - num) <= 0:
            return 0
        else:
            return h - num
    return h

# 切割图片
def cuttingPicture():
    if os.path.exists( var1.get() ) == False:
        tkMessageBox.showinfo( "错误", "大图片不存在或者路径错误")
        return
    if os.path.exists( var2.get() ) == False:
        tkMessageBox.showinfo( "错误", "保存路径不存在或者格式错误")
        return
    hzm = var1.get()[var1.get().rfind('.'):]
    if hzm != ".png":
        tkMessageBox.showinfo( "错误", "暂时只支持png格式的图片")
        return
    sys.setrecursionlimit(999999999)
    global width
    global height
    global twoBox
    global bx0
    global by0
    global bx1
    global by1
    global listData
    global allsum

    listData = []
    width = 0
    height = 0
    twoBox = []

    bx0 = 0
    by0 = 0
    bx1 = 0
    by1 = 0

    im = Image.open( var1.get() )  
    width = im.size[0]  
    height = im.size[1]  
    x0 = width
    y0 = height
    x1 = 0
    y1 = 0

    
    print "/* width:%d */"%(width)  
    print "/* height:%d */"%(height)  
    
    for h in xrange(0,height):
        cellData = []
        for w in xrange(0,width):
            cellData.append( 0 )
        listData.append(cellData)

    allPoint = []
    for h in xrange(0,height):
        for w in xrange(0,width):
            pixel = im.getpixel((w, h)) 
            if pixel[3] > 0:
                listData[h][w] = 1
                # draw.point((w, h), fill=rndColor())
                if x0 >= w:
                    x0 = w
                if x1 <= w:
                    x1 = w
                if y0 >= h:
                    y0 = h
                if y1 <= h:
                    y1 = h

    for h in xrange(0,height):
        cellData = []
        for w in xrange(0,width):
            cellData.append( 0 )
            if listData[h][w] == 1:
                if setpoint(h, w):
                    # draw.point((w, h), fill=rndColor())
                    allPoint.append( [h, w] )
                    cellData[w] = 1
        twoBox.append(cellData)


    cou = 0
    path = getPath( var2.get() )
    for i in xrange(0,len(allPoint)):
        bx0 = width
        by0 = height
        bx1 = 0
        by1 = 0
        if twoBox[allPoint[i][0]][allPoint[i][1]] == 1:
            TreeRecursive( allPoint[i][0], allPoint[i][1] )
            if bx0 != bx1:
                if by0 != by1:
                    region = im.crop( (bx0, by0, bx1, by1) )
                    region.save( var2.get()+ path + "/small_%d.png"%cou, 'png' )
                    cou = cou + 1
    print cou

    tkMessageBox.showinfo( "Tips", "切割成功，一共%d张小图片"%cou + " 路径：" + var2.get()+ path)
    allsum = allsum + 1

def choiceDirectory():
    filename = tkFileDialog.askopenfilename(parent=top,initialdir="/",defaultextension=".png",title='Pick a png')
    var1.set( filename )

def saveDirectory():
    filename = tkFileDialog.askdirectory(parent=top,initialdir="/",title='Pick a directory')
    var2.set( filename )

def showTips():
    tkMessageBox.showinfo( "说明", "将大图自动智能切割分成一张张不规则的小图，暂时只是支持 png格式，要求图片背景是透明，缩放功能请在后面填入你要缩小的倍率，点击缩放就能生成，icon是手机app需要用的icon尺寸")

def updataScale():
    if os.path.exists( var1.get() ) == False:
        tkMessageBox.showinfo( "错误", "大图片不存在或者路径错误")
        return
    if os.path.exists( var2.get() ) == False:
        tkMessageBox.showinfo( "错误", "保存路径不存在或者格式错误")
        return
    if not isDigits( var3.get() ) :
        tkMessageBox.showinfo( "Tips", "输入的缩放倍率不是数字")
        return

    hzm = var1.get()[var1.get().rfind('.'):]
    if hzm == var1.get()[len(var1.get())-1]:
        tkMessageBox.showinfo( "错误", "大图片不存在或者路径错误")
        return

    scale = float( var3.get() )
    print scale
    im = Image.open( var1.get() )
    w, h = im.size
    im.resize((int(w*scale), int(h*scale)), Image.ANTIALIAS)
    im.save( var2.get() + '/ScaleXXXXXX' + hzm, hzm[1:] )
    tkMessageBox.showinfo( "Tips", "缩放成功，路径：" + var2.get() + '/ScaleXXXXXX' + hzm )

def updataAllScale():
    if os.path.exists( var1.get() ) == False:
        tkMessageBox.showinfo( "错误", "大图片不存在或者路径错误")
        return
    if os.path.exists( var2.get() ) == False:
        tkMessageBox.showinfo( "错误", "保存路径不存在或者格式错误")
        return
    hzm = var1.get()[var1.get().rfind('.'):]
    if hzm == var1.get()[len(var1.get())-1]:
        tkMessageBox.showinfo( "错误", "大图片不存在或者路径错误")
        return

    allsize = [ 144, 128, 96, 72, 48, 36, 32, 24 ]
    if os.path.exists( var2.get() + "/res" ) == False:
        os.mkdir(var2.get() + "/res/")

    for x in xrange(0, len(allsize)):
        im = Image.open( var1.get() )
        im.thumbnail((allsize[x], allsize[x]))
        im.save( var2.get() + '/res/icon%d'%allsize[x] + hzm, hzm[1:] )
    tkMessageBox.showinfo( "Tips", "生成成功，路径：" + var2.get() + "/res" )

def initUI():

    top.title("图片处理")
    top.geometry('480x320')
    top.resizable(width=False, height=False)
    
    # -------------------
    btns1 = Tkinter.Button(top, text ="选择目标大图片", command = choiceDirectory)
    btns1.grid(column=1, row=1)
    E1 = Entry(top, bd =5, textvariable=var1)
    E1.grid(column=4, row=1)
    
    # -------------------
    btns2 = Tkinter.Button(top, text ="选择保存文件夹", command = saveDirectory)
    btns2.grid(column=1, row=2)
    E2 = Entry(top, bd =5, textvariable=var2)
    E2.grid(column=4, row=2)

    # -------------------
    btn = Tkinter.Button(top, text ="切割", command = cuttingPicture)
    btn.grid(column=3, row=8)

    # -------------------
    btn = Tkinter.Button(top, text ="缩放", command = updataScale)
    btn.grid(column=3, row=9)
    E1 = Entry(top, bd =5, textvariable=var3)
    E1.grid(column=4, row=9)

    # -------------------
    btn = Tkinter.Button(top, text ="一键生成icon", command = updataAllScale)
    btn.grid(column=3, row=10)

    btn = Tkinter.Button(top, text ="说明", command = showTips)
    btn.grid(column=5, row=11)

    var = StringVar()
    label = Label( top, textvariable=var, relief=RAISED )
    var.set("Creator is Crh\nLanguage By Python\nversion 1.1\ncrh4@foxmail.com")
    label.grid(column=1, row=0)
    
    top.mainloop()


if __name__=="__main__":
    initUI()
    