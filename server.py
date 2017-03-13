# encoding=utf-8
import os
import web
import json
import base64
import imghdr

web.config.debug = False
render = web.template.render('templates/')


class model:
    """docstring for index"""
    def __init__(self):
        self.errormsg = ['OK', 'Parameter Error', 'Coding Format Error', 'Internal Error', 'Image Error']

    def GET(self):
        result = {}
        xml_filename = 'test.xml'
        img_filename = 'result.png'
        file_path = r'./cache'
        xml_file = os.path.join(file_path, xml_filename)
        img_file = os.path.join(file_path, img_filename)
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
        image = ''
        try:
            image = base64.b64decode(body['imagedata'])
        except Exception, _:
            status = 2
        file = r'./cache/cache.png'
        try:
            with open(file, 'wb') as f:
                f.write(image)
        except Exception, _:
            status = 3
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


urls = ('/', 'upload',
        '/api', 'model')


if __name__ == '__main__':
    app = web.application(urls, globals())
    session = web.session.Session(app, web.session.DiskStore('sessions'))
    app.run()
