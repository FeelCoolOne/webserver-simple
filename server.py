# encoding=utf-8
import os
import web
import json
import base64
import imghdr
import subprocess
import traceback


web.config.debug = False
render = web.template.render('templates/')


class model:
    """docstring for index"""
    def __init__(self):
        self.errormsg = ['OK', 'Parameter Error', 'Coding Format Error', 'Internal Error', 'Image Error']
        self.xml_file_path = './cache/xml'
        # self.img_file_path = './cache/img'
        self.img_file_path = './cache'
        self.cache_dir = './cache'

    def GET(self):
        orderno = web.input(orderno='0').orderno
        result = {}
        xml_file = os.path.join(self.xml_file_path, '{0}.xml'.format(orderno))
        img_file = os.path.join(self.img_file_path, '{0}.png'.format(orderno))
        if os.path.isfile(xml_file) is True and os.path.isfile(img_file) is True:
            with open(xml_file, 'r') as f:
                result['xml'] = f.read()
            with open(img_file, 'rb') as f:
                result['imagedata'] = base64.b64encode(f.read())
        else:
            result['xml'] = self.unfinishedXML()
            result['imagedata'] = ''
        return json.dumps(result)

    def unfinishedXML(self):
        root = """<?xml version="1.0" encoding="utf-8"?>\n"""
        root += u"""<root><errorcode>1</errorcode></root>"""
        return root

    def POST(self):
        body = json.loads(web.data())
        status = 0
        if 'imagedata' not in body or 'orderno' not in body:
            status = 1
            return json.dumps({'errorcode': status, 'errormsg': self.errormsg[status]})
        image = ''
        try:
            image = base64.b64decode(body['imagedata'])
        except Exception, _:
            status = 2
            return json.dumps({'errorcode': status, 'errormsg': self.errormsg[status]})
        orderno = body['orderno']
        file = '{0}/{1}.png'.format(self.cache_dir, orderno)
        try:
            with open(file, 'wb') as f:
                f.write(image)
            subprocess.Popen(['python', 'output.py', orderno])
        except Exception, _:
            status = 3
            return json.dumps({'errorcode': status, 'errormsg': self.errormsg[status]})
        if imghdr.what(file) is None:
            status = 4
        return json.dumps({'errorcode': status, 'errormsg': self.errormsg[status]})


class upload:
    """docstring for index"""

    def GET(self):
        '''return render.index(name)'''
        return """<html><head></head><body>
                  <form method="POST" enctype="multipart/form-data" action="">
                  <input type="file" name="myfile" />
                  <br/>
                  <input type="submit" />
                  </form>
                  </body></html>"""

    def POST(self):
        x = web.input(myfile={})
        # web.debug(x['myfile'].filename)
        # web.debug(x['myfile'].value)
        # web.debug(x['myfile'].file.read())
        with open('./cache/cache.png', 'wb') as f:
            f.write(x['myfile'].value)
        return 'OK'


class cache_clean:

    def GET(self):
        try:
            os.chdir('./cache/xml')
            for xml in os.listdir('.'):
                os.remove(xml)
        except Exception, e:
            traceback.print_exc()
            return '{0}'.format(e)
        os.chdir('../..')
        return 'OK'


urls = ('/', 'upload',
        '/api', 'model',
        '/clear', 'cache_clean')



if __name__ == '__main__':
    app = web.application(urls, globals())
    session = web.session.Session(app, web.session.DiskStore('sessions'))
    app.run()
