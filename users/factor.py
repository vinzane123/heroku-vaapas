import requests
from users.factor_config import *


url = "http://2factor.in/API/V1/"+str(api_key)+"/ADDON_SERVICES/SEND/TSMS"

payload = {'From': From,
'TemplateName': TemplateName,
}
files = [
]

