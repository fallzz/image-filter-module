# -*- coding: utf-8 -*-
"""Inception v3 architecture 모델을 retraining한 모델을 이용해서 이미지에 대한 추론(inference)을 진행하는 예제"""

from flask import Flask, render_template, request, jsonify
# from flask_restful import Api
from flask_cors import CORS
# from flask.ext.cache import Cache
import numpy as np
import tensorflow as tf
import urllib.request
import cv2
import requests

from PIL import Image
from io import BytesIO

modelFullPath = '/tmp/output_graph.pb'  # 읽어들일 graph 파일 경로
labelsFullPath = '/tmp/output_labels.txt'  # 읽어들일 labels 파일 경로
# imagePath = /tmp/test.jpg                                                  # 추론을 진행할 이미지 경로

app = Flask(__name__)
# cache = Cache(app, config={'CACHE_TYPE':'simple'})
CORS(app)


# cors = CORS(app, resources={
#    r"*": {"origin" : "*"},
# })
# api = Api(app)

# Api.add_resource(T)
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        # 파라미터를 전달 받습니다.

        tagImg = []
        backImg = []
        # imageSrc = request.form['avg_img']
        imageSrc = request.json['imgs']
        print(imageSrc)

        create_graph()

        imageType = ['tagImg', 'backImg']

        for imgType in imageType:

            print("imageSrc[%s] length : %d" % (imgType, len(imageSrc[imgType])))
            print(imageSrc[imgType])
            # print(imageSrc[imgType][0])

            if (len(imageSrc[imgType]) == 0):
                print("NoImage 경우.")
                print(imageSrc[imgType])

                # output.append("NoImage")
                if (imgType == 'tagImg'):
                    tagImg.append("NoImage")
                if (imgType == 'backImg'):
                    backImg.append("NoImage")
            else:

                count = 0

                # print("else length : %d" %len(imageSrc[imgType]))
                # print(imageSrc[imgType])

                for imgs in imageSrc[imgType]:
                    # print("imageSrc in imgs :")
                    print(imgs)

                    if (imgs == '' or imgs == ' '):
                        print("공백임.")
                        # output.append("b'nood\\n'")

                        if (imgType == 'tagImg'):
                            tagImg.append("nood")
                        if (imgType == 'backImg'):
                            backImg.append("nood")
                    else:
                        count = count + 1
                        print("imgSrc count : %d" % count)
                        hdr = {
                            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none',
                            'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}

                        req = urllib.request.Request(imgs, headers=hdr)
                        # response = urllib.request.urlopen(req).read()

                        resp = urllib.request.urlopen(req)
                        info = resp.info()

                        # print(info.get_content_type())
                        # print(info.get_content_maintype())  # -> text
                        print("file type : %s" % (info.get_content_subtype()))

                        if (info.get_content_subtype() == 'jpeg') or (info.get_content_subtype() == 'png'):
                            image = np.asarray(bytearray(resp.read()), dtype="uint8")
                            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                            image = cv2.imencode('.jpg', image)[1].tostring()

                            # output.append(run_inference_on_image(image))
                            if (imgType == 'tagImg'):
                                tagImg.append(run_inference_on_image(image))
                            if (imgType == 'backImg'):
                                backImg.append(run_inference_on_image(image))

                        # print(image)
                        elif info.get_content_subtype() == 'gif':
                            # print("gif file임")

                            img = BytesIO(resp.read())
                            img = Image.open(img)
                            mypalette = img.getpalette()
                            img.putpalette(mypalette)
                            new_im = Image.new("RGBA", img.size)
                            new_im.paste(img)
                            new_im = np.array(new_im)

                            image = cv2.imencode('.jpg', new_im)[1].tostring()

                            # output.append(run_inference_on_image(image))

                            if (imgType == 'tagImg'):
                                tagImg.append(run_inference_on_image(image))
                            if (imgType == 'backImg'):
                                backImg.append(run_inference_on_image(image))

                        #                     response = requests.get(imgs)
                        #                     img = Image.open(BytesIO(response.content))
                        #                     mypalette = img.getpalette()
                        #                     img.putpalette(mypalette)
                        #                     new_im = Image.new("RGBA",img.size)
                        #                     new_im.paste(img)
                        #                     new_im = np.array(new_im)
                        #                     output.append(run_inference_on_image(new_im))

                        else:
                            print("jepg png 아님.")
                            # output.append("b'nood'")
                            if (imgType == 'tagImg'):
                                tagImg.append("nood")
                            if (imgType == 'backImg'):
                                backImg.append("nood")

        # output = ['normal', 'nood', 'gamble']

        # print(imageSrc[0])
        # print('start run_inference_on_image')

        # print('finish run_inference_on_image')

        output = {'tagImg': tagImg, 'backImg': backImg}
        print(output)

        return jsonify(imgs=output)

        # return jsonify(result = output)
        # return render_template('index.html', output=imageSrc)
        # return render_template('index.html', output=output)


def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # return the image
    return image

    # urls = [


#      "https://ssl.pstatic.net/tveta/libs/1240/1240155/1b47a8d4e3229d9531cf_20190510121017466.png",
#      "https://s.pstatic.net/static/newsstand/up/2017/0424/nsd154219877.png"
# ]

# loop over the image URLs
# for url in urls:
#   # download the image URL and display it
#   print ("downloading %s" % (url))
#   image = url_to_image(url)
#   cv2.imshow("Image", image)

# imagePath = url_to_image(url)

##########################################################################################


def create_graph():
    """저장된(saved) GraphDef 파일로부터 graph를 생성하고 saver를 반환한다."""
    # 저장된(saved) graph_def.pb로부터 graph를 생성한다.
    with tf.gfile.GFile(modelFullPath, 'rb') as f:
        print("create_grpah()")
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')
        # print('finish create_graph()')


with tf.device('/gpu:0'):
    def run_inference_on_image(image):
        #    if not tf.gfile.Exists(imagePath):
        #        tf.logging.fatal('File does not exist %s', imagePath)
        #        return answer

        ###############################################################################
        # image_data = tf.gfile.FastGFile(imagePath, 'rb').read()
        # url = "https://ssl.pstatic.net/tveta/libs/1240/1240155/1b47a8d4e3229d9531cf_20190510121017466.png"

        ##############################################################################
        # 저장된(saved) GraphDef 파일로부터 graph를 생성한다.
        # print(type(image_data))
        answer = None

        with tf.Session() as sess:
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            # print('softmax_tensor')
            predictions = sess.run(softmax_tensor,
                                   {'DecodeJpeg/contents:0': image})
            # print('sess.run')

            predictions = np.squeeze(predictions)
            # print('finish squeeze')
            top_k = predictions.argsort()[-5:][::-1]  # 가장 높은 확률을 가진 5개(top 5)의 예측값(predictions)을 얻는다.
            #         f = open(labelsFullPath, 'rb')
            #         #print('finish labelsFullPath open')
            #         lines = f.readlines()
            #         labels = [str(w).replace("\n", "") for w in lines]
            #         for node_id in top_k:
            #             human_string = labels[node_id]
            #             score = predictions[node_id]
            #             print('%s (score = %.5f)' % (human_string, score))

            f = open(labelsFullPath, 'rb')
            #        lines = f.readlines()
            lines = f.read().splitlines()
            labels = [str(w).replace("\n", "") for w in lines]
            #        print(labels)
            for node_id in top_k:
                human_string = labels[node_id]
                human_string = human_string[1:]
                score = predictions[node_id]
                print('%s (score = %.5f)' % (human_string, score))

            answer = labels[top_k[0]][1:]
            answer = answer.replace("'", "")
            print(answer)

            return answer

if __name__ == '__main__':
    # start_time = time.time()
    # app.run(host='0.0.0.0')
    app.run(host='202.31.202.253', port=5000, threaded=False)
    # end_time = time.time()
    # print("WorkingTime: {} sec".format(end_time-start_time))



