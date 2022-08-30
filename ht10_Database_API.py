import json
from datetime import datetime, date, time, timedelta
import fileinput
import string
import csv
import re
import os
import xml.etree.ElementTree as ET
from ht4_2 import text_capitalazing, iz_replace
import pyodbc

output_path = '..\\Magazine.txt'
source_path = '..\\Publication.txt'
json_source_path = '..\\Publication.json'
xml_source_path = '..\\Publication.xml'

def FYI():
    print(f"""Current path for all publication is {output_path}
Current path for the source txt file from which new posts are taken and added to the Journal is {source_path}
Current path for the source json file is {json_source_path}
Current path for the source xml file is {xml_source_path}
Current path for the source data base is magazine.db
""")
    print("""           XML
The source xml file should be in .xml extension and consist data if folowing format:
<root>
    <publication name='News'>
        <body>News text</body>
        <foot>City</foot>
    </publication>
    <publication name='PrivateAd'>
        <body>PrivateAd text</body>
        <foot>YYYY-MM-DD</foot>
    </publication>
</root>

Each <publication> tag is a separate post and must contain atribute name = 'News', 'PrivateAd' or 'Recipe'.
Each publication has to contain <body> and <foot> as cild tags for publication text and footer respectively.
The text of the publication cannot be an empty space.
The day when advertisement expires must be in the correct format and cannot be a date that has already passed.
--------------------------------------------------------------------------------------------------------------

           JSON
The source json file should be in .json extension and consist data if folowing format:
One publication:
{"head": "PrivateAd", "body": "PrivateAd text", "foot": "YYYY-MM-DD"}

Several publications:
[
    {"head": "News", "body": "News text", "foot": "City"}
,  {"head": "PrivateAd", "body": "PrivateAd text", "foot": "YYYY-MM-DD"}
,  {"head": "Recipe", "body": "Recipe text", "foot": "Time to cook"}
]

The text of the publication cannot be an empty space.
The day when advertisement expires must be in the correct format and cannot be a date that has already passed.
--------------------------------------------------------------------------------------------------------------

            TXT
The source txt file should be in .txt extension and consist data if folowing format:
News--News text--City
PrivateAd--PrivateAd text--YYYY-MM-DD
Recipe--Recipe text--Time to cook

Each line is a separate post and must begin with 'News', 'PrivateAd' or 'Recipe'.
'--' is the separator between the header, text and the footer.
The text of the publication cannot be an empty space.
The day when advertisement expires must be in the correct format and cannot be a date that has already passed.
--------------------------------------------------------------------------------------------------------------
""")


class Publication:
    def __init__(self, head = '', body = '', foot = ''):
        self.header = self.create_header(head)
        self.text = self.create_text(body)
        self.footer = self.create_footer(foot)
        self.path = output_path

    def create_header(self, head):
        return 'Title\n'

    def create_text(self, text):
        if text == '':
            while text == '':
                text = input('Enter your text:\n')
                if text == '':
                    print("You haven't enter any text, please try again")
        return f"{text}\n"

    def create_footer(self, foot):
        return 'Footer\n\n'

    def add(self):
        with open(self.path, 'a') as a_writer:
            a_writer.write(f"{self.header}{self.text}{self.footer}")
        print('Article published')
        add_pub_to_DB(self.header, self.text, self.footer)

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
                    if days_left < 0:
                        print('The specified date has already passed. Please enter a valid date.')
                    else:
                        break
        days_left = (datetime.strptime(expire_date, '%Y-%m-%d') - datetime.today()).days + 1
        if days_left == None:
            raise ValueError("Incorrect dataformat")
        elif days_left <0:
            raise ValueError("The specified date has already passed")
        if days_left == 0:
            return f"Actual until: {expire_date}.  Today is the last day. Don't miss your chance ;)\n\n"
        elif days_left > 0:
            return f"Actual until: {expire_date},  {days_left} days left.\n\n"

class Recipe(Publication):
    def create_header(self, head = ''):
        return 'Recipe of the day\n'

    def create_footer(self, foot = ''):
        if foot == '':
            foot = input('Please enter the time needed to cook the dish:')
        return f"Time to cook {foot}\n\n"


