from datetime import datetime, date, time, timedelta
import fileinput
from ht4_2 import text_capitalazing, iz_replace

class Publication:
    def __init__(self, head = '', body = '', foot = ''):
        self.header = self.create_header(head)
        self.text = self.create_text(body)
        self.footer = self.create_footer(foot)
    __path = '..\\test.txt'

    def create_header(self, head):
        return 'Title\n'

    def create_text(self, text):
        if text == '':
            text = input('Enter your text:\n')
        return f"{text}\n"

    def create_footer(self, foot):
        return 'Footer\n\n'

    def add(self):
        with open(self.__path, 'a') as a_writer:
            a_writer.write(f"{self.header}{self.text}{self.footer}")
        print('Article published\n')

class News(Publication):
    def create_header(self, head = ''):
        return 'News\n'

    def create_footer(self, foot = ''):
        if foot == '':
            foot = input('Pleas enter the name of city:\n')
        return f"{foot} {datetime.now().strftime('%d-%m-%Y %H:%M')}\n\n"

class PrivateAd(Publication):
    def create_header(self, head = ''):
        return 'Private Ad\n'

    def create_footer(self, expire_date = ''):
        if expire_date == '':
            while True:
                try:
                    expire_date = input('Please enter the day when your advertisement expires in format YYYY-MM-DD:\n')
                    days_left = (datetime.strptime(expire_date, '%Y-%m-%d') - datetime.today()).days + 1
                except ValueError:
                    print("Invalid input\nFor example:\nFor February 14, 2022 input should looks like 2022-2-14")
                    continue
                else:
                    break
        else:
            days_left = (datetime.strptime(expire_date, '%Y-%m-%d') - datetime.today()).days + 1
        if days_left == 0:
            return f"Actual until: {expire_date}  Today is the last day. Don't miss your chance ;)\n\n"
        elif days_left > 0:
            return f"Actual until: {expire_date},  {days_left} days left.\n\n"
        else:
            return f"Actual until: {expire_date},  ad expired {days_left * -1} days ago.\n\n"

class Recipe(Publication):
    def create_header(self, head = ''):
        return 'Recipe of the day\n'

    def create_footer(self, foot = ''):
        if foot == '':
            foot = input('Please enter the time needed to cook the dish:')
        return f"Time to cook {foot}\n\n"


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

    def file_publish(selfself):
        for line in fileinput.input(files='Publication.txt'):
            splt_line = line.split('--')
            head = splt_line[0]
            body = iz_replace(text_capitalazing(splt_line[1]))
            foot = splt_line[2]
            if head == 'News':
                pub = News(body = body, foot = foot)
                pub.add()
            elif head == 'PrivateAd':
                pub = PrivateAd(body=body, foot=foot)
                pub.add()
            elif head == 'Recipe':
                pub = Recipe(body=body, foot=foot)
                pub.add()

    def start(self):
        choice = input("""Do you whant to make publication by console input or from file:\nI for console input\nF for from file\n""").lower()
        if choice not in ['i', 'f']:
            print('Your input is invalid. Please try again.')
            self.start()
        else:
            if choice == 'i':
                self.publish()
            elif choice == 'f':
                self.file_publish()


import fileinput
for line in fileinput.input(files='Publication.txt'):
    print(line)

x = Operator()
x.start()
