from typing import ClassVar 

class Foo:
    def __init__(self):
        pass
    def sample(self):
       try:     
            bar: ClassVar[list[str]] = ["account", 'world']
            print(bar)
       except:
           print("error")     
           
    
obj = Foo()
obj.sample()
