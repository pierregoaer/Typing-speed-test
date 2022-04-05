import requests

URL = "https://www.mit.edu/~ecprice/wordlist.10000"

words = requests.get(URL).content.splitlines()
# keeping only 7-letter words and convert bytes to str
words_clean = [word.decode("utf-8") for word in words if len(word) < 8]

# print(words_clean)
