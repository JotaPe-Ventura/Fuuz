class StatusCodeController:
    def __init__(self, status_code) -> None:
        self.status_code = status_code
        pass
    
    def get_status_codes(self):
        if not self.status_code is None:
            return self.status_code.split(',')
        
        return [200, 301, 403, 404]