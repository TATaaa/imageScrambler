# -*- encoding: utf-8 -*-
from PIL import Image
import uuid
import random
import math

class scrambler():
    
    def imageScram(self, im, key):
        RGBim = im.convert("RGB")
        imSize = RGBim.size
        intKey = int(key, 16)
        keyDigitList = self.__intToList(intKey)

        for x in range(imSize[0]):
            for y in range(imSize[1]):
                rDiff, gDiff, bDiff = self.__getRGBDiffs(intKey, keyDigitList, x, y)
                r,g,b = RGBim.getpixel((x, y))
                intKey = intKey + x + y

                r = self.__RGBRangeConst(r + rDiff)
                g = self.__RGBRangeConst(g + gDiff)
                b = self.__RGBRangeConst(b + bDiff)

                im.putpixel((x, y), (r, g, b, 0))

        print "finish."
        return im

    def unImageScram(self, im, key):
        RGBim = im.convert("RGB")
        imSize = RGBim.size
        intKey = int(key, 16)
        keyDigitList = self.__intToList(intKey)

        for x in range(imSize[0]):
            for y in range(imSize[1]):
                rDiff, gDiff, bDiff = self.__getRGBDiffs(intKey, keyDigitList, x, y)
                r,g,b = RGBim.getpixel((x, y))
                intKey = intKey + x + y
                
                r = abs(r - rDiff)
                g = abs(g - gDiff)
                b = abs(b - bDiff)

                im.putpixel((x, y), (r, g, b, 0))

        print "finish"
        return im
    
    def __getRGBDiffs(self, intKey, keyDigitList, x, y):
        seedFunc = lambda a, b, c, d: intKey + ((keyDigitList[(len(keyDigitList) - 1)] + 1) % (a + b + 1) - (keyDigitList[(len(keyDigitList) - 1)] + 1) % (c + d + 1))
        rDiff = self.__getRGBDiff(seedFunc(x, y, x, x))
        gDiff = self.__getRGBDiff(seedFunc(x, x, y, y))
        bDiff = self.__getRGBDiff(seedFunc(x, x, y, x))
        return rDiff, gDiff, bDiff

    def __intToList(self, Num):
        List = []
        while Num != 0:
            List.append(Num % 10)
            Num /= 10
        
        return List

    def __getRGBDiff(self, seedNum):
        random.seed(seedNum)
        return random.randint(0, 256)

    def __RGBRangeConst(self, num):
        if num > 256:
            return num - 256
        else :
            return num

if __name__ == "__main__":
    import sys

    args = sys.argv
    scram = scrambler()

    im = Image.open(args[1])

    print "Scramble  : 1"
    print "unScranble: 2"
    choice = input("> ")

    if choice == 1:
        key = uuid.uuid4().hex
        im = scram.imageScram(im, key)
        print "key: " + key
        im.show()
        im.save(args[1] + "_after.png")
    elif choice == 2:
        print "pls give me uuid"
        key = raw_input("> ")
        im = scram.unImageScram(im, key)
        im.show()
        im.save(args[1] + "_before.png")
    else :
        print "The choice you entered is not correct"
