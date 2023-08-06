class BaseWrapper:
    def __init__(self, akamai=None):
        self.generate_headers(akamai)

    def generate_headers(self, akamai=None):
        self.headers = {
            'Content-Type': 'application/json'
        }

        if akamai:
            self.headers['X-TKPD-AKAMAI'] = akamai
        
        return self.headers

    def serialize(self):
        raise NotImplementedError