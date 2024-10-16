def test_method1(input):
    '''Lite simpla docstrings den inte ska räkna''' 
    print("En simpel metod som endast testar lite") #1

    #En kommentar efter ett mellanrum för att se 
    #så att den inte räknar tomma rader eller komentarer

    return 0 #2

def test_method2(
        input1, 
        input2
    ):
    """
    En lite jobbigare metod med parametrar som tar flera rader 
    och docstrings som tar flera rader
    """

    print("Nu får vi se om den kan lägga till inre metoder i yttra rätt") #1

    def local_method(input3):
        print("Bara en liten inre metod som kan sabba allt") #2, 1
        return input3 #3, 2
    
    return "Det är bra så" #4

#Genomsnitt = 2.67
#Weight= 3