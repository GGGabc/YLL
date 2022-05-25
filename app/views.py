from django.shortcuts import render
from app.models import IMG
from PIL import Image
import pytesseract
from django.http import HttpResponse, HttpResponseRedirect
import os

def delete_dir(root):
    dirlist = os.listdir(root)   # 返回dir文件夹里的所有文件列表
    for f in dirlist:
        filepath = root + '\\' + f    # 路径与文件名拼接成完整的路径
        print(filepath)
        if os.path.isdir(filepath):      # 如果该文件是个文件夹
            delete_dir(filepath)        # 递归调用函数，将该文件夹内的文件删掉
            os.rmdir(filepath)         # 把文件夹删掉
        else:
            os.remove(filepath)      # 如果该文件不是文件夹，直接删除
    # os.rmdir(root)   # 最后还需要把root删掉

def uploadImg(request):
    # 如果有上传文件就存入数据库和文件夹中
    if request.method == 'POST':
        # 删除数据库的数据
        IMG.objects.all().delete()
        # 删除文件夹里面的文件
        root = r'E:\pycharm\YLL\media\img'  # 要删除的文件夹路径
        delete_dir(root)

        new_img = IMG(
            img=request.FILES.get('img'),
            name=request.FILES.get('img').name
        )
        new_img.save()
        return HttpResponseRedirect('/show')
    return render(request, 'app/uploading.html')


def showImg(request):
    # 获取文件夹的图片
    imgs = IMG.objects.all()
    content = {
        'imgs': imgs,
    }
    for i in imgs:
        image = 'E://pycharm/YLL/'+ i.img.url
        # 图像处理PIL 文字识别OCR
        pytesseract.pytesseract.tesseract_cmd = 'E://OCR/Tesseract-OCR/tesseract.exe'
        text = pytesseract.image_to_string(Image.open(image), lang='chi_sim')
    content['hello'] = text
    return render(request, 'app/showing.html', content)