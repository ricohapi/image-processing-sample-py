# Ricoh Image Processing Sample for Python

Image Processing Service Python Library samples for Ricoh API.
You can apply image filters to the image stored in the Media Storage.

## Requirements

You need

* Ricoh API Client Credentials (client_id & client_secret)
* Ricoh ID (user_id & password)

If you don't have them, please register yourself and your client from [THETA Developers Website](http://contest.theta360.com/).

## Install

```sh
pip install --upgrade git+https://github.com/ricohapi/auth-py.git
pip install --upgrade git+https://github.com/ricohapi/media-storage-py.git
git clone https://github.com/ricohapi/image-processing-sample-py.git
```

In your downloaded directory,
```sh
pip install .
```

# Image processing samples
## Command-line sample
This is a command-line sample program of applying image filters.

### Setup
- Move to samples directory.
- Rename `config_template.json` to `config.json` and setup your credentials.

```json
{
  "USER": "set_your_user_id",
  "PASS": "set_your_user_pass",
  "CLIENT_ID": "set_your_client_id",
  "CLIENT_SECRET": "set_your_client_secret"
}
```

### Example

You need to specify a JPEG file to be uploaded to the media storage service.
Image filters will be applied to the uploaded JPEG image.

```sh
$ python image_processing.py -f <JPEG file name>
```

The program will show the original image followed by equalized, grayscaled and resized images.

# Sample Code Usage
### Constructor

For ImageProcessing module to work, it has to be initialized with valid AuthClient.

```python
from ricohapi.ips.client import ImageProcessing

auth_client = AuthClient('<your_client_id>', '<your_client_secret>')
auth_client.set_resource_owner_creds('<your_user_id>', '<your_password>')

ips_client = ImageProcessing(auth_client)
```

### Apply image filters

image_filter() API accepts two parameters, `<media_id>` and `list` of `<commands>`.

```python
ips_client.image_filter('<media_id>', '[<commands>]')
```

Each command should be described in `dict` form. For instance:

```python
equalize = {'equalize': {}}
commands = [equalize]

grayscale = {'grayscale': {}}
commands = [grayscale]

resize = {'resize': {'width': 100, 'height': 200}}
commands = [resize]
```

You can specify multiple filters at the same time by adding each filter in `<commands>` `list`.

```python
grayscale = {'grayscale': {}}
resize = {'resize': {'width': 100, 'height': 200}}
commands = [grayscale, resize]
```
