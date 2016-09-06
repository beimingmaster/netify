# Copyright 2015 Curtis Sand
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

"""Flask view objects for the netify app."""

from enum import Enum

from flask.ext.classy import FlaskView
from yattag import Doc

from .template import HtmlPage
from .template import build_debug_div


class HelloWorldIndex(FlaskView):
    """The index view."""
    name = 'index'
    route_base = '/'
    netify_app = None

    @classmethod
    def register(cls, netify_app, **kwargs):
        """Register this view against the Netify Web Application."""
        cls.netify_app = netify_app
        super(HelloWorldIndex, cls).register(netify_app.flask_app, **kwargs)

    def index(self):
        """Handle an incoming request for a route registered to this View."""
        hello_world = 'Hello World From Netify'
        view_opts = self.netify_app.config.get_page_options(self.name)
        if 'debug' not in view_opts:
            body_txt = hello_world
        else:  # add the debug div to the bottom of the page
            body = Doc()
            body.text(hello_world)
            body.stag('hr')
            body.asis(build_debug_div(self.netify_app))
            body_txt = body.getvalue()
        return HtmlPage(head=None, body=body_txt).render_template()


class Views(Enum):
    """Enum of view classes available in this module."""
    hello_world_index = HelloWorldIndex
