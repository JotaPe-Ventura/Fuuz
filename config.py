import argparse


class Config:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser()
        self.setup_arguments()
        pass
    
    def setup_arguments(self):
        self.parser.add_argument('-u', '--url', required=True,
                                 help='Target URL: https://example.com/FUZZ')
        self.parser.add_argument('-sc', '--status_code', required=False,
                                 help='Expected response status code (200, 301, 403, 500)')
        self.parser.add_argument('-e', '--extension', required=False,
                                 help='File extension')
        self.parser.add_argument('-w', '--wordlist', required=True,
                                 help='Wordlist file for fuzzing')
        self.parser.add_argument(
            '-X', '--method', required=False, default='GET')
        self.parser.add_argument(
            '-d', '--data', help='Request content body', required=False)
        self.parser.add_argument('-cr', '--content_reader', required=False,
                                 help='Search for word in response')
        self.parser.add_argument('-cl', '--content_length', required=False)

    def parse_args(self):
        return self.parser.parse_args()
