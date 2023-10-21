#!/usr/bin/env python3

# Copyright 2023 Dirk Pleiter <dirk.pleiter@pm.me>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Test whether a set of XML documents comply with an XML schema
"""


import os
import sys
import argparse
import xmlschema
from avocado import Test
from avocado.core.job import Job
from avocado.core.suite import TestSuite


config = {
    "resolver.references":      [__file__ + ":Validator.test"],
    "run.dict_variants":        [],
    "run.max_parallel_tasks":   1,
}


class Validator(Test):
    def test(self):
        xsd = self.params.get("xsd")
        xml = self.params.get("xml")
        isValid = self.params.get("isValid")

        inst = xmlschema.XMLSchema(xsd)
        
        if (isValid > 0):
            try:
                inst.validate(xml)
            except:
                self.error("Document \"%s\" is not expected to be invalid" % (xml))
        else:
            try:
                inst.validate(xml)
            except:
                self.fail("Document \"%s\" is expected to be invalid" % (xml))
            else:
                self.error("Document \"%s\" is not expected to be valid" % (xml))

    def add(xsd, xmlLst, isValid):
        if xmlLst is not None:
            for xml in xmlLst:
                if not os.path.isfile(xml):
                    print("XML file \"%s\" does not exist or is not a file" % (xml), file=sys.stderr)
                    sys.exit()
                config["run.dict_variants"].append({"xsd": xsd, "xml":  xml, "isValid": isValid})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--schema', dest='xsd', type=str)
    parser.add_argument('--valid', action='extend', nargs='*', type=str, required=False)
    parser.add_argument('--nonvalid', action='extend', nargs='*', type=str, required=False)
    args = parser.parse_args()

    if not os.path.isfile(args.xsd):
        print("XSD file \"%s\" does not exist or is not a file" % (args.xsd), file=sys.stderr)
        sys.exit()

    Validator.add(args.xsd, args.valid, 1)
    Validator.add(args.xsd, args.nonvalid, 0)

    if (len(config["run.dict_variants"]) > 0):
        suite = TestSuite.from_config(config)
        with Job(config, [suite]) as job:
            sys.exit(job.run())