import base64
import numpy as np
import io
from PIL import Image
import keras
from keras import backend as K
from keras.models import Sequential
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from flask import request
from flask import jsonify
from flask import Flask
import tensorflow as tf
import mysql.connector
import datetime

app=Flask(__name__)
#PORT = os.environ['PORT']
#app.run(host = "0.0.0.0", port=PORT, debig = True, reloader=True)
#CREATE TABLE IF NOT EXISTS WEEK (date VARCHAR(255),num INTEGER(99)) DEFAULT CHARSET=utf8;
def Create_db():
    cursor.execute("CREATE DATABASE maxdb")
    return

def Create_table(week_):
    try:
        cursor.execute("SELECT * FROM users" + week_)
    except:
        cursor.execute("CREATE TABLE IF NOT EXISTS users" + week_ + "(name VARCHAR(255), student_id VARCHAR(255), attend INTEGER(99)) DEFAULT CHARSET=utf8")
        students = [('王郁琪', 'f', 0),('邱百纓', 'f', 0),
                    ('簡丞珮', 'f', 0),('張語恩', 'f', 0),
                    ('何奕萱', 'f', 0),('倪國勛', 'f', 0),
                    ('吳偵平', 'f', 0),('林亭伃', 'f', 0),
                    ('梁致綜', 'f', 0),('賴柏瑜', 'f', 0),
                    ('林辰臻', 'f', 0),('黃威翔', 'f', 0),
                    ('蔡柏垣', 'f', 0),('潘荏羽', 'f', 0),
                    ('曾韻如', 'f', 0),('柳孟芸', 'f', 0),
                    ('陳軒翊', 'f', 0),('張祐禎', 'f', 0),
                    ('王聖中', 'f', 0),('林家緯', 'f', 0),
                    ('王宏偉', 'f', 0),('洪培軒', 'f', 0),
                    ('宋金操', 'f', 0),('郭彥松', 'f', 0),
                    ('黃俊豪', 'f', 0),('林郁松', 'f', 0),
                    ('張財實', 'f', 0),('陳彥達', 'f', 0),
                    ('林禹辰', 'f', 0),('黃瑞連', 'f', 0),
                    ('吳郁晨', 'f', 0),('陳香君', 'f', 0),
                    ('陳昱霖', 'f', 0),('蔡明修', 'f', 0),
                    ('林鴻諭', 'f', 0),]
        Insert_Multiple_Records(students,week_)

        sqlStuff_week = "INSERT INTO WEEK (date, num) VALUES (%s,%s)"
        tmp=[(week_, 0)]
        cursor.executemany(sqlStuff_week,tmp)
        maxdb.commit()

    return


def Insert_Multiple_Records(records,week_):
    sqlStuff = "INSERT INTO users" + week_ + "(name, student_id, attend) VALUES (%s,%s,%s)"
    cursor.executemany(sqlStuff, records)
    maxdb.commit()

    return

def Read_table(week_):
    #cursor.execute("SELECT * FROM users Where name Like 'A%'")
    #if want to print all users
    cursor.execute("SELECT * FROM users" + week_)
    result = cursor.fetchall()
    for row in result:
        print(row)
    return

def Update_table(name_, week_,attend_):
    name_ = '\'' + name_ + '\''
    #attend_ = '\'' + attend_ + '\''
    update_users = "UPDATE users" + week_ + " SET attend = " + attend_ + " WHERE name = " + name_
    print(update_users)
    cursor.execute(update_users)
    maxdb.commit()
    return

def Delete_a_person(name_):
    name_ = '\'' + name_ + '\''
    i = 0
    while i <= 20:
        delete_users = "DELETE FROM users" + str(i) + "WHERE name = " + name_
        cursor.execute(delete_users)
        maxdb.commit()
        i = i+1
    return

def Delete_drpo_table(week_):
    delete_table = "DROP TABLE IF EXISTS users" + week_
    cursor.execute(delete_table)
    return

