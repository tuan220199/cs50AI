import random
list1 = [1,2,3,4]
for i in range(10):
	print(random.choices(list1,[4,4,6,4],k=1))