import os
import sys
import datetime
import re


text_dir = 'texts'

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
today = datetime.date.today()
start_t = datetime.datetime.now()

if not os.path.exists(os.path.join(BASE_DIR, text_dir)):
    os.mkdir(os.path.join(BASE_DIR, text_dir))


def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    BASE_DIR = 'private'
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.path.join(BASE_DIR,"gdf-service-f0c823f4a436.json")
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    # print('Texts:')
    test_list = []

    for text in texts:
        # print('\n"{}"'.format(text.description))
        test_list.append(text.description)

        # 위치 정보
        # vertices = (['({},{})'.format(vertex.x, vertex.y)
        #             for vertex in text.bounding_poly.vertices])

        # print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return test_list


img_dir = os.path.join(BASE_DIR, f'detail/{today}')
imgs = os.listdir(img_dir)

total = len(imgs)
for img in imgs:
    i = imgs.index(img)
    
    img_abs_path = os.path.join(img_dir, img)
    try:
        texts = detect_text(img_abs_path)
    except Exception as err:
        print(f"{err}\nskip this image")
    file_name = img.split('_')[0]
    file_path = os.path.join(os.path.join(BASE_DIR, text_dir), f'{file_name}.txt')
    with open(file_path, 'a') as txtfile:
        text = ' '.join(texts)
        text = re.sub('\n', ' ', text)
        txtfile.write(text)
    finish_t = datetime.datetime.now()
    runtime = finish_t - start_t
    print(f'\r{i}/{total} runtime={runtime}',end='')

# texts = detect_text('/Users/ssamko/Downloads/detail_img/19W_OKS_WJP4_04_03.jpg')
# print(''.join(texts))
# with open('test.txt','w') as f:
#     f.write(' '.join(texts))