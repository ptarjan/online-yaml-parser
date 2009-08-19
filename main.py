#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

import yaml
import simplejson

import wsgiref.handlers
from django_jsonencoder import DjangoJSONEncoder

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

examples = []
prefix = os.path.join(os.path.dirname(__file__), "examples")
for ex in sorted(os.listdir(prefix)) :
    examples.append(file(os.path.join(prefix, ex)).read())

class MainHandler(webapp.RequestHandler):
    def get(self):
        template_values = {}
        y = self.request.get("yaml")

        type = self.request.get("type", "json")
        try :
            objects = yaml.load(y)
            if type == "json" :
                output = simplejson.dumps(objects, cls=DjangoJSONEncoder, indent=2)
            elif type == "python" :
                output = str(objects)
        except Exception, why :
            output = "ERROR:\n\n" + str(why)

        template_values['output'] = output
        template_values['yaml'] = y
        template_values['examples'] = examples
        template_values['type'] = type

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

    def post(self) :
        return self.get()

def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
