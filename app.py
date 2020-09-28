from flask import Flask, render_template, request
from bs4 import BeautifulSoup as bs
import os
import json
import urllib.request
import urllib.parse
import urllib.error
from urllib.request import urlretrieve

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scrapper", methods = ['GET', 'POST'])
def scrapper():
    if request.method == 'POST':
        name = request.form['image_name']
        iters = int(request.form['number'])
        images_with_jpg = []
        files = os.listdir('static')
        for i in files:
            sp = i.split(".")[-1]
            if sp == 'jpg':
                images_with_jpg.append(i)
            else:
                pass
        for i in images_with_jpg:
            try:
                os.remove("./static/" + i)
            except:
                pass
        image_name = name.split()
        image_name = "+".join(image_name)
    
        header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

        url = "https://www.google.co.in/search?q=" + image_name + "&source=lnms&tbm=isch"
        req = urllib.request.Request(url, headers=header)
        resp = urllib.request.urlopen(req)
        respData = resp.read()
        html = bs(respData, 'html.parser')

        imageUrlList = []
        for a in html.find_all("img", {"class": "rg_i"}):
            if a.get("data-src")!=None:
                imageUrlList.append(a.get('data-src'))
        masterListOfImages = []
        count=0

        imageFiles = []
        print(imageUrlList) 
        image_counter=0
        for i, img in enumerate(imageUrlList):

            if (count > iters):
                break
            else:
                count = count + 1
            req = urllib.request.Request(img, headers=header)
                
            urllib.request.urlretrieve(img,"./static/"+image_name+str(image_counter)+".jpg")
            image_counter=image_counter+1
                
            respData = urllib.request.urlopen(req)
            raw_img = respData.read()

            imageFiles.append(raw_img)

        masterListOfImages.append(imageFiles)
        images_with_jpg = []
        files = os.listdir('static')
        for i in files:
            sp = i.split(".")[-1]
            if sp == 'jpg':
                images_with_jpg.append(i)
            else:
                pass
        try:
            if(len(images_with_jpg)>0): 
                return render_template('showImage.html',user_images = images_with_jpg )
            else:
                return "Please try with a different string" 
        except Exception as e:
            print(e)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=False)