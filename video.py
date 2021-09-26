from PIL import Image, ImageDraw, ImageFont
import os, sys
import shutil

# 灰阶值越大，取越后面的字符
symbols = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'.   ")
scale = 4    # 长宽扩大倍数
border = 1  # 边框宽度
fnt = ImageFont.truetype('C:\Windows\Fonts\Arial.ttf', int(scale*3))
intervalPixel = 3     # 间隔多少个像素点来填充，使图片看起来不密集，提高转化时间
thumbnailMaxSize = 400, 400 # 缩略图最大长宽像素

#生成字符画,在第104行调用！！！！！！
def asciiConvert(srcDir, targetDir): 
    print('开始生成...')
    jpegList = sorted(os.listdir(srcDir))
    jpegCount = len(jpegList)
    
    i = 1
    #输出所有缩略图文件和文件夹，对每一张图进行操作
    for picture in jpegList:
        (pixels, xSize, ySize) = loadPicture(os.path.join(srcDir, picture))  #调用转灰度图函数
        picToAscii(pixels, symbols,os.path.join(targetDir, picture), xSize, ySize)  #调用灰度图转字符画
        print('正在生成中... {0}/{1}'.format(i, jpegCount))
        i += 1

def createThumbnail(srcDir, targetDir):
    jpegList = sorted(os.listdir(srcDir))
    for picture in jpegList:
        img = Image.open(os.path.join(srcDir, picture))
        img.thumbnail(thumbnailMaxSize, Image.ANTIALIAS)
        img.save(os.path.join(targetDir, os.path.basename(picture)))

#将图片转为灰度图
def loadPicture(filename):
    img = Image.open(filename).convert('L')
    (x, y) = img.size
    pixels = list(img.getdata())
    img.close()
    return (pixels, x, y)


#在第21行调用！！！！！！
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

# 创建文件夹
def createDir(path):
    if not os.path.exists(path):
        os.mkdir(path)

# 删除文件夹
def deleteDir(path):
    if os.path.exists(path):
        os.remove(path)

#创建目录
def videoToAscii(srcFile):
    createDir('./temp_pic')
    createDir('./temp_thum')
    createDir('./temp_ascii')
    createDir('./temp_voice')

    # 提取音频 ./temp_voice/temp.mp3
    slice_audio_cmd = 'ffmpeg.exe -i {0} -vn ./temp_voice/temp.mp3'.format(srcFile)  
    os.system(slice_audio_cmd)
    # 视频转图片到 ./temp_pic 文件夹
    slice_pic_cmd = 'ffmpeg.exe -i {0} -r 24 ./temp_pic/%06d.jpeg'.format(srcFile) 
    os.system(slice_pic_cmd)
    #生成缩略图 保存到./temp_thum
    createThumbnail('./temp_pic', './temp_thum') 
    #生成字符画 保存到./temp_ascii
    asciiConvert('./temp_thum', './temp_ascii') 
    #合成字符视频
    dst_name = os.path.join(os.path.dirname(srcFile), 'ascii_' + os.path.basename(srcFile))    #os.path.dirname(path)
    merge_ascii_video_cmd = 'ffmpeg -threads 2 -start_number 000001 -r 24 -i {0}/%06d.jpeg -i ./temp_voice/temp.mp3 -vcodec mpeg4 {1}'.format('./temp_ascii', dst_name)
    os.system(merge_ascii_video_cmd)

    print('生成完成！')
    #删除一些临时的文件及文件夹
    deleteDir('./temp_pic')
    deleteDir('./temp_thum')
    deleteDir('./temp_ascii')
    deleteDir('./temp_voice')

if __name__ == '__main__':
    srcFile = 'gua.mp4'    #待转换视频的文件路径
    videoToAscii(srcFile)   #调用函数