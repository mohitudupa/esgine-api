import requests
import json


URL = "http://127.0.0.1:8000/predict/"


multipart_form_data = {'text': ('test.bin', open('text.txt', 'r'))}


def pretty_print(data):
	print("{")
	for i in data:
		print(str(i) + ": ")
		print("\t{")
		for j in data[i]:
			print("\t" + str(j) + ": " + str(data[i][j]))
		print("\t}")
	print("}")


def send_request():
	try:
		r = requests.post(url = URL, files=multipart_form_data)
		print("Response status: ", end="")
		if r.ok:
			print("OK")
		else:
			print("Error")
		pretty_print(r.json())
		r.close()
	except:
		print("Exception in send_request function")


def main():
	send_request()


try:
	if __name__ == "__main__":
		main()
except:
	pass
