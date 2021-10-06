import requests

if __name__ == '__main__':
    s = requests.Session()
    count = 0
    while count < 1000:
        s.get('http://127.0.0.1:8000/data')      # best practice
        # requests.get('http://127.0.0.1:8000/data') #   not be recommended
