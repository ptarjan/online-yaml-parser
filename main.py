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
import json
import yaml
import pprint
import urllib.request

from django_jsonencoder import DjangoJSONEncoder

from jinja2 import Environment, FileSystemLoader

import webapp2

# Set up Jinja2 environment
jinja_env = Environment(
    loader=FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True
)

examples = []
prefix = os.path.join(os.path.dirname(__file__), "examples")
for ex in sorted(os.listdir(prefix)):
    with open(os.path.join(prefix, ex)) as f:
        examples.append(f.read())

default_yaml = """
- just: write some
- yaml: 
  - [here, and]
  - {it: updates, in: real-time}
"""

def getOutput(y, type):
    try:
        objects = yaml.safe_load(y)
        if type == "python":
            return pprint.pformat(objects)
        elif type == "canonical_yaml":
            return yaml.dump(objects, canonical=True)
        else:  # type == "json"
            return json.dumps(objects, cls=DjangoJSONEncoder, indent=2)
    except Exception as why:
        return "ERROR:\n\n" + str(why)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        y = self.request.get("yaml", default_yaml)
        url = self.request.get("url")
        url_error = None
        if url:
            try:
                response = urllib.request.urlopen(url)
                y = response.read()
                if isinstance(y, bytes):
                    y = y.decode('utf-8')
            except Exception as e:
                url_error = f"Failed to download URL: {str(e)}"
        type = self.request.get("type", "json")

        output = getOutput(y, type)
        template_values = {}
        template_values['output'] = output
        template_values['yaml'] = y
        template_values['examples'] = examples
        template_values['type'] = type
        template_values['url'] = url
        template_values['url_error'] = url_error

        template = jinja_env.get_template('index.html')
        self.response.write(template.render(template_values))

    def post(self):
        return self.get()

class AjaxHandler(webapp2.RequestHandler):
    def get(self):
        y = self.request.get("yaml")
        type = self.request.get("type", "json")
        output = getOutput(y, type)

        response = json.dumps(output)
        cb = self.request.get("callback")
        if cb:
            response = cb + "(" + response + ")"

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(response)

    def post(self):
        return self.get()

class FaviconHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect("https://pyyaml.org/favicon.ico")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/ajax', AjaxHandler),
    ('/favicon.ico', FaviconHandler),
])