class Operator():
    def start(self):
        choice = input("""Do you whant to make publication by console input, from txt file input, json input or xml input?
C for console input\nF for from txt file\nJ for json file input\nX for xml file input\nI to view info\nS for change settings\n""").lower()
        if choice not in ['c', 'f', 'i', 's', 'j', 'x']:
            print('Your input is invalid. Please try again.')
            self.start()
        else:
            if choice == 'c':
                self.publish()
            elif choice == 'f':
                self.file_publish()
            elif choice == 'i':
                FYI()
                self.start()
            elif choice == 's':
                self.set_settings()
            elif choice == 'j':
                self.json_publish()
            elif choice == 'x':
                self.xml_publish()

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

    def file_publish(self):
        for line in fileinput.input(files= source_path):
            splt_line = line.split('--')
            head = splt_line[0]
            body = iz_replace(text_capitalazing(splt_line[1]))
            x = splt_line[2]
            if x[-1] == '\n':
                foot = x[:len(x) - 1]
            else:
                foot = splt_line[2]
            if head == 'News':
                pub = News(body=body, foot=foot)
                pub.add()
            elif head == 'PrivateAd':
                pub = PrivateAd(body=body, foot=foot)
                pub.add()
            elif head == 'Recipe':
                pub = Recipe(body=body, foot=foot)
                pub.add()

    def set_settings(self):
        global source_path
        global output_path
        global json_source_path
        global xml_source_path
        print(f"""Current path for all publication is {output_path}
Current path for the source txt file is {source_path}
Current path for the source json file is {json_source_path}
Current path for the source xml file is {xml_source_path}""")
        setting = input("""O for change path to output\nS for change path to txt source
J for change path to json source\nX for change path to xml source
P to proceed without any changes\n""").lower()
        if setting not in ['o', 's', 'p','j', 'x']:
            print('Your input is invalid. Please try again.')
            self.set_settings()
        else:
            if setting == 'o':
                output_path = input('Please enter new path for output publications\n')
                proceed = input('Do You also want to chande path to source?\nY/N\n').lower()
                if proceed == 'y':
                    source_path = input('Please enter new path for the source file\n')
                    self.start()
                else:
                    self.start()
            elif setting == 's':
                source_path = input('Please enter new path for the source txt file\n')
                proceed = input('Do You also want to chande path for output publications?\nY/N\n').lower()
                if proceed == 'y':
                    output_path = input('Please enter new path to the output file\n')
                    self.start()
                else:
                    self.start()
            elif setting == 'p':
                self.start()

            if setting == 'j':
                json_source_path = input('Please enter new path for the json source\n')
                proceed = input('Do You also want to chande path for output publications?\nY/N\n').lower()
                if proceed == 'y':
                    output_path = input('Please enter new path to the output file\n')
                    self.start()
                else:
                    self.start()

            if setting == 'x':
                xml_source_path = input('Please enter new path for the json source\n')
                proceed = input('Do You also want to chande path for output publications?\nY/N\n').lower()
                if proceed == 'y':
                    output_path = input('Please enter new path to the output file\n')
                    self.start()
                else:
                    self.start()

    def json_publish(self):
        try:
            json_input = json.load(open(json_source_path))

            if type(json_input) == list:
                for element in json_input:
                    head = element['head']
                    body = iz_replace(text_capitalazing(element['body']))
                    x = element['foot']
                    if x[-1] == '\n':
                        foot = x[:len(x) - 1]
                    else:
                        foot = element['foot']
                    if head == 'News':
                        pub = News(body=body, foot=foot)
                        pub.add()
                    elif head == 'PrivateAd':
                        pub = PrivateAd(body=body, foot=foot)
                        pub.add()
                    elif head == 'Recipe':
                        pub = Recipe(body=body, foot=foot)
                        pub.add()

            if type(json_input) == dict:
                head = json_input['head']
                body = iz_replace(text_capitalazing(json_input['body']))
                x = json_input['foot']
                if x[-1] == '\n':
                    foot = x[:len(x) - 1]
                else:
                    foot = json_input['foot']
                if head == 'News':
                    pub = News(body=body, foot=foot)
                    pub.add()
                elif head == 'PrivateAd':
                    pub = PrivateAd(body=body, foot=foot)
                    pub.add()
                elif head == 'Recipe':
                    pub = Recipe(body=body, foot=foot)
                    pub.add()

        except:
            print("Something went wrong. Try to read Info or reach code writer for clarification\n")
            self.start()
        else:
            os.remove(json_source_path)
            print('json source file deleted')

    def xml_publish(self):
        try:
            xml_file = ET.parse(xml_source_path)
            root = xml_file.getroot()

            for publication in root:
                body_element = iz_replace(text_capitalazing(publication.find('body').text))
                foot_element = publication.find('foot').text
                if publication.get('name') == 'News':
                    pub = News(body=body_element, foot=foot_element)
                    pub.add()
                elif publication.get('name') == 'PrivateAd':
                    pub = PrivateAd(body=body_element, foot=foot_element)
                    pub.add()
                elif publication.get('name') == 'Recipe':
                    pub = Recipe(body=body_element, foot=foot_element)
                    pub.add()
        except:
            print("Something went wrong. Try to read Info or reach code writer for clarification\n")
            self.start()
        else:
            os.remove(xml_source_path)
            print('xml source file deleted')

