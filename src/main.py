"""A module containing the main CLI frontend code."""
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
from .app import NetifyApp
from .view import Views
from .config import Config


def main():
    """The main method for the Netify application."""
    config = Config.load_config('/home/csand/netify/dev.cfg')
    netify_app = NetifyApp(config)
    netify_app.register_views(Views)
    netify_app.run(debug=True)
