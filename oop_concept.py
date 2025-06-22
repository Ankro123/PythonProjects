class Animal:
    def __init__(self, name:str) -> None:
        self.name = name
    
    def eat(self):
        print(f'{self.name} is eating')
        
    def speak(self):
        print(f'{self.name} is speaking')
        
        
class Dog(Animal):
    
    def __init__(self, name:str, breed:str) -> None:
        super().__init__(name)
        self.__breed = breed
    
    def speak(self):
        print(f'Dog named {self.name} of breed {self.__breed} is WOOFing')
        
if __name__ == "__main__":
    dog1 = Animal('Soumil')
    dog1.speak()