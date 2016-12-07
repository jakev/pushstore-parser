#!/usr/bin/env python
# pushstore_parser.py
# Copyright 2016 Jake Valletta (@jake_valletta)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Python script to parse Apple Push Notification ("APN") .pushstore files"""

import argparse
import datetime
import sys
import biplist

UNIX_OFFSET = 978307200

ARCHIVER_KEY = '$archiver'
CLASS_KEY = '$class'
CLASSNAME_KEY = '$classname'
OBJECTS_KEY = '$objects'
TOP_KEY = '$top'

NS_KEYS = 'NS.keys'
NS_OBJECTS = 'NS.objects'
NS_TIME = 'NS.time'

NS_ARRAY_CLASSNAME = 'NSArray'
NS_MUTABLE_ARRAY_CLASSNAME = 'NSMutableArray'
NS_MUTABLE_DICTIONARY = 'NSMutableDictionary'

DEFAULT_KEYS = ['AppNotificationCreationDate',
                'RequestedDate',
                'TriggerDate',
                'AppNotificationMessage']


class PushStoreParser(object):

    """Main Execution Class"""

    delimit = ""
    plist = None
    objects_list = None

    @classmethod
    def error(cls, error):

        """Write an error to stderr"""

        sys.stderr.write("[Error] %s\n" % error)

    def run(self, args):

        """Start parse"""

        self.delimit = args.delimit

        try:
            self.plist = biplist.readPlist(args.pushstore_file)

        except (biplist.InvalidPlistException,
                biplist.NotBinaryPlistException), err:
            self.error("Not a plist: %s" % err)
            return 1

        if not self.is_valid_pushstore():
            self.error("Not a valid NSKeyedArchiver!")
            return 2

        top = self.get_top()
        if top == -1:
            self.error("Unable to get $top location!")
            return 3

        self.objects_list = self.plist[OBJECTS_KEY]

        pointer_to_entries = self.load_from_location(top)

        print self.delimit.join(DEFAULT_KEYS)

        for entry_offset in pointer_to_entries['objects']:

            entry_dict = self.make_entry_dict(
                self.load_from_location(entry_offset))

            formatted = self.format_entry(entry_dict)

            print self.delimit.join([formatted[x] for x in DEFAULT_KEYS])

        return 0

    def is_valid_pushstore(self):

        """Check version and archiver key"""

        try:
            return bool(self.plist[ARCHIVER_KEY] == "NSKeyedArchiver")
        except KeyError:
            self.error("Unable to read '$archiver'")
            return False

    def get_top(self):

        """Find pointer in $objects to starting point"""

        try:
            return int(self.plist[TOP_KEY]['root'])
        except (KeyError, ValueError):
            return -1

    def load_from_location(self, top):

        """Load objects (and keys) from a location"""

        loaded_dict = dict()

        start = self.objects_list[top]

        loaded_class = self.get_classname_at(start)

        if loaded_class is None:
            self.error("Unable to determine $classname of key!")
            return None,

        loaded_dict['class'] = loaded_class
        loaded_dict['objects'] = [int(x) for x in start[NS_OBJECTS]]

        if loaded_class == NS_MUTABLE_DICTIONARY:
            loaded_dict['keys'] = [int(x) for x in start[NS_KEYS]]

        return loaded_dict

    def get_classname_at(self, start):

        """Get the classname of the object referenced"""

        try:
            return self.objects_list[int(start[CLASS_KEY])][CLASSNAME_KEY]
        except (KeyError, ValueError):
            return None

    def make_entry_dict(self, loaded):

        """Make dict from offset and keys"""

        entries = dict()

        offsets = loaded['objects']
        keys = loaded['keys']

        i = 0
        while i < len(keys):
            entries[self.objects_list[keys[i]]] = self.objects_list[offsets[i]]
            i += 1

        return entries

    def format_entry(self, raw):

        """Format each of the entries"""

        formatted = dict()

        formatted['AppNotificationCreationDate'] = self.safe_get_time(
            raw, 'AppNotificationCreationDate')
        formatted['RequestedDate'] = self.safe_get_time(
            raw, 'RequestedDate')
        formatted['TriggerDate'] = self.safe_get_time(
            raw, 'TriggerDate')

        formatted['AppNotificationMessage'] = raw['AppNotificationMessage']

        return formatted

    @classmethod
    def to_real_time(cls, ns_time):

        """Convert an NSTime to UTC timestamp string"""

        return str(datetime.datetime.utcfromtimestamp(ns_time + UNIX_OFFSET))

    def safe_get_time(self, in_dict, key):

        """Safely get a timestamp"""

        try:
            return self.to_real_time(in_dict[key][NS_TIME])
        except KeyError:
            return 'N/A'


def main():

    """Main execution"""

    parser = argparse.ArgumentParser()
    parser.add_argument('pushstore_file', type=str,
                        help='Pushstore file to parse')
    parser.add_argument('-F', '--delimit',
                        help='Delimiter to use (Default: |)', default='|')

    args = parser.parse_args()

    main_class = PushStoreParser()

    return main_class.run(args)

if __name__ == "__main__":
    main()
