# -*- encoding: utf-8 -*-
from PIL import Image
import uuid
import random

class scrambler():
    
    MAX_RGB = 256
    MIN_RGB = 0

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

                r = self.__RGBRangeConstMax(r + rDiff)
                g = self.__RGBRangeConstMax(g + gDiff)
                b = self.__RGBRangeConstMax(b + bDiff)

                im.putpixel((x, y), (r, g, b, 0))

        print("finish.")
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
                
                r = self.__RGBRangeConstMin(r - rDiff)
                g = self.__RGBRangeConstMin(g - gDiff)
                b = self.__RGBRangeConstMin(b - bDiff)

                im.putpixel((x, y), (r, g, b, 0))

        print("finish")
        return im
    
    def __getRGBDiffs(self, intKey, keyDigitList, x, y):
        seedFunc = lambda a, b, c, d: intKey + ((keyDigitList[(a + b + c * d) % (len(keyDigitList) - 1)]) % (a + b + c * d + 1) - (keyDigitList[(a * b + c + d) % (len(keyDigitList) - 1)]) % (a * b + c + d + 1))
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
        return random.randint(0, self.MAX_RGB)

    def __RGBRangeConstMax(self, num):
        if num >= self.MAX_RGB:
            return num - self.MAX_RGB
        else :
            return num

    def __RGBRangeConstMin(self, num):
        if num < self.MIN_RGB:
            return num + self.MAX_RGB
        else :
            return num

if __name__ == "__main__":
    import sys

    args = sys.argv
    scram = scrambler()

    im = Image.open(args[1])

    print("Scramble  : 1")
    print("unScranble: 2")
    choice = int(input("> "))

    if choice == 1:
        key = uuid.uuid4().hex
        im = scram.imageScram(im, key)
        print("key: " + key)
        im.save(args[1] + "_Scram.png")
    elif choice == 2:
        print("pls give me uuid")
        key = input("> ")
        im = scram.unImageScram(im, key)
        im.save(args[1] + "_unScram.png")
    else :
        print("The choice you entered is not correct")
