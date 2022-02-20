from datetime import datetime, date, time, timedelta

class Publication:
    def __init__(self):
        self.header = self.create_header()
        self.text = self.create_text()
        self.footer = self.create_footer()
    __path = '..\\test.txt'

    def create_header(self):
        return 'Title\n'

    def create_text(self):
        return input('Enter your text:\n')

    def create_footer(self):
        return 'Footer\n\n'

    def add(self):
        with open(self.__path, 'a') as a_writer:
            a_writer.write(f"{self.header}{self.text}\n{self.footer}")
        print('Article published\n')

class News(Publication):
    def create_header(self):
        return 'News\n'

    def create_footer(self):
        city = input('Pleas enter the name of city:\n')
        return f"{city} {datetime.now().strftime('%d-%m-%Y %H:%M')}\n\n"

class PrivateAd(Publication):
    def create_header(self):
        return 'Private Ad\n'

    def create_footer(self):
        while True:
            try:
                expire_date = input('Please enter the day when your advertisement expires in format YYYY-MM-DD:\n')
                days_left = (datetime.strptime(expire_date, '%Y-%m-%d') - datetime.today()).days + 1
            except ValueError:
                print("Invalid input\nFor example:\nFor February 14, 2022 input should looks like 2022-2-14")
                continue
            else:
                break
        if days_left == 0:
            return f"Actual until: {expire_date}  Today is the last day. Don't miss your chance ;)\n\n"
        elif days_left > 0:
            return f"Actual until: {expire_date},  {days_left} days left.\n\n"
        else:
            return f"Actual until: {expire_date},  ad expired {days_left * -1} days ago.\n\n"

class Recipe(Publication):
    def create_header(self):
        return 'Recipe of the day\n'

    def create_footer(self):
        return f"Time to cook {input('Please enter the time needed to cook the dish:')}\n\n"


class Operator():
    def publish(self):
        choice = input("""Choose what kind of publication you want to create:\nN fo news\nP for PrivateAd\nR for Recipe\n""").lower()
        if choice not in ['n','p','r']:
            print('Your input is invalid. Please try again.')
            self.publish()
        else:
            if choice == 'n':
                pub = News()
            elif choice == 'p':
                pub = PrivateAd()
            elif choice == 'r':
                pub = Recipe()
        if 'pub' in locals():
            pub.add()
        pros =  input('Do you want to make enother publication?\nY for Yes\nN for No\n').lower()
        if pros == 'y':
            self.publish()
        elif pros == 'n':
            return print('Program ended')

x = Operator()
x.publish()
