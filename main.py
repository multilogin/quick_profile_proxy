import requests
import json
import hashlib

USERNAME = 'Foo@Bar.com'
PASSWORD = 'FooBar'

PROXY_COUNTRY = 'us'
PROXY_PROTOCOL = 'socks5'
PROXY_TYPE = 'sticky'
PROXY_QUALITY = 'medium'

# Signin on Multilogin platform to get token

url = 'https://api.multilogin.com/user/signin'

payload = json.dumps({
  'email': f'{USERNAME}',
  'password': hashlib.md5(bytes(f'{PASSWORD}', encoding='UTF-8')).hexdigest()
})
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

response = requests.request('POST', url, headers=headers, data=payload, verify=False)

token = response.json().get('data').get('token')

headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': f'Bearer {token}'
}

# Get proxy info

payload = {
    'country': f'{PROXY_COUNTRY}',
    'region': '',
    'city': '',
    'protocol': f'{PROXY_PROTOCOL}',
    'sessionType': f'{PROXY_TYPE}',
    'IPTTL': 0,
    'quality': f'{PROXY_QUALITY}'
}

url = 'https://profile-proxy.multilogin.com/v1/proxy/connection_url'

response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)

# Parse the response
if response.status_code == 201:
    response_data = response.json()
    proxy_data = response_data['data']
    # Split the data string to extract host, port, username, and password
    parts = proxy_data.split(':')
    host = parts[0]
    port = int(parts[1])
    username = parts[2]
    password = parts[-1]  # Assuming password is the last part

    proxy_info = {
        'host': host,
        'type': payload['protocol'],
        'port': port,
        'username': username,
        'password': password
    }
else:
    raise Exception(f'Failed to get proxy connection URL. Status code: {response.status_code}, Response: {response.text}')

# Start quick profile

url = 'https://launcher.mlx.yt:45001/api/v2/profile/quick'

payload = json.dumps({
    'browser_type': 'mimic',
    'os_type': 'macos',
    'is_headless': False,
    'proxy': proxy_info,
    'parameters': {
        'flags': {
            'audio_masking': 'mask',
            'fonts_masking': 'mask',
            'geolocation_masking': 'mask',
            'geolocation_popup': 'allow',
            'graphics_masking': 'mask',
            'graphics_noise': 'mask',
            'localization_masking': 'mask',
            'media_devices_masking': 'mask',
            'navigator_masking': 'mask',
            'ports_masking': 'mask',
            'screen_masking': 'mask',
            'timezone_masking': 'mask',
            'webrtc_masking': 'mask',
            'proxy_masking': 'custom'
        },
        'fingerprint': {}
    }})

response = requests.request('POST', url, headers=headers, data=payload, verify=False)