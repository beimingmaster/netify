"""The netify application object."""
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
import abc

from flask import Flask

from .view import Views
from .config import Config


class UwsgiMixin(object):
    """A mixin to add a main method that can be called with UWSGI."""
    @staticmethod
    def uwsgi_main(config_file):
        """The main method for the Netify app, when started via UWSGI."""
        netify_app = NetifyApp(Config.load_config(config_file))
        netify_app.register_views(Views)
        netify_app.flask_app.logger.info('NETIFY Loaded.')

        return netify_app.flask_app


class NetifyCore(abc.ABC):
    """The Netify Application object.

    Both the Flask Application object and the Netify context are saved as
    singletons for easy access by other code elsewhere in the project. Once the
    Netify Application is configured it can be accessed by a piece of code
    simply by reinstanciating the App class.
    """
    flask_app = None
    netify_app = None

    def __init__(self, config=None):
        if self.netify_app is None:  # First time init
            if self.flask_app is None:
                self.__class__.flask_app = Flask(__name__)
                self.registered_views = []
                if config:
                    self.config = config
                    self.config.update_flask(self.flask_app)
            self.__class__.netify_app = self
        else:
            self = self.__class__.netify_app

    @staticmethod
    def cli_main():
        """The main method for the Netify app, when called from the CLI."""
        config = Config.load_config(os.path.join(os.getenv('HOME'),
                                                 'netify/dev.cfg'))
        netify_app = NetifyApp(config)
        netify_app.register_views(Views)
        netify_app.run(debug=True)

    @property
    @abc.abstractproperty
    def description(self):
        """Provide a description of your app for the CLI Help text."""
        return getattr(self, 'description', '')

    def register_views(self, views):
        """Register the view classes against the flask app.

        The "Method" name registered in the Flask app is the "name" field for
        each View class.
        """
        view_config = self.config.netify_views
        enabled = [name.strip() for name in view_config['enabled'].split(',')]
        for view in views:
            view_cls = view.value
            if view.name in enabled:
                if view_cls.name in self.registered_views:
                    self.flask_app.logger.warning(
                        'Not Registering view %s. A view has already '
                        'been registered for %s.' % (view.name, view_cls.name))
                view_opts = self.config.get_page_options(view_cls.name)
                view_cls.register(self, **view_opts)
                self.registered_views.append(view_cls.name)

    def run(self, host=None, port=None, debug=None):
        """Run the Flask Server."""
        self.flask_app.run(host, port, debug)


class NetifyApp(NetifyCore, CliMixin, UwsgiMixin):
    """An example Netify App composed of the Core and some Mixins."""
    description = "A basic Netify application with all the bells and whistles."
