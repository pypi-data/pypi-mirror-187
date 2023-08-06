from pobaidu.core.ImageProcess import ImageProcess

ip = ImageProcess()


def selfie_anime(img_path):
    ip.selfie_anime(img_path)


def colourize(img_path, output_path=r'./colourize.jpg'):
    ip.colourize(img_path, output_path)
