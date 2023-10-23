import requests
import sys
from time import sleep

from banner import get_banner
from config import Config
from exceptions import InvalidHTTPMethodError, InvalidUrlFormat, MissingFUZZTargetError
from method_controller import MethodController
from host_controller import HostController
from status__code_controller import StatusCodeController

args = Config()


class Fuzzer:
    def __init__(self) -> None:
        """
        Initialize the Fuzzer class with command-line arguments and configurations.
        """
        self.arg = args.parse_args()
        self.url = self.arg.url
        self.status_code = self.arg.status_code
        self.wordlist = self.arg.wordlist
        self.request_method = self.arg.method
        self.request_data = self.arg.data
        self.content_reader = self.arg.content_reader
        self.content_length = self.arg.content_length

    def banner(self):
        """
        Display the banner and configuration information.
        """
        banner = get_banner()
        print(banner)
        print('v1 --------------------- Made By Pixel.Def')
        print('-' * 50, '\n')
        sleep(1)
        print(':: URL:          :', str(self.url))
        print(':: Payload:      :', str(self.wordlist))
        print(':: Method:       :', str(self.request_method)
              if not self.request_method is None else 'GET')
        print(':: Status-Code:  :', str(self.status_code)
              if not self.status_code is None else '200, 301, 403, 404' + '\n')
        print('-' * 50, '\n')
        print('[+] Warning: This is fuzzing-based vulnerability testing software. Do not use it without prior permission because this is an illegal action.')
        print('Use it only in authorized environments that have full control. I am not responsible for misuse of the application.\n')
        sleep(2)

    def fuzzer(self):
        """
        Main application method to perform the fuzzing.
        """
        self.banner()
        try:
            method_controller = MethodController(self.request_method)
            host_controller = HostController(self.url)
            self.url = host_controller.locate_fuzz_target()
            host_controller.host_is_up()
            method_controller.allow_methods()

        except InvalidUrlFormat as error:
            print(error)
            return
        except MissingFUZZTargetError as error:
            print(error)
            return
        except InvalidHTTPMethodError as error:
            print(f'\nHTTP method not allowed: {error}')
            return

        try:
            payloads = self.file_read()
            total_payloads = len(payloads)

            count = 0
            for payload in payloads:
                self.fuzzer_request(payload)
                sys.stdout.write(f'\r:: Progress: {count}/{total_payloads}')
                count += 1
        except KeyboardInterrupt:
            print('\n\n:: App Aborted!')
            exit(1)

    def fuzzer_request(self, payload):
        """
        Make HTTP requests using a wordlist payload and handle the responses.

        :param payload: The payload to replace 'FUZZ' in the URL.
        """
        parsed_url = self.url.replace('FUZZ', payload)
        
        self.request_method = self.request_method if not self.request_method is None else 'GET'

        status_code = self.get_status_code()

        response = requests.request(self.request_method, parsed_url)
        
        self.response_controller(response, payload, status_code)

    
    def response_controller(self, response, payload, status_code):
        response_content = response.text
        response_status_code = response.status_code
        response_size = len(response.content)
        response_time = response.elapsed.total_seconds()

        if (not self.content_reader is None and self.content_reader in response_content) and (response_status_code in status_code):
            print(f'\r{payload.ljust(30)}           [Status: {response_status_code}, Size: {response_size}, Duration: {response_time}]')
        
        elif response_status_code in status_code and self.content_reader is None:
            print(f'\r{payload.ljust(30)}           [Status: {response_status_code}, Size: {response_size}, Duration: {response_time}]')
            
        elif (not self.content_length is None and response_size >= self.content_length) and (response_status_code in status_code):
            print(f'\r{payload.ljust(30)}           [Status: {response_status_code}, Size: {response_size}, Duration: {response_time}]')
            
        else:
            pass
        
        
    def get_status_code(self):
        status_code = StatusCodeController(self.status_code)
        return [int(selected_status_code) for selected_status_code in status_code.get_status_codes()]
        
        
    
    def file_read(self):
        """
        Open and read the wordlist file.

        :return: A list of payloads from the wordlist.
        """
        with open(self.wordlist, 'rb') as file:
            payloads = [line.decode('utf-8').strip()
                        for line in file.readlines()]

        return payloads


fz = Fuzzer()
fz.fuzzer()
