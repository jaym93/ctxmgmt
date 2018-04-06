import json
import requests

base_url = 'https://cloud.internalpositioning.com/api/v1'

def get_location(device_name, family_name='ctxmgmt'):
  """
  Gives last seen location of device
  :param device_name: Name of device
  :param family_name: Name of family
  :return:
  """
  url = '{:s}/location_basic/{:s}/{:s}'.format(base_url, family_name,
                                               device_name)

  out = {}

  try:
    resp = requests.get(url)
    resp = json.loads(resp.content)

    if not resp['success']:
      out['message'] = 'Unable to get data from Find3: {:s}'. \
        format(resp['message'])

    out['device_name'] = device_name
    out['family_name'] = family_name
    for k,v in resp['data'].items():
      out[k] = v

  except ConnectionError as e:
    out['message'] = 'Connection error: {:s}'.format(e)
  except requests.HTTPError as e:
    out['message'] = 'HTTP error: {:s}'.format(e)
  except TimeoutError as e:
    out['message'] = 'Timeout error: {:s}'.format(e)
  except requests.TooManyRedirects as e:
    out['message'] = 'Too many redirects: {:s}'.format(e)
  except:
    out['message'] = 'unknown error'
  finally:
    return out


if __name__ == '__main__':
  import time
  while True:
    out = get_location('rpi')
    print('rpi is at {:s} ({:d}% confident)'.format(out['loc'],
                                                       int(float(out['prob']*100))))
    time.sleep(10)