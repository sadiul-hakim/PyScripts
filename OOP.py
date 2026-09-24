class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(self.__class__)
        print("Animal")


Animal("Name").speak()
