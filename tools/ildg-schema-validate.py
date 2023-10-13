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
import xmlschema
from avocado import Test
from avocado.core.job import Job
from avocado.core.suite import TestSuite


config = {
    "resolver.references":      [__file__ + ":Validate.test"],
    "run.dict_variants":        [],
    "run.max_parallel_tasks":   4,
}


class Validate(Test):
    def test(self):
        xsd = self.params.get("xsd")
        xml = self.params.get("xml")
        inst = xmlschema.XMLSchema(xsd)
        inst.validate(xml)


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Usage: %s schema.xsd doc1.xml [doc2.xml ...]" % (sys.argv[0]))
        sys.exit()

    xsd = sys.argv[1]
    if not os.path.isfile(xsd):
        print("XSD file \"%s\" does not exist or is not a file" % (xsd), file=sys.stderr)
        sys.exit()

    for i in range(2, len(sys.argv)):
        xml = sys.argv[i]
        if not os.path.isfile(xml):
            print("XML file \"%s\" does not exist or is not a file" % (xml), file=sys.stderr)
            sys.exit()
        config["run.dict_variants"].append({"xsd": xsd, "xml":  xml})

    suite = TestSuite.from_config(config)

    with Job(config, [suite]) as j:
        sys.exit(j.run())
