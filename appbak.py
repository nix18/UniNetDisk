from functools import wraps
from flask import Flask, render_template, make_response, send_from_directory, request, url_for, redirect, session
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
UPLOADED_FILE_DEST = os.getcwd() + "/file"
subdest = "file"

setusername = 'admin'
setuserpassword = 'admin'


def is_login(func):
    @wraps(func)
    def check_login(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('new_login'))

    return check_login


@app.route('/new_login/', methods=['GET', 'POST'])
def new_login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if username == setusername and password == setuserpassword:
            session['user_id'] = 1
            session.permanent = True
            return redirect((url_for('mainpage')))
        else:
            return render_template('login.html', loginfail=1)


@app.route('/logout')
def logout():
    print(session.get('username'))
    session.clear()
    print(session.get('username'))
    return '''
     <div align='center'>
            <h1>登出成功</h1>
            <a href='/'>返回首页</a>
            </div>
     '''


@app.route('/mainpage', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
@is_login
def mainpage():
    if request.method == 'GET':
        file_isdir = []
        file_list = os.listdir(UPLOADED_FILE_DEST)
        for i in range(len(file_list)):
            path = UPLOADED_FILE_DEST + "/" + file_list[i]
            if (os.path.isdir(path)):
                file_isdir.append(1)
            else:
                file_isdir.append(0)
        file_dict = dict(zip(file_list, file_isdir))
        file_dict = dict(sorted(file_dict.items(), key=lambda item: item[1], reverse=True))
        file_list = list(file_dict.keys())
        return render_template('index.html', filedict=file_dict, file=file_list, isdel=0)
    if request.method == 'POST':
        f = request.files['file']
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
            path = UPLOADED_FILE_DEST + "/" + file_list[i]
            if (os.path.isdir(path)):
                file_isdir.append(1)
            else:
                file_isdir.append(0)
        file_dict = dict(zip(file_list, file_isdir))
        file_dict = dict(sorted(file_dict.items(), key=lambda item: item[1], reverse=True))
        file_list = list(file_dict.keys())
        return render_template('index.html', filedict=file_dict, file=file_list, isdel=0, isupload=1)
    file_isdir = []
    file_list = os.listdir(UPLOADED_FILE_DEST)
    for i in range(len(file_list)):
        path = UPLOADED_FILE_DEST + "/" + file_list[i]
        if (os.path.isdir(path)):
            file_isdir.append(1)
        else:
            file_isdir.append(0)
    file_dict = dict(zip(file_list, file_isdir))
    file_dict = dict(sorted(file_dict.items(), key=lambda item: item[1], reverse=True))
    file_list = list(file_dict.keys())
    return render_template('index.html', filedict=file_dict, file=file_list, isdel=0, isupload=0)


@app.route('/subdir/<dir>', methods=['POST', 'GET'])
@is_login
def subdir(dir):
    inidir = dir
    dir = dir.replace('--', '/')
    if request.method == 'GET':
        file_isdir = []
        file_list = os.listdir(UPLOADED_FILE_DEST + "/" + dir)
        for i in range(len(file_list)):
            path = UPLOADED_FILE_DEST + "/" + dir + "/" + file_list[i]
            if (os.path.isdir(path)):
                file_isdir.append(1)
            else:
                file_isdir.append(0)
        file_dict = dict(zip(file_list, file_isdir))
        file_dict = dict(sorted(file_dict.items(), key=lambda item: item[1], reverse=True))
        file_list = list(file_dict.keys())
        url_list = dir.split("/")
        if (len(url_list) == 1):
            preurl = "/"
        else:
            preurl = '/subdir/'
            for i in range(len(url_list) - 2):
                preurl += url_list[i] + "--"
            preurl += url_list[len(url_list) - 2]
        return render_template('index.html', filedict=file_dict, file=file_list, isdel=0, issub=1, curdir=inidir,
                               pre=preurl)
    if request.method == 'POST':
        f = request.files['file']
        file_checklist = os.listdir(UPLOADED_FILE_DEST + "/" + dir)
        fname = f.filename
        while (fname in file_checklist):
            filenamelist = fname.split(".")
            filenamelist[0] = filenamelist[0] + "-副本"
            fname = ''
            for i in range(len(filenamelist) - 1):
                fname += filenamelist[i] + "."
            fname += filenamelist[len(filenamelist) - 1]
        upload_path = os.path.join(UPLOADED_FILE_DEST, dir, fname)
        f.save(upload_path)
        file_isdir = []
        file_list = os.listdir(UPLOADED_FILE_DEST + "/" + dir)
        for i in range(len(file_list)):
            path = UPLOADED_FILE_DEST + "/" + dir + "/" + file_list[i]
            if (os.path.isdir(path)):
                file_isdir.append(1)
            else:
                file_isdir.append(0)
        file_dict = dict(zip(file_list, file_isdir))
        file_dict = dict(sorted(file_dict.items(), key=lambda item: item[1], reverse=True))
        file_list = list(file_dict.keys())
        url_list = dir.split("/")
        if (len(url_list) == 1):
            preurl = "/"
        else:
            preurl = '/subdir/'
            for i in range(len(url_list) - 2):
                preurl += url_list[i] + "--"
            preurl += url_list[len(url_list) - 2]
        return render_template('index.html', filedict=file_dict, file=file_list, isdel=0, issub=1, curdir=inidir,
                               pre=preurl, isupload=1)
    file_isdir = []
    file_list = os.listdir(UPLOADED_FILE_DEST + "/" + dir)
    for i in range(len(file_list)):
        path = UPLOADED_FILE_DEST + "/" + dir + "/" + file_list[i]
        if (os.path.isdir(path)):
            file_isdir.append(1)
        else:
            file_isdir.append(0)
    file_dict = dict(zip(file_list, file_isdir))
    file_dict = dict(sorted(file_dict.items(), key=lambda item: item[1], reverse=True))
    file_list = list(file_dict.keys())
    url_list = dir.split("/")
    if (len(url_list) == 1):
        preurl = "/"
    else:
        preurl = '/subdir/'
        for i in range(len(url_list) - 2):
            preurl += url_list[i] + "--"
        preurl += url_list[len(url_list) - 2]
    return render_template('index.html', filedict=file_dict, file=file_list, isdel=0, issub=1, curdir=inidir, pre=preurl,
                           isupload=0)


@app.route('/delfile/<filename>', methods=['GET', 'POST'])
@is_login
def delfile(filename):
    if request.method == 'GET':
        try:
            file_path = UPLOADED_FILE_DEST + "/" + filename
            os.remove(file_path)
            isdeled = 1
        except BaseException:
            isdeled = 0
        finally:
            file_isdir = []
            file_list = os.listdir(UPLOADED_FILE_DEST)
            for i in range(len(file_list)):
                path = UPLOADED_FILE_DEST + "/" + file_list[i]
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
            path = UPLOADED_FILE_DEST + "/" + file_list[i]
            if (os.path.isdir(path)):
                file_isdir.append(1)
            else:
                file_isdir.append(0)
        file_dict = dict(zip(file_list, file_isdir))
        file_dict = dict(sorted(file_dict.items(), key=lambda item: item[1], reverse=True))
        file_list = list(file_dict.keys())
        return render_template('index.html', filedict=file_dict, file=file_list, isdel=0, isupload=1)
    file_isdir = []
    file_list = os.listdir(UPLOADED_FILE_DEST)
    for i in range(len(file_list)):
        path = UPLOADED_FILE_DEST + "/" + file_list[i]
        if (os.path.isdir(path)):
            file_isdir.append(1)
        else:
            file_isdir.append(0)
    file_dict = dict(zip(file_list, file_isdir))
    file_dict = dict(sorted(file_dict.items(), key=lambda item: item[1], reverse=True))
    file_list = list(file_dict.keys())
    return render_template('index.html', filedict=file_dict, file=file_list, isdel=0, isupload=0)


@app.route('/subdelfile/<dir>/<filename>', methods=['GET', 'POST'])
@is_login
def subdelfile(filename, dir):
    inidir = dir
    dir = dir.replace('--', '/')
    if request.method == 'GET':
        try:
            file_path = UPLOADED_FILE_DEST + "/" + dir + "/" + filename
            os.remove(file_path)
            isdeled = 1
        except BaseException:
            isdeled = 0
        finally:
            file_isdir = []
            file_list = os.listdir(UPLOADED_FILE_DEST + "/" + dir)
            for i in range(len(file_list)):
                path = UPLOADED_FILE_DEST + "/" + dir + "/" + file_list[i]
                if (os.path.isdir(path)):
                    file_isdir.append(1)
                else:
                    file_isdir.append(0)
            file_dict = dict(zip(file_list, file_isdir))
            file_dict = dict(sorted(file_dict.items(), key=lambda item: item[1], reverse=True))
            file_list = list(file_dict.keys())
            url_list = dir.split("/")
            if (len(url_list) == 1):
                preurl = "/"
            else:
                preurl = '/subdir/'
                for i in range(len(url_list) - 2):
                    preurl += url_list[i] + "--"
                preurl += url_list[len(url_list) - 2]
            return render_template('index.html', filedict=file_dict, file=file_list, isdel=isdeled, issub=1, curdir=inidir,
                                   pre=preurl)
    if request.method == 'POST':
        f = request.files['file']
        file_checklist = os.listdir(UPLOADED_FILE_DEST + "/" + dir)
        fname = f.filename
        while (fname in file_checklist):
            filenamelist = fname.split(".")
            filenamelist[0] = filenamelist[0] + "-副本"
            fname = ''
            for i in range(len(filenamelist) - 1):
                fname += filenamelist[i] + "."
            fname += filenamelist[len(filenamelist) - 1]
        upload_path = os.path.join(UPLOADED_FILE_DEST, dir, fname)
        f.save(upload_path)
        file_isdir = []
        file_list = os.listdir(UPLOADED_FILE_DEST + "/" + dir)
        for i in range(len(file_list)):
            path = UPLOADED_FILE_DEST + "/" + dir + "/" + file_list[i]
            if (os.path.isdir(path)):
                file_isdir.append(1)
            else:
                file_isdir.append(0)
        file_dict = dict(zip(file_list, file_isdir))
        file_dict = dict(sorted(file_dict.items(), key=lambda item: item[1], reverse=True))
        file_list = list(file_dict.keys())
        url_list = dir.split("/")
        if (len(url_list) == 1):
            preurl = "/"
        else:
            preurl = '/subdir/'
            for i in range(len(url_list) - 2):
                preurl += url_list[i] + "--"
            preurl += url_list[len(url_list) - 2]
        return render_template('index.html', filedict=file_dict, file=file_list, isdel=0, issub=1, curdir=inidir,
                               pre=preurl, isupload=1)
    file_isdir = []
    file_list = os.listdir(UPLOADED_FILE_DEST + "/" + dir)
    for i in range(len(file_list)):
        path = UPLOADED_FILE_DEST + "/" + dir + "/" + file_list[i]
        if (os.path.isdir(path)):
            file_isdir.append(1)
        else:
            file_isdir.append(0)
    file_dict = dict(zip(file_list, file_isdir))
    file_dict = dict(sorted(file_dict.items(), key=lambda item: item[1], reverse=True))
    file_list = list(file_dict.keys())
    url_list = dir.split("/")
    if (len(url_list) == 1):
        preurl = "/"
    else:
        preurl = '/subdir/'
        for i in range(len(url_list) - 2):
            preurl += url_list[i] + "--"
        preurl += url_list[len(url_list) - 2]
    return render_template('index.html', filedict=file_dict, file=file_list, isdel=0, issub=1, curdir=inidir, pre=preurl,
                           isupload=0)


@app.route('/download/<filename>')
@is_login
def download(filename):
    response = make_response(send_from_directory(UPLOADED_FILE_DEST, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response


@app.route('/subdownload/<dir>/<filename>')
@is_login
def subdownload(filename, dir):
    response = make_response(send_from_directory(UPLOADED_FILE_DEST + "/" + dir, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response


@app.route('/mkdir', methods=['GET', 'POST'])
@is_login
def mkdir():
    if request.method == 'GET':
        return render_template('mkdir.html')
    else:
        dirname = request.values.get('dirname')
        print(dirname)
        dirpath = os.path.join(UPLOADED_FILE_DEST, dirname)
        isExists = os.path.exists(dirpath)
        if not isExists:
            os.makedirs(dirpath.encode('utf-8'))
            return redirect('/')
        else:
            return '''
            <div align='center'>
            <h1>文件夹已存在，创建失败</h1>
            <a href="#" onClick="javascript :history.go(-1);">返回上一页</a>
            <a href='/'>返回首页</a>
            </div>
            '''


@app.route('/submkdir/<dir>', methods=['GET', 'POST'])
@is_login
def submkdir(dir):
    inidir = dir
    dir = dir.replace('--', '/')
    if request.method == 'GET':
        return render_template('mkdir.html', curdir=dir)
    else:
        dirname = request.values.get('dirname')
        print(dirname)
        dirpath = os.path.join(UPLOADED_FILE_DEST, dir, dirname)
        isExists = os.path.exists(dirpath)
        if not isExists:
            os.makedirs(dirpath.encode('utf-8'))
            return redirect(url_for('subdir', dir=inidir))
        else:
            return '''
            <div align='center'>
            <h1>文件夹已存在，创建失败</h1>
            <a href="#" onClick="javascript :history.go(-1);">返回上一页</a>
            <a href='/'>返回首页</a>
            </div>
            '''


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8099)
