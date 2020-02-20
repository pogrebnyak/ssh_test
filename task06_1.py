class MyList():

    def __init__(self):
        self._my_list = []
         
    def append(self, value):
       self._my_list += [value]

    def insert(self, index, value):
        self._my_list = self._my_list[0:index] + [value] + self._my_list[index:len(self._my_list)] 
        
    def remove(self, value):
        flag = True
        for index, j in enumerate(self._my_list):
            if value == j:
                self._my_list = self._my_list[0:index] + self._my_list[index + 1:len(self._my_list)]
                flag = False
        if flag:
            raise ValueError
                           
    def pop(self, index=None):
       if index == None:
            index = len(self._my_list) - 1
       result = self._my_list[index]
       self._my_list = self._my_list[0:index] + self._my_list[index + 1:len(self._my_list)]
       if not result:
           raise IndexError('pop index out of range')
       return result 
         
    def clear(self):
        self._my_list = []

    def __add__(obj1, obj2):
        return obj1() + obj2()
    
    def __str__(self):
        return str(self._my_list)

a = MyList()
c = MyList()
c = ['1','2','3','4','5']
a.append('1')
a.append('2')
a.append('3')
a.append('4')
a.append('5')
a.insert(8,'13')
a.pop(0)
print(a,c)
print(a + c)
print()
b = ['1','2','3','4','5']
b.insert(8,'14')
b.pop(4)
print(b + b)




    
