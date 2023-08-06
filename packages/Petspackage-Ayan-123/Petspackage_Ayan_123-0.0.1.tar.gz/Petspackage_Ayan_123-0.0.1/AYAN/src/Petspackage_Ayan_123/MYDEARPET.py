#So,this program has been created to help users to classify their pet/pets according to their animal species and kinds and characteristic features and breeds.
class pet:   #A class named pet is initialised(or introduced).
    attr1=input("Enter what type/kind of animal it is whether a bird,or reptile,or mammal,or rodent,etc.:")#Seven attributes are named attr1,attr2,attr3,attr4,
    attr2=input("Now please enter whether it is a dog,or cat,or snake,or parrot,etc.:")#attr5,attr6,attr7 are initialised which ask for the
    attr3=input("OK,now enter the respective breed of the pet:")#pet animal's type/kind,specific type,breed,name,weight,colour of the skin/fur,hobbies/favourite actions respectively
    attr4=input("Enter the name of your cute animal:")
    attr5=input("Enter the weight of the animal:")
    attr6=input("Now,enter the colour of the fur/skin of the animal:")
    attr7=input("Enter its hobbies/favourite actions which it likes to do daily or frequently:")
    def fun(cuddle):#A function/method named fun is created,in which a variable named cuddle is introduced.
        print("I'm a ", cuddle.attr1)
        print("I'm a ", cuddle.attr2)
        print("I'm from ",cuddle.attr3)
        print("My name is ",cuddle.attr4)
        print("My weight is ",cuddle.attr5)
        print("My fur/skin is ",cuddle.attr6)
        print("My hobbies/favoourite actions ",cuddle.attr7)
# Object instantiation/initialisation
hidear = pet()
 
# Accessing class attributes and method through objects
print(hidear.attr1)
print(hidear.attr2)
print(hidear.attr3)
print(hidear.attr4)
print(hidear.attr5)
print(hidear.attr6)
print(hidear.attr7)
hidear.fun()
