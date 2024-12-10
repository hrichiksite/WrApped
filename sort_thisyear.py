import json
import re

#import json file
with open('result.json') as f:
    data = json.load(f)
    load_data_chats = data.keys()
    load_data_chats = list(load_data_chats)
    load_data_chats_messages = []
    for chat in load_data_chats:
        load_data_chats_messages.append(data[chat]['messages'].keys())
    
    #print the chat names and the number of messages in each chat
    total_message_count = 0
    message_count_list = []
    for i in range(len(load_data_chats)):
        #print(load_data_chats[i])
        total_message_count += len(load_data_chats_messages[i])
        if(data[load_data_chats[i]]['name'] != None):
            message_count_list.append((data[load_data_chats[i]]['name'], len(load_data_chats_messages[i])))
        else:
            message_count_list.append((load_data_chats[i], len(load_data_chats_messages[i])))
    message_count_list.sort(key=lambda x: x[1], reverse=True)

    #edge case - if a contact has multiple numbers saved
    # if the chat name is a variation of the other as in User (1) and User (2)
    # then combine the messages of the two chats
    
    for i in range(len(message_count_list)):
        if('(' in message_count_list[i][0]):
            for j in range(i+1, len(message_count_list)):
                if('(' in message_count_list[j][0]):
                    if(message_count_list[i][0].split('(')[0] == message_count_list[j][0].split('(')[0]):
                        message_count_list[i] = (message_count_list[i][0].split('(')[0], message_count_list[i][1] + message_count_list[j][1])
                        message_count_list[j] = ('REMOVED_CHAT', 0)
    txt_file = open("thisyear.txt", "w", encoding='utf-8')
    for chat in message_count_list:
        if(chat[0] == 'REMOVED_CHAT'):
            continue
        txt_file.write(chat[0] + " " + str(chat[1]) + "\n")
    txt_file.close()
    
    print("Total messages: ", total_message_count)

    #calculate the number of messages sent and received
    sent_messages = 0
    received_messages = 0

    for i in range(len(load_data_chats)):
        for message in load_data_chats_messages[i]:
            if(data[load_data_chats[i]]['messages'][message]['from_me']):
                received_messages += 1
            else:
                sent_messages += 1

    print("Sent messages: ", sent_messages)
    print("Received messages: ", received_messages)

    #calculate the number of unique words sent and received total

    all_words = []

    for i in range(len(load_data_chats)):
        #can be nonetype
        
        for message in load_data_chats_messages[i]:
            if(data[load_data_chats[i]]['messages'][message]['media']):
                continue
            if(data[load_data_chats[i]]['messages'][message]['key_id'].startswith('call:')):
                continue
            if(data[load_data_chats[i]]['messages'][message]['data'] == None):
                continue
            all_words += data[load_data_chats[i]]['messages'][message]['data'].split()

    unique_words = set(all_words)
    print("Unique words used: ", len(unique_words))

    # most used words
    word_count = {}
    for word in all_words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    
    print("Most used words: ", word_count[:10])

    #calculate the most used word by me
    my_words = []
    for i in range(len(load_data_chats)):
        for message in load_data_chats_messages[i]:
            if(data[load_data_chats[i]]['messages'][message]['from_me']):
                if(data[load_data_chats[i]]['messages'][message]['media']):
                    continue
                if(data[load_data_chats[i]]['messages'][message]['key_id'].startswith('call:')):
                    continue
                if(data[load_data_chats[i]]['messages'][message]['data'] == None):
                    continue
                my_words += data[load_data_chats[i]]['messages'][message]['data'].split()

    my_word_count = {}
    for word in my_words:
        if word in my_word_count:
            my_word_count[word] += 1
        else:
            my_word_count[word] = 1
    
    my_word_count = sorted(my_word_count.items(), key=lambda x: x[1], reverse=True)

    print("Most used words by me: ", my_word_count[:10])

    #calculate the most used word by the other person
    other_words = []

    for i in range(len(load_data_chats)):
        for message in load_data_chats_messages[i]:
            if(not data[load_data_chats[i]]['messages'][message]['from_me']):
                if(data[load_data_chats[i]]['messages'][message]['media']):
                    continue
                if(data[load_data_chats[i]]['messages'][message]['key_id'].startswith('call:')):
                    continue
                if(data[load_data_chats[i]]['messages'][message]['data'] == None):
                    continue
                other_words += data[load_data_chats[i]]['messages'][message]['data'].split()

    
    other_word_count = {}
    for word in other_words:
        if word in other_word_count:
            other_word_count[word] += 1
        else:
            other_word_count[word] = 1

    #remove not useful words
    not_useful_words = ['the', '<br>', 'to', 'and', 'I\'m', 'You', 'a', 'I', 'i', 'is', 'in', 'for', 'of', 'it', 'that', 'on', 'with', 'you', 'this', 'are', 'be', 'have', 'not', 'was', 'or', 'as', 'at', 'but', 'if', 'so', 'me']
    for word in not_useful_words:
        if word in other_word_count:
            del other_word_count[word]


    
    other_word_count = sorted(other_word_count.items(), key=lambda x: x[1], reverse=True)

    print("Most used words by the other person: ", other_word_count[:10])

    #how many times did i wish gm

    gm_count = 0
    for i in range(len(load_data_chats)):
        for message in load_data_chats_messages[i]:
            if(data[load_data_chats[i]]['messages'][message]['from_me']):
                msg_data = data[load_data_chats[i]]['messages'][message]['data']
                msg_data = str(msg_data).lower()
                if(msg_data.__contains__('gm')):
                    gm_count += 1
    print("gm count: ", gm_count)

    #how many times did i wish gn

    gn_count = 0
    for i in range(len(load_data_chats)):
        for message in load_data_chats_messages[i]:
            if(data[load_data_chats[i]]['messages'][message]['from_me']):
                msg_data = data[load_data_chats[i]]['messages'][message]['data']
                msg_data = str(msg_data).lower()
                if(msg_data.__contains__('gn')):
                    gn_count += 1
    print("gn count: ", gn_count)

    #minutes spent on call
    # calls have the data 'A voice call to [number] was initiated and lasted for 07:31 minutes with 1.76 MB data transferred.'
    
    
    call_minutes = 0
    call_count = 0
    for i in range(len(load_data_chats)):
        for message in load_data_chats_messages[i]:
            if(data[load_data_chats[i]]['messages'][message]['key_id'].startswith('call:')):
                #ignore missed calls 'was not answered'
                if(data[load_data_chats[i]]['messages'][message]['data'].__contains__(' was initiated and lasted for ')):
                
                    match = re.search(r'(\d{2}):(\d{2})', data[load_data_chats[i]]['messages'][message]['data'])
                    call_count += 1

                    if match:
                        #print(data[load_data_chats[i]]['messages'][message]['data'])
                        #print(match.group(1))
                        #print(match.group(2))
                        minutes = int(match.group(1))  # Get the minutes part
                        seconds = int(match.group(2))  # Get the seconds part
                        total_seconds = minutes * 60 + seconds
                        #print("Total seconds:", total_seconds)
                        call_minutes += total_seconds / 60
    print("Call minutes: ", call_minutes)
    print("Call count: ", call_count)
    #average call duration
    if(call_count != 0):
        print("Average call duration: ", call_minutes / call_count)
    else:
        print("Average call duration: 0")

    # most called person
    call_count_dict = {}
    for i in range(len(load_data_chats)):
        for message in load_data_chats_messages[i]:
            if(data[load_data_chats[i]]['messages'][message]['key_id'].startswith('call:')):
                #only count the initiated calls
                if(data[load_data_chats[i]]['messages'][message]['data'].__contains__(' was initiated and lasted for ')):
                    
                    call_number = data[load_data_chats[i]]['messages'][message]['sender']
                    if call_number in call_count_dict:
                        call_count_dict[call_number] += 1
                    else:
                        call_count_dict[call_number] = 1

    call_count_dict = sorted(call_count_dict.items(), key=lambda x: x[1], reverse=True)
    print("Most called person: ", call_count_dict[:10])

    #minutes spent on arguing with someone
    #arguing is subjective
    #if the messages are sent in quick succession then it is an argument
    
    argument_minutes = 0
    argument_count = 0
    for i in range(len(load_data_chats)):
        message_time = []
        for message in load_data_chats_messages[i]:
            message_time.append(data[load_data_chats[i]]['messages'][message]['timestamp'])
        message_time.sort()
        for j in range(1, len(message_time)):
            if(message_time[j] - message_time[j-1] < 60000):
                argument_count += 1
                argument_minutes += (message_time[j] - message_time[j-1]) / 60000
    print("Argument minutes: ", argument_minutes)
    print("Argument count: ", argument_count)

    #how many times did i say sorry
    sorry_count = 0
    for i in range(len(load_data_chats)):
        for message in load_data_chats_messages[i]:
            if(data[load_data_chats[i]]['messages'][message]['from_me']):
                msg_data = data[load_data_chats[i]]['messages'][message]['data']
                msg_data = str(msg_data).lower()
                if(msg_data.__contains__('sorry')):
                    sorry_count += 1
    print("Sorry count: ", sorry_count)

    #minutes spent on texting
    text_minutes = 0
    text_count = 0
    #assume that the time between messages is the time spent texting, 
    #when the time between messages is greater than 5 minutes, it is not considered texting,
    #just pad the time with 5 minutes
    
    for i in range(len(load_data_chats)):
        message_time = []
        for message in load_data_chats_messages[i]:
            message_time.append(data[load_data_chats[i]]['messages'][message]['timestamp'])
        message_time.sort()
        for j in range(1, len(message_time)):
            if(message_time[j] - message_time[j-1] < 300000):
                text_count += 1
                text_minutes += (message_time[j] - message_time[j-1]) / 60000
            else:
                text_minutes += 5
    print("Text minutes: ", text_minutes)
    print("Text count: ", text_count)
    
    #random stats
    #how many times did i say lol
    lol_count = 0
    for i in range(len(load_data_chats)):
        for message in load_data_chats_messages[i]:
            if(data[load_data_chats[i]]['messages'][message]['from_me']):
                msg_data = data[load_data_chats[i]]['messages'][message]['data']
                msg_data = str(msg_data).lower()
                if(msg_data.__contains__('lol')):
                    lol_count += 1
    print("lol count: ", lol_count)
    

    #total character count
    total_char_count = 0
    for i in range(len(load_data_chats)):
        for message in load_data_chats_messages[i]:
            if(data[load_data_chats[i]]['messages'][message]['data'] != None):
                total_char_count += len(data[load_data_chats[i]]['messages'][message]['data'])

    print("Total character count: ", total_char_count)
    


    





