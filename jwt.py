import base64
import hashlib
import json

class JWT:
    header = { 'alg': 'HS512', 'typ': 'JWT' }
    payload = {}
    token = None

    def __init__(self, payload = {}, token = None):
        if not token:
            self.payload = payload
        else:
            self.payload = self.parsePayload(token)
            self.token = token

    @classmethod
    def base64ToDict(self, str):
        return json.loads(base64.b64decode(str.encode()).decode('utf-8'))

    @classmethod
    def dictToBase64(self, dict):
        return base64.b64encode(json.dumps(dict).encode()).decode('utf-8')

    def generateSignature(self, headerBase64, payloadBase64):
        return hashlib.sha512(f'{headerBase64}.{payloadBase64}'.encode()).hexdigest()

    def generateToken(self):
        headerBase64 = self.dictToBase64(self.header)
        payloadBase64 = self.dictToBase64(self.payload)
        signature = self.generateSignature(headerBase64, payloadBase64)
        return f'Bearer {headerBase64}.{payloadBase64}.{signature}'

    def isValid(self):
        return self.generateToken() == self.token

    @staticmethod
    def parseHeader(token):
        jwt = JWT({}, token)
        return jwt

    def parsePayload(self, token):
        return self.base64ToDict(token.split('.')[1])
