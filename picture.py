from PIL import Image, ImageDraw, ImageFont
import os, sys
import shutil

# 灰阶值越大，取越后面的字符
symbols = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'.   ")
scale = 4    # 长宽扩大倍数
border = 1  # 边框宽度
fnt = ImageFont.truetype('C:\Windows\Fonts\Arial.ttf', int(scale*3))
intervalPixel = 3     #原图片间隔多少个像素点来填充，使图片看起来不密集，提高转化时间


#将图片转为灰度图
def loadPicture(filename):
    img = Image.open(filename).convert('L')
    (x, y) = img.size
    pixels = list(img.getdata())
    img.close()
    return (pixels, x, y)

#将灰度图的每一个像素点替换为相应的字符
def picToAscii(pixels, symbols, dest_name, xSize, ySize):
    img = Image.new('L',(xSize*scale + 2*border,ySize*scale + 2*border),255)
    t = ImageDraw.Draw(img)
    x = border
    y = border
    for j in range(0, ySize, intervalPixel):
        for i in range(0, xSize, intervalPixel):
            t.text((x, y),symbols[int(pixels[j*xSize + i]/256 * len(symbols))],font=fnt,fill=0)
            x += scale * intervalPixel
        x = border
        y += scale * intervalPixel
    img.save(dest_name, "JPEG")

if __name__ == '__main__':
    srcFile = 'anzhua.jpg'
    (pixels, xSize, ySize) = loadPicture(srcFile)  #调用转灰度图函数
    picToAscii(pixels, symbols, 'output.jpg', xSize, ySize)  #调用灰度图转字符画