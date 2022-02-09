import string

homework = '''homEwork:

  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.'''

# Split text into sentences.
splited_text = homework.split('.')
#print(splited_text) # Test

# Capitalizing every sentence.
capitalized_splited_text = []
for sentence in splited_text:
    for id, char in enumerate(sentence):
        if char.isalpha():
            break
    capitalized_splited_text.append(sentence[:id] + sentence[id:].capitalize())
#print(capitalized_splited_text) # Test
capitalized_text = '.'.join(capitalized_splited_text)

# Capitalizing new line after ':'.
# Could be improved to react to all colons, not just the first one.
if ':' in capitalized_text:
    for id, char in enumerate(capitalized_text):
        if ':' in capitalized_text[:id] and capitalized_text[id].isalpha():
            x = capitalized_text[:id] + capitalized_text[id].upper() + capitalized_text[id+1:]
            capitalized_text = x
            break
#print(capitalized_text) # Test

# Initialization a sentence from the last words.
sentence_from_last_words = ''
for sentence in capitalized_text.split('.'):
    if len(sentence) > 0:
        word_id = -1
        while sentence.split(' ')[word_id].isdigit() == True:
            word_id -= 1
            if -word_id == len(sentence):
                break
        sentence_from_last_words += ' ' + sentence.split(' ')[word_id]
sentence_from_last_words = ' ' + sentence_from_last_words.strip(' ').capitalize() + '.'
#print(sentence_from_last_words) # Test

# Final text.
result = capitalized_text.replace('add it to the end of this paragraph.', f'add it to the end of this paragraph.{sentence_from_last_words}')
result =  result.replace(' iz ', ' is ')
print(result)

# Whitespace counter.
counter = 0
for char in result:
    if char in string.whitespace:
        counter += 1
print('\n This text has ' + str(counter) + ' whitespaces')
