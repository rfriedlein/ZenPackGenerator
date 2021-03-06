#!/usr/bin/env python
#
#
# Copyright (C) Zenoss, Inc. 2013, all rights reserved.
#
# This content is made available according to terms specified in the LICENSE
# file at the top-level directory of this package.
#
#

from ._zenoss_utils import KlassExpand
from .Relationship import Relationship
find = Relationship.find


class DeviceClass(object):

    '''Device Class Container'''
    deviceClasses = {}

    def __init__(self,
                 ZenPack,
                 path,
                 prefix='/zport/dmd',
                 zPythonClass='Products.ZenModel.Device.Device',
                 componentTypes=None,
                 deviceType=None):
        '''Args:
                 path: Destination device class path (the prefix is
                        automatically prepended)
                 ZenPack: ZenPack Class Instance
                 prefix: Destination device class prefix [/zport/dmd]
                 zPythonClass: The zPythonClass this Device Class references.
                               [Products.ZenModel.Device.Device]
                 componentTypes: an array of dictionaries used to create
                                  components.
                 deviceType: a dictionary used to create a device component.
        '''

        self.zenpack = ZenPack
        self.path = '/'.join([prefix, path.lstrip('/')])
        self.id = self.path
        self.subClasses = {}
        self.zPythonClass = KlassExpand(self.zenpack, zPythonClass)
        self.DeviceType()

        DeviceClass.deviceClasses[self.id] = self
        self.zenpack.registerDeviceClass(self)

        # Dict loading
        if componentTypes:
            for component in componentTypes:
                self.addComponentType(**component)

    def DeviceType(self):
        '''Create a deviceType component from a zPythonClass reference'''

        self.deviceType = self.zenpack.addComponentType(
            self.zPythonClass, device=True)

    def addClass(self, deviceClass, *args, **kwargs):
        '''Create a sub device class'''

        if 'prefix' in kwargs:
            del(kwargs['prefix'])

        if 'zPythonClass' in kwargs:
            return DeviceClass(self.zenpack,
                               deviceClass,
                               prefix=self.path,
                               *args,
                               **kwargs)
        else:
            return DeviceClass(self.zenpack,
                               deviceClass,
                               prefix=self.path,
                               zPythonClass=self.zPythonClass,
                               *args,
                               **kwargs)

    def addComponentType(self, *args, **kwargs):
        '''Add a component to the deviceType component'''

        if 'zenpack' not in kwargs:
            kwargs['zenpack'] = self.zenpack
        c = self.deviceType.addComponentType(*args, **kwargs)
        return c

    @property
    def componentTypes(self):
        '''Return the component types defined inside this deviceClass.
           Including child components.
        '''

        def ComponentFind(child=None):
            components = []
            if child:
                rels = find(child, First=True)
                for rel in rels:
                    newchild = rel.child()
                    components.append(newchild)
                    rval = ComponentFind(newchild)
                    if rval:
                        components = components + rval
            return components
        components = ComponentFind(self.deviceType)
        return sorted(components)
