import json
import pickle
import time
import ujson


dataa = None
with open("testout") as f:
	dataa = f.read().split('\n')

i = 0
data=dataa[:15]
x = [10,20,30,40,50,75,100,250,500,600,750,900,1000,2000,3000]
# res = {"avg": 0}
# for size in x:
#         obj = json.loads(data[i].rstrip())
#         t1 = time.time()
#         ob = None
#         for j in range(10000):
#             ob = pickle.loads(pickle.dumps(obj))
#         t2 = time.time()
#         res['avg'] = (t2 - t1) / 10000
#         print(str(size) + ";" + str(res))
#         i += 1

dataa = None
with open("testout", "rb") as f:
	dataa = f.read().replace(b'b\\\'', b'')
	dataa = dataa.replace(b'\'', b'')
	dataa = dataa.replace(b'b', b'')
	dataa = dataa.split(b'\n')


res = {"avg": 0}
i = 0
data=dataa[15:]
# for size in x:
# 	obj = data[i]
# 	t1 = time.time()
# 	ob = None
# 	for j in range(10000):
# 		ob = json.loads(obj)
# 	t2 = time.time()
# 	res['avg'] = (t2 - t1) / 10000
# 	print(str(size) + ";" + str(res))
# 	i += 1
i = 0
for size in x:
	obj = data[i]
	t1 = time.time()
	ob = None
	for j in range(10000):
		ob = ujson.loads(obj)
	t2 = time.time()
	res['avg'] = (t2 - t1) / 10000
	print(str(size) + ";" + str(res))
	i += 1
