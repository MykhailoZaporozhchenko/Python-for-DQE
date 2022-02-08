import string

homework = '''homEwork:

  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.'''


# The function capitalizes every sentence and words after a colon.
def text_capitalazing(text):
    if type(text) != str:
        return print(f'Error:\nThe text_capitalazing function expects a string as an attribute. \nThe input attribute is {type(text)}')

    # Capitalizing every sentence.
    splited_text = text.split('.')
    capitalized_splited_text = []
    for sentence in splited_text:
        for id, char in enumerate(sentence):
            if char.isalpha():
                break
        capitalized_splited_text.append(sentence[:id] + sentence[id:].capitalize())
    capitalized_text = '.'.join(capitalized_splited_text)

    # Capitalizing next letter after ':'.
    temp_list = []
    splited_text = capitalized_text.split(':')
    for sentence in splited_text:
        if len(sentence) == 0:
            temp_list.append('')
        else:
            for id, char in enumerate(sentence):
                if char.isalpha():
                    break
            x = sentence[:id] + sentence[id].upper() + sentence[id + 1:]
            temp_list.append(x)
    capitalized_text = ':'.join(temp_list)

    return capitalized_text


#  The function creates a sentence from the last words of given text.
def add_sentence_from_last_words(text):
    if type(text) != str:
        return print(f'Error:\nThe add_sentence_from_last_words function expects a string as an attribute. \nThe input attribute is {type(text)}')

    sentence_from_last_words = ''
    for sentence in text.split('.'):
        if len(sentence) > 0:
            word_id = -1
            while sentence.split(' ')[word_id].isdigit() == True:
                word_id -= 1
                if -word_id == len(sentence):
                    break
            sentence_from_last_words += ' ' + sentence.split(' ')[word_id]

    sentence_from_last_words = ' ' + sentence_from_last_words.strip(' ').capitalize() + '.'

    # Could be changed so the function returns only the sentence
    # And the user should add it wherever he wants. Since there are no clear instructions in the task, I did it like this.
    return text.replace('add it to the end of this paragraph.', f'add it to the end of this paragraph.{sentence_from_last_words}')


# The function replaces 'is' with 'is'
def iz_replace(text):
    if type(text) != str:
        return print(f'Error:\nThe iz_replace function expects a string as an attribute. \nThe input attribute is {type(text)}')
    return text.replace(' iz ', ' is ')


# Whitespace counter.
def whitespace_counter(text):
    counter = 0
    for char in text:
        if char in string.whitespace:
            counter += 1
    return f'\nThis text has {str(counter)} whitespaces.'


final_text = text_capitalazing(homework)
final_text = add_sentence_from_last_words(final_text)
final_text = iz_replace(final_text)
print(final_text)
print(whitespace_counter(final_text))