def get_model():
    global model
    model=load_model('37_best.h5')
    global graph
    graph = tf.get_default_graph()
    print('Model loaded!')

def preprocess_image(image):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image=image.resize((300,300))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    return image

def most_possible_prediction(response):
    max=-1.0
    result = -1
    for i in range(0, 35):
        if max < response['predictions'][str(i)]:
            max = response['predictions'][str(i)]
            result = i
    return result

print("Loading Keras Model...")
get_model()

maxdb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="ROOT",
    database="maxdb"
)
cursor = maxdb.cursor(buffered=True)


@app.route("/index",methods=["POST"])
def predict():
    message=request.get_json(force=True)

    if list(message.keys())[0] == "image":
        print("+++message++")
        encoded=message['image']
        decoded=base64.b64decode(encoded)
        image=Image.open(io.BytesIO(decoded))
        processed_image=preprocess_image(image)
        with graph.as_default():
            prediction = model.predict(processed_image).tolist()

        dict_name = {0: '王郁琪', 1: '邱百纓', 2: '簡丞珮', 3: '張語恩', 4: '何奕萱'
            , 5: '倪國勛', 6: '吳偵平', 7: '林亭伃', 8: '梁致綜', 9: '林辰臻'
            ,10: '黃威翔', 11: '蔡柏垣', 12: '潘荏羽', 13: '柳孟芸', 14: '曾韻如'
            , 15: '張祐禎', 16: '林鴻諭', 17: '王聖中', 18: '林家緯', 19: '陳軒翊'
            , 20: '王宏偉', 21: '洪培軒', 22: '賴柏瑜', 23: '陳昱霖', 24: '郭彥松'
            , 25: '黃俊豪', 26: '林郁松', 27: '宋金操', 28: '張財實', 29: '陳彥達'
            , 30: '林禹辰', 31: '黃瑞連', 32: '吳郁晨', 33: '陳香君', 34: '蔡明修'}
        print(prediction)
        response={
            'predictions':{
                '0': prediction[0][0], '1': prediction[0][1],
                '2': prediction[0][2], '3': prediction[0][3],
                '4': prediction[0][4], '5': prediction[0][5],
                '6': prediction[0][6], '7': prediction[0][7],
                '8': prediction[0][8], '9': prediction[0][9],
                '10': prediction[0][10], '11': prediction[0][11],
                '12': prediction[0][12], '13': prediction[0][13],
                '14': prediction[0][14], '15': prediction[0][15],
                '16': prediction[0][16], '17': prediction[0][17],
                '18': prediction[0][18], '19': prediction[0][19],
                '20': prediction[0][20], '21': prediction[0][21],
                '22': prediction[0][22], '23': prediction[0][23],
                '24': prediction[0][24], '25': prediction[0][25],
                '26': prediction[0][26], '27': prediction[0][27],
                '28': prediction[0][28], '29': prediction[0][29],
                '30': prediction[0][30], '31': prediction[0][31],
                '32': prediction[0][32], '33': prediction[0][33],
                '34': prediction[0][34]
            }
        }

        print(prediction)
        result=dict_name[most_possible_prediction(response)]

        return jsonify(result)

    elif list(message.keys())[0] == 'date':
        print("+++date++")
        str_list = []
        cursor.execute("SELECT * FROM WEEK Where num Like '0%'")
        result = cursor.fetchall()
        for row in result:
            print('week ', row)
            str_list.append(row)
            cursor.execute("SELECT * FROM users" + row[0])
            result2 = cursor.fetchall()

            for row2 in result2:
                print('users ', row2)
                str_list.append(row2)
        print(str_list)
        return jsonify(str_list)

    else:
        print("+++angel++")
        time_now = datetime.datetime.now()
        week = str(time_now.year) + str(time_now.month) + str(time_now.day)
        Create_table(week)
        for i in range(0,len(message)):
            Update_table(list(message.keys())[i], week, list(message.values())[i])

        Read_table(week)
        return jsonify('ok')

    return jsonify('err')
    


