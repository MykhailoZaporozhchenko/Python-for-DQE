from datetime import datetime, date, time, timedelta

class Publication:
    def __init__(self):
        self.header = 'Title\n'
        self.footer = 'Footer\n\n'
        self.text = input('Enter your text: ')
    __path = '..\\test.txt'

    def add(self):

        with open(self.__path, 'a') as a_writer:
            a_writer.write(f"{self.header}{self.text}\n{self.footer}")

class News(Publication):
    def __init__(self):
        self.header = 'News\n'
        self.footer = f"{input('Pleas enter the name of city: ')} {datetime.now().strftime('%d-%m-%Y %H:%M')}\n\n"
        self.text = input('Enter your text: ')

class PrivateAd(Publication):
    def __init__(self):
        self.header = 'Private Ad\n'
        self.expire_date = input('Please enter the day when your advertisement expires in format YYYY-MM-DD: ')
        # how to check is input correct
        self.footer = f"Actual until: {self.expire_date},  {(datetime.strptime(expire_date, '%Y-%m-%d') - datetime.today()).days + 1} days left\n\n"
        self.text = input('Enter your text: ')


class Recipe(Publication):
    def __init__(self):
        self.header = 'Recipe of the day\n'
        self.footer = f"Time to cook {input('Please enter the time needed to cook the dish:')}\n\n"
        self.text = input('Enter your text: ')

#class Operator():
def publish():
    choice = input("""Choose what kind of publication you want to create:\nN fo news\nP for PrivateAd\nR for Recipe\n""").lower()
    if choice not in ['n','p','r']:
        print('Your input is invalid. Please try again.')
        publish()
    else:
        if choice == 'n':
            pub = News()
        elif choice == 'p':
            pub = PrivateAd()
        elif choice == 'r':
            pub = Recipe()
    pub.add()
    pros =  input('Do you want to make enother publication?\nY for Yes\nN for No\n').lower()
    if pros == 'y':
        publish()
    elif pros == 'n':
        return print('Program ended')

publish()



