#!/usr/bin/env python
import web
web.config.debug = False
import os
import time
import config
from urllib import quote
import simplejson as json
# load config file
root = config.root

types = [
    ".h",".cpp",".cxx",".cc",".c",".cs",".html",".js",
    ".php",".java",".py",".rb",".as",".jpeg",".jpg",".png",
    ".gif",".ai",".psd",".mp3",".avi",".rmvb",".mp4",".wmv",
    ".mkv",".doc",".docx",".ppt",".pptx",".xls",".xlsx",
    ".zip",".tar",".gz",".7z",".rar",".pdf",".txt",".exe",
    ".apk"
]

render = web.template.render('template')

urls = (
    '/login','Login',
    '/search','Search',
    '/favicon.ico',"Ico",
    '/(.*)','Index',
)
app = web.application(urls, globals())
web.config.session_parameters['timeout'] = 60*24*60
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'isLogin': 0})
    web.config._session = session
else:
    session = web.config._session
def session_hook():
    web.ctx.session = session
app.add_processor(web.loadhook(session_hook))
def logged():
    if session.isLogin == 1:
        return True
    else:
        return False
    
class Login:
    def GET(self):
        if logged():
            web.seeother('/')
        else:
            return render.login()
    def POST(self):
        data = web.input()
        admin_name, admin_password = data.get('admin_name'), data.get('admin_psw')
        if admin_name == config.admin_name and admin_password == config.admin_password:
            session.isLogin = 1
            web.seeother('/')
        else:
            session.isLogin = 0
            return render.login()
def admin_required(func):
    def Function(*args, **kargs):
        if not session.isLogin:
            return json.dumps({"flag":0})
        else:
            return func(*args, **kargs)
    return Function

class Ico:
    def GET(self):
        return open("static/img/favicon.ico").read()
class Search:
    def POST(self):
        search_content =  web.input()["search-dash"]
        print search_content
        try:
            web.header('Content-Type','application/octet-stream')
            web.header('Content-disposition', 'attachment; filename=%s' % search_content)
            file = open(os.path.join(root,search_content))
            size = os.path.getsize(os.path.join(root,search_content))
            web.header('Content-Length','%s' % size)
            return file.read()
        except:
            raise web.seeother("/")
class Index:
    def GET(self,path):
        if path == '':
            list = []
            item = os.listdir(root)
            item = sorted(item, key = str.lower)
            
            for i in item:
                if i[0] == '.' or os.path.isdir(root + i):
                    continue
                temp = {}
                temp['name'] = i
                temp['type'] = '.' + i.split('.')[-1]
                
                try:
                    types.index(temp['type'])
                except:
                    temp['type'] = "general"

                temp["time"] = time.strftime("%H:%M:%S %Y-%m-%d",
                        time.localtime(os.path.getmtime(root + i))) 
                
                size = os.path.getsize(os.path.join(root,i))
                if size < 1024:
                    size = str(size) + ".0 B"
                elif size < 1024 * 1024:
                    size = "%0.1f KB" % (size/1024.0)
                elif size < 1024 * 1024 * 1024:
                    size = "%0.1f MB" % (size/1024.0/1024.0)
                else :
                    size = "%0.1f GB" % (size/1024.0/1024.0/1024.0)
                
                temp["size"] = size
                temp["encode"] = quote(i)

                list.append(temp)
            
            return render.layout(list) 
        
        else:
            web.header('Content-Type','application/octet-stream')
            web.header('Content-disposition', 'attachment; filename=%s' % path)
            file = open(os.path.join(root,path))
            size = os.path.getsize(os.path.join(root,path))
            web.header('Content-Length','%s' % size)
            return file.read()
    @admin_required
    def DELETE(self,filename):
        try:
            os.remove(os.path.join(root,filename))
            return json.dumps({"flag":1})
        except:
            return json.dumps({"flag":1})

    def POST(self,filename):
        x = web.input(file={})
        if 'file' in x:
            try:
                filepath= x.file.filename.replace('\\','/')     # replaces the windows-style slashes with linux ones.
                filename = filepath.split('/')[-1]              # splits the and chooses the last part (the filename with extension)
                fout = open(os.path.join(root,filename),'w')    # creates the file where the uploaded file should be stored
                fout.write(x.file.file.read())                  # writes the uploaded file to the newly created file.
                fout.close()                                    # closes the file, upload complete.
            except:
                pass
        return "<script>parent.location.reload()</script>"
     
#if __name__ == "__main__":
    #app = web.application(urls, globals())
    #app.run()

application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
    