def words_statistic():
    word_dict = {}
    with open( output_path, 'r') as magazine:
        text = magazine.read()
        row_list = re.sub("[^\w']", " ", text).split()
        temp_str = ''
        for item in row_list:
            temp_str += item + ' '
        word_list = re.sub("[\d]", " ", temp_str).split()
        for idx, item in enumerate(word_list):
            word_list[idx] = item.lower().strip("'")
        for word in word_list:
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1

    with open('..\\WordsStatistic.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='-')
        for key in list(word_dict.keys()):
            writer.writerow([key, word_dict[key]])

def letter_statistic():
    matrix = {}
    alphabet_string = string.ascii_lowercase
    alphabet_list = list(alphabet_string)
    for letter in alphabet_list:
        matrix[letter] = [0,0,0.0]

    with open( output_path, 'r') as magazine:
        text = magazine.read()
        letters_counter = 0
        for character in text:
            if character.isalpha():
                letters_counter += 1
                matrix[character.lower()][0] += 1
                if character == character.upper():
                    matrix[character.lower()][1] += 1
        for key in  list(matrix.keys()):
            if matrix[key][0] == 0:
                del matrix[key]
        for key in list(matrix.keys()):
            matrix[key][2] = round((matrix[key][0] / letters_counter * 100), 2)

    with open('..\\LetterStatistic.csv', 'w', newline='') as csvfile:
        headers = ['letter', 'cout_all', 'count_uppercase', 'percentage']
        writer = csv.DictWriter(csvfile, fieldnames= headers)
        writer.writeheader()
        for key in list(matrix.keys()):
            writer.writerow({'letter':key, 'cout_all':matrix[key][0], 'count_uppercase':matrix[key][1], 'percentage':matrix[key][2]})




def add_pub_to_DB(header, text, footer):
    connection = pyodbc.connect("DRIVER={SQLite3 ODBC Driver};Direct=True;Database=magazine.db;String Types= Unicode")
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS news
                 (city text, date text, news_text text)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS private_ad
                 (actual_until text, days_left text, ad_text text)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS recipe
                 (cooking_time text, recipe_text text)''')

    if header == 'News\n':
        splitted_footer = footer.split()
        pub_time = splitted_footer[-2] + ' ' + splitted_footer[-1]
        pub_city = ' '.join(splitted_footer[0:-2])

        cursor.execute(f"""INSERT INTO news VALUES ('{pub_city}'
        , '{pub_time}'
        , '{text[:-1]}')""")

        cursor.execute('SELECT * FROM news')
        result = cursor.fetchall()
        last_row = result[-1]
        if last_row in result[:-1]:
            print(f"Row {last_row} is a duplicate. It isn't added to the news table\n")
            connection.rollback()
        else:
            print('Row added to the news table\n')
            connection.commit()

    elif header == 'Private Ad\n':
        splitted_footer = footer.split()
        pub_date = splitted_footer[2][:-1]
        if splitted_footer[3] == 'Today':
            pub_days_left = 'Today is the last day.'
        else:
            pub_days_left = splitted_footer[3]

        cursor.execute(f"""INSERT INTO private_ad VALUES ('{pub_date}'
        , '{pub_days_left}'
        , '{text[:-1]}')""")

        cursor.execute('SELECT * FROM private_ad')
        result = cursor.fetchall()
        last_row = result[-1]
        if last_row in result[:-1]:
            print(f"Row {last_row} is a duplicate. It isn't added to the private_ad table\n")
            connection.rollback()
        else:
            print('Row added to the private_ad table\n')
            connection.commit()

    elif header == 'Recipe of the day\n':
        cursor.execute(f"""INSERT INTO recipe VALUES ('{footer[13:-2]}'
            , '{text[:-1]}')""")

        cursor.execute('SELECT * FROM recipe')
        result = cursor.fetchall()
        last_row = result[-1]
        if last_row in result[:-1]:
            print(f"Row {last_row} is a duplicate. It isn't added to the recipe table\n")
            connection.rollback()
        else:
            print('Row added to the recipe table\n')
            connection.commit()

    cursor.close()
    connection.close()


x = Operator()
x.start()

words_statistic()
letter_statistic()
