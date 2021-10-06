
#!/usr/bin/python
 
dict = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
 
dict['Age'] = 18                 # 更新
dict['School'] = "RUNOOB"       # 添加
 

if __name__ == '__main__':
    print("dict['Age']: ", dict['Age'])
    print("dict['School']: ", dict['School'])
    dict1 = dict
    dict1['Age'] = 8
    print("dict['Age']: ", dict['Age'])

