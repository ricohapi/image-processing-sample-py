# -*- coding: utf-8 -*-
# Copyright (c) 2016 Ricoh Co., Ltd. All Rights Reserved.
"""
Smoke test for client API.
"""

from unittest import TestCase
from mock import Mock, patch
from nose.tools import raises
from ricohapi.ips.client import ImageProcessing

ENDPOINT = 'https://ips.ricohapi.com/v1/filter'

PREFIX = '{"version": "2016-06-29", "source": {"mss_id": "1234"}, "filter": '
POSTFIX = '}'

class TestMethodOk(TestCase):
    """ all the successful test cases """
    def setUp(self):
        self.aclient = Mock()
        self.aclient.get_access_token = Mock(return_value='atoken')
        self.ips = ImageProcessing(self.aclient)

    @patch('requests.post')
    def test_equalize_ok(self, req):
        """ valid equalize command """
        payload = PREFIX + '[{"command": "equalize"}]' + POSTFIX
        self.ips.image_filter('1234', [{'equalize': {}}])
        headers = {'Authorization': 'Bearer atoken', 'Content-Type': 'application/json'}
        req.assert_called_once_with(ENDPOINT, headers=headers, data=payload)

    @patch('requests.post')
    def test_grayscale_ok(self, req):
        """ valid grayscale command """
        payload = PREFIX + '[{"command": "grayscale"}]' + POSTFIX
        self.ips.image_filter('1234', [{'grayscale': {}}])
        headers = {'Authorization': 'Bearer atoken', 'Content-Type': 'application/json'}
        req.assert_called_once_with(ENDPOINT, headers=headers, data=payload)

    @patch('requests.post')
    def test_resize_ok(self, req):
        """ valid resize command """
        payload = PREFIX + '[{"command": "resize", "parameters": {"width": 100, "height": 200}}]' + POSTFIX
        self.ips.image_filter('1234', [{'resize': {'width': 100, 'height': 200}}])
        headers = {'Authorization': 'Bearer atoken', 'Content-Type': 'application/json'}
        req.assert_called_once_with(ENDPOINT, headers=headers, data=payload)

    @patch('requests.post')
    def test_resize_width_only_ok(self, req):
        """ valid resize command which has only width parameter"""
        payload = PREFIX + '[{"command": "resize", "parameters": {"width": 100}}]' + POSTFIX
        self.ips.image_filter('1234', [{'resize': {'width': 100}}])
        headers = {'Authorization': 'Bearer atoken', 'Content-Type': 'application/json'}
        req.assert_called_once_with(ENDPOINT, headers=headers, data=payload)

    @patch('requests.post')
    def test_resize_height_only_ok(self, req):
        """ valid resize command which has only height parameter"""
        payload = PREFIX + '[{"command": "resize", "parameters": {"height": 200}}]' + POSTFIX
        self.ips.image_filter('1234', [{'resize': {'height': 200}}])
        headers = {'Authorization': 'Bearer atoken', 'Content-Type': 'application/json'}
        req.assert_called_once_with(ENDPOINT, headers=headers, data=payload)

    @patch('requests.post')
    def test_equalize_grayscale_ok(self, req):
        """ both equalize and grayscale command will be applied """
        payload = PREFIX + '[{"command": "equalize"}, {"command": "grayscale"}]' + POSTFIX
        self.ips.image_filter('1234', [{'equalize': {}}, {'grayscale': {}}])
        headers = {'Authorization': 'Bearer atoken', 'Content-Type': 'application/json'}
        req.assert_called_once_with(ENDPOINT, headers=headers, data=payload)

class TestMethodError(TestCase):
    """ all the failure test cases """
    def setUp(self):
        self.aclient = Mock()
        self.aclient.get_access_token = Mock(return_value='atoken')
        self.ips = ImageProcessing(self.aclient)

    @raises(KeyError)
    def test_key_error(self):
        """ specifying invalid filter command """
        self.ips.image_filter('1234', [{'no_such_command': {}}])

    @raises(TypeError)
    def test_command_format_error(self):
        """ specifying invalid format filter command """
        self.ips.image_filter('1234', ['equalize'])

    @raises(TypeError)
    def test_command_type_error(self):
        """ specifying invalid type filter command """
        self.ips.image_filter('1234', [{'equalize': 0}])

    @raises(TypeError)
    def test_resize_format_error(self):
        """ resize command should have parameters as dict """
        self.ips.image_filter('1234', [{'resize': (100, 200)}])

    @raises(ValueError)
    def test_resize_command_error(self):
        """ resize command should have at least one parameter """
        self.ips.image_filter('1234', [{'resize': {}}])

    @raises(ValueError)
    def test_resize_param_error(self):
        """ unsupported resize command parameter """
        self.ips.image_filter('1234', [{'resize': {'width': '50%'}}])

    @raises(ValueError)
    def test_duplicate_equalize_error(self):
        """ the same command should not repeat """
        self.ips.image_filter('1234', [{'equalize': {}}, {'equalize': {}}])

    @raises(ValueError)
    def test_duplicate_grayscale_error(self):
        """ the same command should not repeat """
        self.ips.image_filter('1234', [{'grayscale': {}}, {'grayscale': {}}])

    @raises(ValueError)
    def test_no_filter_error(self):
        """ at least one valid command should be given """
        self.ips.image_filter('1234', [])

    @raises(AttributeError)
    def test_no_empty_dict_error(self):
        """ command should not be empty """
        self.ips.image_filter('1234', [{}])

    @raises(AttributeError)
    def test_too_many_items(self):
        """ each dict item should contain only one item """
        self.ips.image_filter('1234', [{'equalize': {}, 'grayscale': {}}])

