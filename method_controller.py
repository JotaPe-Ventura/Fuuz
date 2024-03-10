from exceptions import InvalidHTTPMethodError


class MethodController:
    def __init__(self, method) -> None:
        self.method = method.upper()
        pass
    
    def allow_methods(self):
        allow_methods_to_request = ['GET', 'POST', 'PUT', 'DELETE', 'TRACE', 'OPTIONS', 'HEAD']
        
        if self.method not in allow_methods_to_request:
            raise InvalidHTTPMethodError(f'{self.method}')
        
        return self.method
