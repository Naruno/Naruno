#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.class cache:

class Cache
  cache = {}

  @staticmethod
  def get(key):
    return cache.cache[key]  
  @staticmethod
  def save (key, value):
    cache.cache[key] = value
