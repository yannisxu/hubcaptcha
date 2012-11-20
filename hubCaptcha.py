#!/usr/bin/python
import Image,math,sys
samples = [[0.2857142857142857, 0.25, 0.3888888888888889, 0.42857142857142855], [0.08, 0.38461538461538464, 0.6666666666666666, 0.07142857142857142], [0.09090909090909091, 0.36363636363636365, 0.42857142857142855, 0.17647058823529413], [0.125, 0.5, 0.6666666666666666, 0.14285714285714285], [0.02857142857142857, 0.36363636363636365, 0.5151515151515151, 0.17647058823529413], [0.17391304347826086, 0.5652173913043478, 0.3793103448275862, 0.1111111111111111], [0.125, 0.2857142857142857, 0.42857142857142855, 0.5384615384615384], [0.16129032258064516, 0.36363636363636365, 0.13636363636363635, 0.02564102564102564], [0.3333333333333333, 0.36363636363636365, 0.47058823529411764, 0.3333333333333333], [0.3333333333333333, 0.3235294117647059, 0.3888888888888889, 0.25]]
white = (255,255,255)
black = (0,0,0)

def getAverage(pixel):
    return (pixel[0]+pixel[1]+pixel[2])/3
def divideBlackWhite(img,floor=140): 
    w,h = img.size
    pixels = img.load()
    for x in range(w):
        for y in range(h):
            pixels[x,y]=( getAverage(pixels[x,y]) ,getAverage(pixels[x,y]) ,getAverage(pixels[x,y]))
            if pixels[x,y][0] > floor:
                pixels[x,y] = white
            else:
                pixels[x,y] = black
    for x in range(1,w-1):
        for y in range(1,h-1):
            isValid = False
            for i in range(-1,2):
                for j in range(-1,2):
                    if i!=0 and j!=0 and pixels[x+i,y+j] == black:
                        isValid = True
            if not isValid:
                pixels[x,y] = white
                

def genSlideEdge(img): 
    w,h = img.size
    pixels = img.load()
    Edges = []
    lastResult = True
    isEdge = True
    thisEdge = 0
    lastEdge = 0
    for x in range(w):
        lastResult = isEdge 
        isEdge = True 
        for y in range(h):
            if pixels[x,y]!=white:
                isEdge = False
                break 
        if isEdge:
            thisEdge = x 
            if not lastResult:
                Edges.append((lastEdge,thisEdge))
            lastEdge = thisEdge 
    
    return Edges
def sliceByEdges(img,edges,minWidth=3):
    imgs = []
    w,h = img.size
    for index,item in enumerate(edges):
    #too small it can't be a number
        if item[1]-item[0]<minWidth:
            continue
        imgs.append(img.crop((item[0],0,item[1],h-1)))
    return imgs
def getRectPercentage(img,lt,rb):
    wDot = 0
    bDot = 0
    pixels = img.load()
    for x in range(lt[0],rb[0]):
        for y in range(lt[1],rb[1]):
            if pixels[x,y]==black:
                bDot += 1
            else:
                wDot += 1
    return (bDot,wDot)

def getDiff(a,b):
    result = 0
    for index,block in enumerate(a):
        result += math.fabs(b[index] - block)
    return result/4
def getSample(img):
    bands = []
    w,h = img.size
    result = 0
    bands.append(getRectPercentage(img,(0,0),(w/2,h/2)))
    bands.append(getRectPercentage(img,(w/2,0),(w,h/2)))
    bands.append(getRectPercentage(img,(w/2,h/2),(w,h))) 
    bands.append(getRectPercentage(img,(0,h/2),(w/2,h)))
    imgSample = [ float(item[0])/float(item[1]) for item in bands ] 
    return imgSample
def getSampleDiff(img,sample):
    return getDiff(sample,getSample(img))
def judege80(img):
    w,h = img.size
    pixels = img.load()
    last = white
    if pixels[w/2,h/2] == white:
        return 0
    else:
        return 8
def judege89(img):
    w,h = img.size
    pixels = img.load()
    last = white

    y = h-h/3
    i = 0
    for x in range(8):
        if pixels[x,y]==black and last == white:
            i += 1
        last = pixels[x,y] 
    if i == 1:
        return 9
    return 8

def parseStr(img,allSamples,invalidFloor=0.25):
    results = [ getSampleDiff(img,sample) for sample in allSamples] 
    result = 1
    number = -1
    for index,item in enumerate(results):
        if result > item:
            result = item
            number = index
    if result > invalidFloor:
        return "N"
    if number == 8  or number == 9:
        number =  judege89(img) 
    if number == 8 :
        number = judege80(img)
    return str(number)
for index in range(1,len(sys.argv)):
    try:
        img = Image.open(sys.argv[index])
    except Exception,e:
        print e
        exit(1)
    divideBlackWhite(img,130)
    img.save('blackWhite.bmp')
    edges = genSlideEdge(img)
    numberPics = sliceByEdges(img,edges)
    string = ""
    for numberPic in numberPics:
        string += parseStr(numberPic,samples)
    print string
