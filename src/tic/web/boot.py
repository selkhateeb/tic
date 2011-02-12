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
import logging
from google.appengine.ext.webapp import util
from tic.web.main import dispatch_request
from tic.env import Environment
from google.appengine.dist import use_library
use_library('django', '1.2')

ENVIRONMENT = Environment()

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    util.run_wsgi_app(dispatch_request)

if __name__ == '__main__':
    main()
