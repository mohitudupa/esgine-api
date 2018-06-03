import requests
import json


URL = "http://127.0.0.1:8000/predict/api/"


multipart_form_data = {'text': ('text.bin', open('esgine.csv', 'r'))}


def send_request():
	try:
		r = requests.post(url = URL, files=multipart_form_data)
		print("Response status: ", end="")
		if r.ok:
			print("OK")
		else:
			print("Error")
		print(r.json())
		r.close()
	except Exception as e:
		print("Exception in send_request function")
		print(e)


def main():
	send_request()


try:
	if __name__ == "__main__":
		main()
except:
	pass
