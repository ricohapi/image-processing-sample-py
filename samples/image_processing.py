#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2016 Ricoh Co., Ltd. All Rights Reserved.

"""image processing sample"""
import json
import argparse
from io import BytesIO as stream
from PIL import Image
from ricohapi.mstorage.client import MediaStorage
from ricohapi.auth.client import AuthClient
from ricohapi.ips.client import ImageProcessing

class ImageProcessingSample(object):
    """ image processing sample """

    def __init__(self):
        """ read config file and initialize auth client """
        with open('./config.json', 'r') as settings:
            config = json.load(settings)
            client_id = config['CLIENT_ID']
            client_secret = config['CLIENT_SECRET']
            user_id = config['USER']
            user_pass = config['PASS']

        self.auth_client = AuthClient(client_id, client_secret)
        self.auth_client.set_resource_owner_creds(user_id, user_pass)

        self.mss_client = MediaStorage(self.auth_client)
        self.ips_client = ImageProcessing(self.auth_client)

    def show_result(self, media_id, commands, title=None):
        """ call image_filter API and show the processed image """
        res = self.ips_client.image_filter(media_id, commands)
        Image.open(stream(self.mss_client.download(res['id']))).show(title)

    def main(self):
        """ main """
        parser = argparse.ArgumentParser(description='Image processing sample')
        parser.add_argument('-f', type=str, dest='filename', help='specify JPEG file to process')
        args = parser.parse_args()
        if args.filename is None:
            parser.print_help()
            return

        try:
            img = Image.open(args.filename)
            if img.format != 'JPEG':
                raise ValueError('Non-jpeg file is specified.')
        except IOError:
            raise

        self.mss_client.connect()
        res = self.mss_client.upload(args.filename)
        media_id = res['id']

        img.show(title='original image')

        equalize = {'equalize': {}}
        grayscale = {'grayscale': {}}
        half_width = img.width//2
        half_height = img.height//2
        resize = {'resize': {'width': half_width, 'height': half_height}}

        commands = [equalize]
        self.show_result(media_id, commands, title='equalize')

        commands = [grayscale]
        self.show_result(media_id, commands, title='grayscale')

        commands = [resize]
        self.show_result(media_id, commands, title='resize')

        # when you specify either one of resize parameter, image aspect ratio will be retained
        # therefore, following code should also work
        # resize = {'resize': {'width': half_width}}
        # commands = [resize]
        # self.show_result(media_id, commands, title='resize')
        # resize = {'resize': {'height': half_height}}
        # commands = [resize]
        # self.show_result(media_id, commands, title='resize')

        commands = [grayscale, resize]
        self.show_result(media_id, commands, title='grayscale and resize')

if __name__ == '__main__':
    ImageProcessingSample().main()
