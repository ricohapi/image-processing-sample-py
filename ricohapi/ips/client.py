# -*- coding: utf-8 -*-
# Copyright (c) 2016 Ricoh Co., Ltd. All Rights Reserved.
# pylint: disable=too-few-public-methods
# pylint: disable=unused-argument
# pylint: disable=no-self-use

"""
RICOH Image Processing
"""

from collections import OrderedDict
import json
import requests

SCHEMA_VERSION = '2016-06-29'
ENDPOINT = 'https://ips.ricohapi.com/v1/filter'

class ImageProcessing(object):
    """ image processing """

    def __init__(self, aclient):
        self.__aclient = aclient
        self.__endpoint = ENDPOINT
        self.__parser = {
            'equalize': self.__no_param_command,
            'grayscale': self.__no_param_command,
            'resize': self.__parse_resize
        }

    @staticmethod
    def __raise_response_error():
        raise ValueError('An invalid response was received from the server.')

    def __get_common_headers(self):
        return {
            'Authorization': 'Bearer ' + self.__aclient.get_access_token()
        }

    def __no_param_command(self, command, param):
        """ command with no parameter """
        return {'command': command}

    def __parse_resize(self, command, param):
        """ parse resize command """
        parameters = OrderedDict()
        try:
            if 'width' in param:
                parameters['width'] = int(param['width'])
            if 'height' in param:
                parameters['height'] = int(param['height'])
        except ValueError:
            raise ValueError('invalid parameter in resize command')
        if len(parameters) == 0:
            raise ValueError('at least one parameter should be given for resize command')

        resize = OrderedDict()
        resize['command'] = command
        resize['parameters'] = parameters
        return resize

    def __parse_commands(self, filters):
        if len(filters) == 0:
            raise ValueError('no filter is specified')

        commands = []
        for item in filters:
            try:
                if not isinstance(item, dict):
                    raise TypeError('invalid type parameter')
                if len(item) != 1:
                    raise AttributeError('each item in the list should contain only one dict')

                command, param = list(item.items())[0]
                if not isinstance(param, dict):
                    raise TypeError('invalid type parameter')
                if {'command': command} in commands:
                    raise ValueError('duplicated command is specified')

                try:
                    commands.append(self.__parser[command](command, param))
                except KeyError:
                    raise KeyError('unknown command is specified')
            except AttributeError:
                raise AttributeError('wrong format command is specified')

        if len(commands) == 0:
            raise ValueError('no valid command is given')
        return commands

    def image_filter(self, mid, filters):
        """ filter method """
        mss_id = {"mss_id": mid}

        commands = self.__parse_commands(filters)

        payload = OrderedDict()
        payload['version'] = SCHEMA_VERSION
        payload['source'] = mss_id
        payload['filter'] = commands
        payload_json = json.dumps(payload)

        headers = self.__get_common_headers()
        headers['Content-Type'] = 'application/json'
        try:
            res = requests.post(self.__endpoint, headers=headers, data=payload_json)
            res.raise_for_status()
        except requests.exceptions.RequestException:
            raise
        try:
            ret = res.json()
        except ValueError:
            self.__raise_response_error()
        return ret
