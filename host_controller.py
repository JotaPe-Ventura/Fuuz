import requests

from exceptions import InvalidUrlFormat, MissingFUZZTargetError


class HostController:
    def __init__(self, url, arg_data) -> None:
        self.url = url
        self.request_data = arg_data
        pass

    def url_parser(self):
        protocols = ['http', 'https', 'ftp', 'ssh']
        for protocol in protocols:
            if not self.url.startswith(protocol):
                self.url = self.url.split('://')
                if not '://' in self.url:
                    raise InvalidUrlFormat(
                        f'\nProtocol is missing in URL. Try https://{self.url[0]}')

                raise InvalidUrlFormat(
                    f'\nProtocol is missing in URL. Try https://{self.url[1]}')
            else:
                return self.url

    def host_is_up(self):
        status_codes_online = [200, 201, 204, 206, 202]
        
        try:
            self.url = self.url_parser()
            
            if 'FUZZ' in self.url:
                self.url = self.url.replace('FUZZ', '')

            response = requests.get(self.url)
            response_status_codee = response.status_code

            if response_status_codee not in status_codes_online:
                print(response_status_codee)
                print('\n[+] Target is Down!')
            else:
                return self.url

        except requests.exceptions.InvalidURL:
            print(f'\nUrl is invalid: {self.url}')
            return
        except requests.exceptions.ConnectionError:
            print(f'\nError establishing connection with target: {self.url}')
            return


    def locate_fuzz_target(self):
        if 'FUZZ' not in self.url and self.request_data is None:
            raise MissingFUZZTargetError(f'\nUnable to find FUZZ in the url: {self.url}. Try: https://target.com/FUZZ')
        
        return self.url