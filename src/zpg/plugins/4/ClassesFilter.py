#!/usr/bin/env python
import logging
import os
logging.basicConfig()
log = logging.getLogger('Classes Filter')
from zpg.utils import KlassExpand

class ClassesFilter(object):
    type = 'filter'
    def __init__(self,config,opts):
        self.config = config
        self.basedir = opts.dest

    def run(self):
        self.config['classes'] = [x for x in self.config['component']]
        return self.config