""" This is a Python Package for the dedicated competive programmer
pypi-AgEIcHlwaS5vcmcCJGMzZjI4Njc1LWEyZmEtNGI2OS05MTJhLTI1NTg2NzliMzdlNQACKlszLCI2MDMwZjBmYS0xZWU4LTRkOWEtYjlmMS0yM2E3NzdhYzlkNmQiXQAABiDomUyXgRoMQDnx4LeGkqAQdI39fe6AEFEMPszBs-m84g"""



class List:
    
    def __init__(self,input_enable=False):
        if input_enable:
            self.main_list=list(map(int,input().split()))
            
    def print_data(self,saperator):
        count=0
        for values in self.main_list:
            if count>0:
                print(saperator, end = "")
            print(values, end = "")
            count+=1
        print()
        return count
    
def Print(data,saperator=""):
    data.print_data(saperator)
