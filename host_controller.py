import requests

from exceptions import InvalidUrlFormat, MissingFUZZTargetError


class HostController:
    def __init__(self, url) -> None:
        self.url = url
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
                parsed_url = self.url.replace('FUZZ', '')

            response = requests.get(parsed_url)
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
        if 'FUZZ' not in self.url:
            raise MissingFUZZTargetError(f'\nUnable to find FUZZ in the url: {self.url}. Try: https://target.com/FUZZ')
        
        return self.url