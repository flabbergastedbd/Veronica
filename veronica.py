#!/usr/bin/python
# coding: utf-8
"""
Veronica is the main component that manages dashboard and listens for
events relaying them accordingly

Copyright © 2016 Bharadwaj Machiraju <https://blog.tunnelshade.in> <name.surname@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import uuid
import tornado.gen
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.template

from config import V_MODULES


class RootHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        module = self.get_argument('module', None)
        if module == None:
            self.render('index.html', V_MODULES=V_MODULES)
        elif V_MODULES.get(module, None):
            proc = tornado.process.Subprocess(
				V_MODULES[module]['command'].split(),
				cwd=os.path.join(ROOT_DIR, 'scripts'),
				stdout=tornado.process.Subprocess.STREAM)
            result = yield proc.stdout.read_until_close()
            self.write(result)


if __name__ == "__main__":
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_DIR = os.path.join(ROOT_DIR, 'templates')

    args = sys.argv
    tornado.options.parse_command_line(args)

    application = tornado.web.Application([
        (r'/', RootHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(ROOT_DIR, 'static')}),
    ], template_path=TEMPLATE_DIR, debug=True)
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
