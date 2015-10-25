# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2015, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the MIT License along with this 
# program.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

from confluence import Confluence


def create(streamIds, **kwargs):
  """
  Creates and loads data into a Confluence, which is a collection of River 
  Streams.
  :param streamIds: (list) Each data id in this list is a list of strings:
                    1. river name
                    2. stream name
                    3. field name 
  :param kwargs: Passed into Confluence constructor
  :return: (Confluence)
  """
  print "Creating Confluence for the following RiverStreams:" \
        "\n\t%s" % ",\n\t".join([":".join(row) for row in streamIds])
  confluence = Confluence(streamIds, **kwargs)
  confluence.load()
  return confluence


