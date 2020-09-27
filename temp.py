from functools import wraps
from flask import Flask, render_template, make_response, send_from_directory, request, url_for, redirect, session
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
UPLOADED_FILE_DEST=os.getcwd()+"\\file"
subdest="file"

setusername='admin'
setuserpassword='admin'

@app.route('/delfile/<filename>',methods=['GET','POST'])
@is_login
def delfile(filename):
    if request.method=='GET':
        try:
            file_path=UPLOADED_FILE_DEST+"\\"+filename
            os.remove(file_path)
            isdeled=1
        except BaseException:
            isdeled=0
        finally:
            file_isdir = []
            file_list = os.listdir(UPLOADED_FILE_DEST)
            for i in range(len(file_list)):
                path = UPLOADED_FILE_DEST + "\\" + file_list[i]
                if (os.path.isdir(path)):
                    file_isdir.append(1)
                else:
                    file_isdir.append(0)
            file_dict = dict(zip(file_list, file_isdir))
            file_dict = dict(sorted(file_dict.items(), key=lambda item: item[1], reverse=True))
            file_list = list(file_dict.keys())
            return render_template('index.html', filedict=file_dict, file=file_list, isdel=isdeled)
    if request.method == 'POST':
        f = request.files['file']
        if not f.filename:
            return '''
            <div align='center'>
            <h1>上传文件不能为空</h1>
            <a href="#" onClick="javascript :history.go(-1);">返回上一页</a>
            <a href='/'>返回首页</a>
            </div>
            '''
        file_checklist = os.listdir(UPLOADED_FILE_DEST)
        fname = f.filename
        while (fname in file_checklist):
            filenamelist = fname.split(".")
            filenamelist[0] = filenamelist[0] + "-副本"
            fname = ''
            for i in range(len(filenamelist) - 1):
                fname += filenamelist[i] + "."
            fname += filenamelist[len(filenamelist) - 1]
        upload_path = os.path.join(UPLOADED_FILE_DEST, fname)
        f.save(upload_path)
        file_isdir = []
        file_list = os.listdir(UPLOADED_FILE_DEST)
        for i in range(len(file_list)):
            path = UPLOADED_FILE_DEST + "\\" + file_list[i]
            if (os.path.isdir(path)):
                file_isdir.append(1)
            else:
                file_isdir.append(0)
        file_dict = dict(zip(file_list, file_isdir))
        file_dict=dict(sorted(file_dict.items(),key=lambda item:item[1],reverse=True))
        file_list=list(file_dict.keys())
        return render_template('index.html', filedict=file_dict, file=file_list, isdel=0, isupload=1)
    file_isdir = []
    file_list = os.listdir(UPLOADED_FILE_DEST)
    for i in range(len(file_list)):
        path = UPLOADED_FILE_DEST + "\\" + file_list[i]
        if (os.path.isdir(path)):
            file_isdir.append(1)
        else:
            file_isdir.append(0)
    file_dict = dict(zip(file_list, file_isdir))
    file_dict = dict(sorted(file_dict.items(), key=lambda item: item[1], reverse=True))
    file_list = list(file_dict.keys())
    return render_template('index.html', filedict=file_dict, file=file_list, isdel=0, isupload=0)

@app.route('/subdelfile/<dir>/<filename>',methods=['GET','POST'])
@is_login
def subdelfile(filename,dir):
    if request.method=='GET':
        try:
            file_path=UPLOADED_FILE_DEST+"\\"+dir+"\\"+filename
            os.remove(file_path)
            isdeled=1
        except BaseException:
            isdeled=0
        finally:
            file_isdir = []
            file_list = os.listdir(UPLOADED_FILE_DEST + "\\" + dir)
            for i in range(len(file_list)):
                path = UPLOADED_FILE_DEST + "\\" + dir + "\\" + file_list[i]
                if (os.path.isdir(path)):
                    file_isdir.append(1)
                else:
                    file_isdir.append(0)
            file_dict = dict(zip(file_list, file_isdir))
            file_dict = dict(sorted(file_dict.items(), key=lambda item: item[1], reverse=True))
            file_list = list(file_dict.keys())
            url_list = dir.split("\\")
            if (len(url_list) == 1):
                preurl = "/"
            else:
                preurl = '/subdir/'
                for i in range(len(url_list) - 2):
                    preurl += url_list[i] + "%5C"
                preurl += url_list[len(url_list) - 2]
            return render_template('index.html', filedict=file_dict, file=file_list, isdel=isdeled, issub=1, curdir=dir,pre=preurl)
    if request.method == 'POST':
        f = request.files['file']
        if not f.filename:
            return '''
            <div align='center'>
            <h1>上传文件不能为空</h1>
            <a href="#" onClick="javascript :history.go(-1);">返回上一页</a>
            <a href='/'>返回首页</a>
            </div>
            '''
        file_checklist = os.listdir(UPLOADED_FILE_DEST+"\\"+dir)
        fname = f.filename
        while (fname in file_checklist):
            filenamelist = fname.split(".")
            filenamelist[0] = filenamelist[0] + "-副本"
            fname = ''
            for i in range(len(filenamelist) - 1):
                fname += filenamelist[i] + "."
            fname += filenamelist[len(filenamelist) - 1]
        upload_path = os.path.join(UPLOADED_FILE_DEST,dir,fname)
        f.save(upload_path)
        file_isdir = []
        file_list = os.listdir(UPLOADED_FILE_DEST + "\\" + dir)
        for i in range(len(file_list)):
            path = UPLOADED_FILE_DEST + "\\" + dir + "\\" + file_list[i]
            if (os.path.isdir(path)):
                file_isdir.append(1)
            else:
                file_isdir.append(0)
        file_dict = dict(zip(file_list, file_isdir))
        file_dict=dict(sorted(file_dict.items(),key=lambda item:item[1],reverse=True))
        file_list=list(file_dict.keys())
        url_list = dir.split("\\")
        if (len(url_list) == 1):
            preurl = "/"
        else:
            preurl = '/subdir/'
            for i in range(len(url_list) - 2):
                preurl += url_list[i] + "%5C"
            preurl += url_list[len(url_list) - 2]
        return render_template('index.html', filedict=file_dict, file=file_list, isdel=0, issub=1, curdir=dir,pre=preurl,isupload=1)
    file_isdir = []
    file_list = os.listdir(UPLOADED_FILE_DEST + "\\" + dir)
    for i in range(len(file_list)):
        path = UPLOADED_FILE_DEST + "\\" + dir + "\\" + file_list[i]
        if (os.path.isdir(path)):
            file_isdir.append(1)
        else:
            file_isdir.append(0)
    file_dict = dict(zip(file_list, file_isdir))
    file_dict = dict(sorted(file_dict.items(), key=lambda item: item[1], reverse=True))
    file_list = list(file_dict.keys())
    url_list = dir.split("\\")
    if (len(url_list) == 1):
        preurl = "/"
    else:
        preurl = '/subdir/'
        for i in range(len(url_list) - 2):
            preurl += url_list[i] + "%5C"
        preurl += url_list[len(url_list) - 2]
    return render_template('index.html', filedict=file_dict, file=file_list, isdel=0, issub=1, curdir=dir, pre=preurl,isupload=0)