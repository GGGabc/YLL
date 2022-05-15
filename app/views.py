from django.shortcuts import render
from app.models import IMG
from PIL import Image
import pytesseract

def uploadImg(request):
    """
    图片上传
    :param request:
    :return:
    """
    # 删除数据库的数据
    IMG.objects.all().delete()
    # 删除文件夹里面的文件（未完成）

    # 如果有上传文件就存入数据库和文件夹中
    if request.method == 'POST':
        new_img = IMG(
            img=request.FILES.get('img'),
            name=request.FILES.get('img').name
        )
        new_img.save()
    return render(request, 'app/uploading.html')


def showImg(request):
    """
    图片显示
    :param request:
    :return:
    """
    # 获取文件夹的图片
    imgs = IMG.objects.all()
    content = {
        'imgs': imgs,
    }
    for i in imgs:
        print(i.img.url)
    # 进行图像处理将处理出来的文字显示出来
    pytesseract.pytesseract.tesseract_cmd = 'E://OCR/Tesseract-OCR/tesseract.exe'
    text = pytesseract.image_to_string(Image.open('E://pycharm/YLL/media/img/2.jpg'), lang='chi_sim')
    print(text)
    content['hello'] = text
    return render(request, 'app/showing.html', content)