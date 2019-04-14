import pandas as pd
import json
import sys
import requests

test_data = sys.argv[1]

IP = input("Enter server IP:")

test_data = pd.read_csv(test_data, header = None)
test_data = test_data.iloc[1:,:-1]

request_str = {"signature_name": "predict","instances":[]}
for index,row in test_data.iterrows():
	temp = {"sepal_length":[float(row[0])],"sepal_width":[float(row[1])],"petal_length":[float(row[2])],"petal_width":[float(row[3])]}
	request_str['instances'].append(temp)

data = json.dumps(request_str)
headers = {"content-type": "application/json"}
json_response = requests.post('http://'+IP+':9500/v1/models/iris:predict', data=data, headers=headers)


json_response = json.loads(str(json_response.text))

f = open('predictions.txt', 'w')
print(json_response)
ans =json_response["predictions"]
for i in range(len(ans)):
	if ans[i]['classes'] == ['0']:
		print('Iris-Setosa')
		f.write('Iris-Setosa\n')
	elif ans[i]['classes'] == ['1']:
		print('Iris-Virginica')
		f.write('Iris-Virginica\n')
	elif ans[i]['classes'] == ['2']:
		print('Iris-Versicolor')
		f.write('Iris-Versicolor\n')
f.close()
