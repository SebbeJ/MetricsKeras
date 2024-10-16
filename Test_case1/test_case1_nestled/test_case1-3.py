
class Test_class:
    def __init__(self):
        self.name = "Inte så viktigt" #1

    def class_method(self):
        self.name = "en liten ändring" #1

        def inner_class_method():
            print("Fungerar det innanför en klass?") #2, 1

            return "Här kommer stupet"#3, 2
        
def method_after_class():
    return "Hoppas detta fungerar" # 1

#Genomsnitt = 1.25
#Weight= 4S