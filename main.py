
from io import StringIO
from json.decoder import JSONDecoder
from os import path
import json
import re
import ssl
from sqlalchemy.sql.expression import delete, false, true
import telebot
from telebot.types import Message
from db.queries import *
from aiohttp import web
import copy

# Finding the absolute path of the config file
scriptPath = path.abspath(__file__)
dirPath = path.dirname(scriptPath)
configPath = path.join(dirPath,'config.json')

config = json.load(open(configPath,encoding='utf8'))
language = json.load(open(config['language'],encoding='utf8'))

bot = telebot.TeleBot(config['botToken'], parse_mode='HTML')




# Main reply keyboard
def mainReplyKeyboard(userLanguage):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    button1 = telebot.types.KeyboardButton(text=language[userLanguage]['courses'])
    button2 = telebot.types.KeyboardButton(text=language[userLanguage]['sitting'])
    button3 = telebot.types.KeyboardButton(text=language[userLanguage]['contact'])
    button4 = telebot.types.KeyboardButton(text=language[userLanguage]['help'])
    
    
    keyboard.row(button1)
    keyboard.row(button2,button3, button4)

    return keyboard

# Select a Grade
def grade(message, userLanguage, called=False):
    markup = telebot.types.InlineKeyboardMarkup()
    
    markup.add(telebot.types.InlineKeyboardButton(language[userLanguage]['first'], callback_data=f'first_grade_{message.id}'), telebot.types.InlineKeyboardButton(language[userLanguage]['second'], callback_data=f'second_grade_{message.id}')) 
    markup.add(telebot.types.InlineKeyboardButton(language[userLanguage]['third'], callback_data=f'third_grade_{message.id}'), telebot.types.InlineKeyboardButton(language[userLanguage]['fourth'], callback_data=f'fourth_grade_{message.id}')) 
    markup.add(telebot.types.InlineKeyboardButton(language[userLanguage]['fifth'], callback_data=f'fifth_grade_{message.id}'))
    
    if called:
        mk=copy.deepcopy(markup)
        mk.add(telebot.types.InlineKeyboardButton(text=language[userLanguage]['back'], callback_data='grade_setting_back'))
        try:
            bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=language[userLanguage]['change_grade'],reply_markup=mk)
        except Exception:
            
            bot.send_message(message.chat.id, language[userLanguage]['change_grade'], reply_to_message_id=message.id,reply_markup=markup)
    else:
        bot.send_message(message.chat.id, language[userLanguage]['chooseGrade'],reply_to_message_id=message.id, reply_markup=markup)


def makeMarup(mdirs :str,lang,message,justDir=False):
    if justDir==False:
        ids=getMessgesIDs(mdirs)
    
        if ids:
            for id in ids:
                if id:
                    if(id[2]=='document'):
                        bot.send_document(message.chat.id,id[1])
                    elif id[2]=='media_group':
                        bot.send_video(message.chat.id,id[1])
                    elif id[2]=='text':
                        bot.send_message(message.chat.id,id[1])
                    elif id[2]=='audio':
                        bot.send_audio(message.chat.id,id[1])
                    elif id[2]=='photo':
                        bot.send_photo(message.chat.id,id[1])
                    elif id[2]=='video':
                        bot.send_video(message.chat.id,id[1])
                    elif id[2]=='video_note':
                        bot.send_video_note(message.chat.id,id[1])
                    elif id[2]=='voice':
                        bot.send_voice(message.chat.id,id[1])
                    elif id[2]=='location':
                        bot.send_location(message.chat.id,id[1])
                
                

    messages= getMessagesDir(mdirs)
    
    markup = telebot.types.InlineKeyboardMarkup()
    if messages :
        dr =list()
        for mes  in messages:
            dirctoryText=mes.dir.replace(mdirs+'/','')
            if dirctoryText!=mes.dir:
                dirctoryText=dirctoryText.split('/')[0]
                if dirctoryText not in dr :dr.append(dirctoryText)
        for i in range(0,len(dr),2):
            if len(dr)<= i+1 :
                text= dr[i]
                markup.add(telebot.types.InlineKeyboardButton(getDirName(dr=text,lang=lang), callback_data=mdirs+'/'+text))
            else :
                text= dr[i]
                text2= dr[i+1]
                markup.add(telebot.types.InlineKeyboardButton(getDirName(dr=text,lang=lang), callback_data=mdirs+'/'+text),telebot.types.InlineKeyboardButton(getDirName(text2,lang), callback_data=mdirs+'/'+text2))
    if mdirs[0:mdirs.rfind('/')]!="":
        back=mdirs[0:mdirs.rfind('/')]
        markup.add(telebot.types.InlineKeyboardButton(language[lang]['back'], callback_data=back))
    if justDir==True:
        markup.add(telebot.types.InlineKeyboardButton("paste",callback_data=f"paste_{mdirs}"))
        markup.add(telebot.types.InlineKeyboardButton(language['admin']['AddDiractory'],callback_data=f"newDir_{mdirs}"))
    
    return markup
                
    
def checkDir(dirs:str):
    dirList=dirs.split('/') if len(dirs.split('/'))>0 else [dirs]
    for d in dirList:
        if checkDirCode(d)!= True:
            return [d,checkDirCode(d)]
    return True

def dirMarkup(codeNames):
    markup = telebot.types.InlineKeyboardMarkup()
    if  codeNames[1][0]:
        markup.add(telebot.types.InlineKeyboardButton('العربية', switch_inline_query_current_chat=f'$i/ar/{codeNames[0]}/()'))  
    if codeNames[1][1]:
        markup.add(telebot.types.InlineKeyboardButton('English', switch_inline_query_current_chat=f'$i/en/{codeNames[0]}/()'))
    return markup
def insertMessageID(dr:str,message:telebot.types.Message):
    
    if(message.content_type=='document'):
        insertMessageId(dr,message.chat.id,message.document.file_id,message.content_type)
    elif message.content_type=='text':
        insertMessageId(dr,message.chat.id,message.text,message.content_type)
    elif message.content_type=='audio':
        insertMessageId(dr,message.chat.id,message.audio.file_id,message.content_type)
    elif message.content_type=='photo':
        insertMessageId(dr,message.chat.id,message.photo.__str__,message.content_type)
    elif message.content_type=='video':
        insertMessageId(dr,message.chat.id,message.video.file_id,message.content_type)
    elif message.content_type=='video_note':
        insertMessageId(dr,message.chat.id,message.video_note.file_id,message.content_type)
    elif message.content_type=='voice':
        insertMessageId(dr,message.chat.id,message.voice.file_id,message.content_type)
    elif message.content_type=='location':
        insertMessageId(dr,message.chat.id,message.voice.file_id,message.content_type)
    bot.send_message(message.chat.id,language['admin']['messageInserted'],reply_to_message_id=message.id)


def forwardContact(message):
    bot.forward_message('-1001451209844',message.chat.id,message.id)
    bot.reply_to(message,language['ar']['grade_selected'])

def changeSetting(userLanguage:str,message):
    markup  = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    markup.add(telebot.types.InlineKeyboardButton(language[userLanguage]['addIndex']), telebot.types.InlineKeyboardButton(language[userLanguage]['patchNews'])) 
    markup.add(telebot.types.InlineKeyboardButton(language[userLanguage]['back']),telebot.types.InlineKeyboardButton(language[userLanguage]['colNews'])) 
   
    bot.send_message(message.chat.id,text=language[userLanguage]['chooseSetting'],reply_markup=markup)
def saveIndex(message):
    setIndex(message.from_user.id,message.text)
    bot.send_message(message.chat.id,language['ar']['grade_selected'])


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id !=config['chatId'] :
        if not setAccount(message.from_user.id,message.chat.id):
            lang=getLanguage(message.from_user.id)
            bot.send_message(message.chat.id,text=language[lang]['greet'].format(message.from_user.first_name),reply_markup=mainReplyKeyboard(lang),disable_web_page_preview=True)
            grade(message,lang)
        elif(not checkInfo(message.from_user.id,"Lev")):
            lang=getLanguage(message.from_user.id)
            bot.send_message(message.chat.id,text=language[lang]['greetComBack'].format(message.from_user.first_name),reply_markup=mainReplyKeyboard(lang),disable_web_page_preview=True)
            grade(message,lang,True)
    else:
        bot.send_message(message.chat.id,"start command is for bot frontend only 👾",reply_to_message_id=message.id)

@bot.message_handler(commands=['help'])
def help(message):
    if message.chat.id== config['chatId']:
        bot.send_message(message.chat.id,language[getLanguage(message.from_user.id)]['adminHelp'])
    else:
        bot.send_message(message.chat.id,language[getLanguage(message.from_user.id)]['helpMessage'])

@bot.message_handler(commands=['admin'])
def admin(messege):
    if messege.chat.id==config['chatId']:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        button1 = telebot.types.KeyboardButton(text=language['admin']['addDir'])
        button2 = telebot.types.KeyboardButton(text=language['admin']['updateDir'])
        button3 = telebot.types.KeyboardButton(text=language['admin']['delDir'])

        button4 = telebot.types.KeyboardButton(text=language['admin']['addMess'])
        button5 = telebot.types.KeyboardButton(text=language['admin']['updateMess'])
        button6 = telebot.types.KeyboardButton(text=language['admin']['delMess'])

        button7 = telebot.types.KeyboardButton(text=language['admin']['sendNews'])
        
        keyboard.row(button1,button2,button3)
        keyboard.row(button4,button5,button6)
        keyboard.row(button7)

        bot.send_message(messege.chat.id,'⚙️ admin commands running...',reply_markup=keyboard)
    
# Callback handler
@bot.callback_query_handler(func=lambda call: True)
def callbackHandler(call:telebot.types.CallbackQuery):
    lang=getLanguage(call.message.from_user.id)
    if call.data[:11] == 'first_grade':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(language[lang]['it'],callback_data='IT_1'))
        markup.add(telebot.types.InlineKeyboardButton(language[lang]['department'],callback_data='Dep_1'))
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        bot.send_message(call.message.chat.id,text=language[lang]['choos_department'],reply_markup=markup)
        
    elif call.data[:12] == 'second_grade':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(language[lang]['it'],callback_data='IT_2'))
        markup.add(telebot.types.InlineKeyboardButton(language[lang]['department'],callback_data='Dep_2'))        
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        bot.send_message(call.message.chat.id,text=language[lang]['choos_department'],reply_markup=markup)
    elif call.data[:11] == 'third_grade':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(language[lang]['it'],callback_data='IT_3'))
        markup.add(telebot.types.InlineKeyboardButton(language[lang]['department'],callback_data='Dep_3'))
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        bot.send_message(call.message.chat.id,text=language[lang]['choos_department'],reply_markup=markup)

    elif call.data[:12] == 'fourth_grade':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(language[lang]['it'],callback_data='IT_4'),telebot.types.InlineKeyboardButton(language[lang]['CS'],callback_data='CS_4'))
        markup.add(telebot.types.InlineKeyboardButton(language[lang]['mathCS'],callback_data='mathCS_4'),telebot.types.InlineKeyboardButton(language[lang]['staCS'],callback_data='staCS_4'))
        markup.add(telebot.types.InlineKeyboardButton(language[lang]['mathP'],callback_data='mathP_4'),telebot.types.InlineKeyboardButton(language[lang]['stati'],callback_data='stati_4'))
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        bot.send_message(call.message.chat.id,text=language[lang]['choos_department'],reply_markup=markup)

    elif call.data[:11] == 'fifth_grade':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(language[lang]['it'],callback_data='IT5'),telebot.types.InlineKeyboardButton(language[lang]['CS'],callback_data='CS_5'))
        markup.add(telebot.types.InlineKeyboardButton(language[lang]['mathCS'],callback_data='mathCS_5'),telebot.types.InlineKeyboardButton(language[lang]['staCS'],callback_data='staCS_5'))
        markup.add(telebot.types.InlineKeyboardButton(language[lang]['mathP'],callback_data='mathP_5'),telebot.types.InlineKeyboardButton(language[lang]['stati'],callback_data='stati_5'))
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        bot.send_message(call.message.chat.id,text=language[lang]['choos_department'],reply_markup=markup)
    elif call.data[:3]=='sub':
        setUserInfo(call.from_user.id,call.data.split('_')[1],'true')
        if call.data.split('_')[1]=='PatchNews':
            grade(call.message,lang,called=True)
        else:
            bot.send_message(call.message.chat.id,language[lang]['subscribed'],reply_to_message_id=call.message.id)
    elif call.data[:5]=='unSub':
        setUserInfo(call.from_user.id,call.data.split('_')[1],'false')
        bot.send_message(call.message.chat.id,language[lang]['unSubscribed'],reply_to_message_id=call.message.id)

    elif 'IT' in call.data:
        if call.data.split('_')[1]=='1':
            setLev('1/it',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='2':
            setLev('2/it',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='3':
            setLev('3/it',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='4':
            setLev('4/it',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='5':
            setLev('5/it',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
    elif 'Dep' in call.data:
        if call.data.split('_')[1]=='1':
            setLev('1/dep',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='2':
            setLev('2/dep',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='3':
            setLev('3/dep',call.message.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
    elif 'CS' in call.data:
        if call.data.split('_')[1]=='4':
            setLev('4/dep/cs',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='5':
            setLev('5/dep/cs',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
    elif 'mathCS' in call.data:
        if call.data.split('_')[1]=='4':
            setLev('4/dep/mathcs',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='5':
            setLev('5/dep/mathcs',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
    elif 'staCS' in call.data:
        if call.data.split('_')[1]=='4':
            setLev('4/dep/scs',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='5':
            setLev('5/dep/scs',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
    elif 'mathP' in call.data:
        if call.data.split('_')[1]=='4':
            setLev('4/dep/mathp',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='5':
            setLev('5/dep/mathp',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
    elif 'stati' in call.data:
        if call.data.split('_')[1]=='4':
            setLev('4/dep/s',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='5':
            setLev('5/dep/s',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
    elif call.data=='grade_setting_back':
        markup  = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(language[lang]['subscribe'],callback_data='sub_PatchNews'), telebot.types.InlineKeyboardButton(language[lang]['unSubscribe'],callback_data=f'unSub_PatchNews')) 
        bot.edit_message_text(text=language[lang]['patchNewsInfo'],message_id=call.message.id,chat_id=call.message.chat.id)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.id,reply_markup=markup)
    elif "updateDir_" in call.data:
        bot.register_next_step_handler(bot.send_message(call.message.chat.id,language['admin']['newName']),lambda m:setUpdateDir(m,call.data.split('_')[1],call.data.split('_')[2]))
    
    elif "deleteDir" in call.data:
        if call.data.split("_")[2]=='yes':
            deleteDiractory(call.data.split("_")[1])
            bot.delete_message(call.messege.chat.id,call.messege.id)
            bot.send_message(call.messege.chat.id,language['admin']['dirDeleted'])
        else:
            bot.delete_message(call.messege.chat.id,call.messege.id)
    elif "paste_" in call.data:
        bot.register_next_step_handler(bot.send_message(call.message.chat.id,language['admin']['pasteMessage']),lambda m: insertMessageID(call.data.split("_")[1],m))
    elif 'newDir_'in call.data:
        addDir_and_con(call.message,call.data.split("_")[1])
    elif 'sendColNews' in call.data:
        bot.register_next_step_handler(bot.send_message(call.message.chat.id,"enter the message you want to send🔽"),callback=snedColNews)
    elif 'sendPacthNews' in call.data:
        sendPatchNews(call.message)
    elif 'SEND_' in call.data:
        bot.register_next_step_handler(bot.send_message(call.message.chat.id,"enter the message you want to send🔽"),lambda m: sendPatchMessage(m,call.data.split("_")[1]))
    elif len(call.data.split('/'))>0:
       
        try:
            
            if language['admin']['AddDiractory'] in call.message.reply_markup.keyboard[-1][0].text:
            
                bot.edit_message_text(getDirName(call.data.split('/')[-1],lang),call.message.chat.id,call.message.id)
                bot.edit_message_reply_markup(call.message.chat.id,call.message.id,reply_markup=makeMarup(mdirs=call.data,lang=lang,message=call.message,justDir=True))
            else:
                bot.edit_message_text(getDirName(call.data.split('/')[-1],lang),call.message.chat.id,call.message.id)
                bot.edit_message_reply_markup(call.message.chat.id,call.message.id,reply_markup=makeMarup(mdirs=call.data,lang=lang,message=call.message))
        except copy.Error:
            return
        


# Text handler
@bot.message_handler(content_types=['text'])
def text(message:telebot.types.Message):
   
    userLanguage = getLanguage(message.from_user.id)
    if message.text in ['/courses',language[userLanguage]['courses']]:
        bot.send_message(message.chat.id,language[userLanguage]['select_sem'],disable_web_page_preview=False,reply_markup=makeMarup('c',userLanguage,message))
    
    elif message.text in ['/contact',language[userLanguage]['contact']]:
        bot.register_next_step_handler(bot.send_message(message.chat.id,language[userLanguage]['sendFeedBack']),forwardContact)
    elif message.text in ['/setting',language[userLanguage]['sitting']]:
        changeSetting(userLanguage,message)
    elif message.text in ['/editIndex',language[userLanguage]['addIndex']]:
        bot.register_next_step_handler(bot.send_message(message.chat.id,language[userLanguage]['enterIndex']),saveIndex)
    elif message.text in ['/backMain',language[userLanguage]['back']]:
        bot.send_message(message.chat.id,language[userLanguage]['main'],reply_markup=mainReplyKeyboard(userLanguage))
    elif message.text in ['editColNews',language[userLanguage]['colNews']]:
        markup  = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(language[userLanguage]['subscribe'],callback_data='sub_News'), telebot.types.InlineKeyboardButton(language[userLanguage]['unSubscribe'],callback_data=f'unSub_News')) 
        bot.send_message(message.chat.id,language[userLanguage]['editColNews'],reply_markup=markup)
    elif message.text in ['editPatchNews',language[userLanguage]['patchNews']]:
        markup  = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(language[userLanguage]['subscribe'],callback_data='sub_PatchNews'), telebot.types.InlineKeyboardButton(language[userLanguage]['unSubscribe'],callback_data=f'unSub_PatchNews')) 
        bot.send_message(message.chat.id,language[userLanguage]['patchNewsInfo'],reply_markup=markup)
    elif message.text in ['/help',language[userLanguage]['help']]:
        bot.send_message(message.chat.id,language[userLanguage]['helpMessage'])
    if message.chat.id==config['chatId']:
        if language['admin']['addDir'] in message.text:
            bot.register_next_step_handler(bot.send_message(message.chat.id,language['admin']['dirName']),callback=addDir)
        elif language['admin']['updateDir'] in message.text:
            bot.register_next_step_handler(bot.send_message(message.chat.id,language['admin']['dirName']),callback=updateDir)
        elif language['admin']['delDir'] in message.text:
            bot.register_next_step_handler(bot.send_message(message.chat.id,language['admin']['dirName']),callback=deleteDir)
        elif language['admin']['addMess'] in message.text:
            showDirs(message)
        elif language['admin']['delMess'] in message.text:
            if message.reply_to_message:
                deleteMessage(message.reply_to_message)
            else:
                bot.send_message(message.chat.id,language['admin']['instracionDelMess'])
        elif language['admin']['sendNews'] in message.text:
            markUp = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(language['admin']['patchNews'], callback_data='sendPacthNews'))
            markUp.add(telebot.types.InlineKeyboardButton(language['admin']['colNews'],callback_data='sendColNews'))
            bot.send_message(message.chat.id,"chose one",reply_markup=markUp)
        elif message.reply_to_message and message.text[0:2]=='$c':
            checker=checkDir(message.text.replace('$',''))
            
            if checker== True:
                insertMessageID(message.text[1:].lower().strip(),message.reply_to_message)
                bot.send_message(message.chat.id,language[userLanguage]['saved'],reply_to_message_id=message.id)
            else:
                bot.send_message(message.chat.id,language[userLanguage]['dir_name_missing'].format(checker[0]),reply_markup=dirMarkup(checker),reply_to_message_id=message.id)
        elif message.reply_to_message and message.text[0:2]=='$m':
            li= message.text.split()
            
            for patch in li[1:] :
                
                patchMembers=getSubUser(patch)
                if len(patchMembers)>0:
                    m=bot.send_message(message.chat.id,language[userLanguage]['sending'],reply_to_message_id=message.id)
                    for member in patchMembers:
                        bot.forward_message(member,message.reply_to_message.chat.id,message.reply_to_message.id)
                        
                    bot.edit_message_text(language[userLanguage]['doneSending'],m.chat.id,m.id)
                else :
                    bot.send_message(message.chat.id,language[userLanguage]['noPatch'].format(patch),reply_to_message_id=message.id)

def addDir(message:telebot.types.Message,Path="",addMessage=False):
    dirname=message.text
    chaeck=checkDirCode(dirname)
    if chaeck== True:
        if addMessage:
            insertMessageId(f"{Path}/{dirname}",'0','null','null')
            bot.send_message(message.chat.id,language['admin']['chooseDir'],reply_markup=makeMarup(Path,'ar',message,justDir=True))
        else: bot.send_message(message.chat.id,language['admin']['exisited'])
    else:
        bot.register_next_step_handler( bot.send_message(message.chat.id,language['admin']['enterLang'].format(chaeck[0])),lambda m:dirLang(m,dirname,chaeck,Path=Path,addMessage=addMessage))
        
def dirLang(message:telebot.types.Message,dirName,check,Path="",addMessage=False):
    nameLang=message.text
    if setDir(check[0],dirName,nameLang):
        chaeck2=checkDirCode(dirName)
        if chaeck2==True:
            if addMessage:
                insertMessageId(f"{Path}/{dirName}",'0','null','null')
                bot.send_message(message.chat.id,language['admin']['chooseDir'],reply_markup=makeMarup(Path,'ar',message,justDir=True))
            else:
                bot.send_message(message.chat.id,language['admin']['setDirComplete'])

        else:
            bot.register_next_step_handler( bot.send_message(message.chat.id,language['admin']['enterLang'].format(chaeck2[0])),lambda m:dirLang(m,dirName,chaeck2,Path=Path,addMessage=addMessage))


def updateDir(message:telebot.types.Message):
    markup = telebot.types.InlineKeyboardMarkup()
    
    markup.add(telebot.types.InlineKeyboardButton(language['admin']['updateDirName'], callback_data=f'updateDir_{message.text}_dir')) 
    markup.add(telebot.types.InlineKeyboardButton(language['admin']['updateENDir'], callback_data=f'updateDir_{message.text}_en')) 
    markup.add(telebot.types.InlineKeyboardButton(language['admin']['updateARDir'], callback_data=f'updateDir_{message.text}_ar'))
    bot.send_message(message.chat.id,"what to update?...",reply_markup=markup)


def setUpdateDir(message:telebot.types.Message,dirc,column):
    if (UpdateDir(dirc,message.text,column)):
        bot.send_message(message.chat.id,f"{column} name updated ✅",reply_to_message_id=message.id)
    else :
        bot.send_message(message.chat.id,"somthing went wrong please try agin..",reply_to_message_id=message.id)
def deleteDir(message:telebot.types.Message):
    if checkDirCode(message.text):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('YES', callback_data=f'deleteDir_{message.text}_yes'),telebot.types.InlineKeyboardButton('NO', callback_data=f'deleteDir_{message.text}_no')) 
        bot.send_message(message.chat.id,f"are you shore you want to delete diractory {message.text} ?",reply_markup=markup)
    else:
        bot.send_message(message.chat.id,"no such diractory Found")

def showDirs(message:telebot.types.Message):
    bot.send_message(message.chat.id,language['admin']['chooseDir'],reply_markup=makeMarup('c',lang='ar',message=message,justDir=True))
def addDir_and_con(message :telebot.types.Message,Path):
    bot.register_next_step_handler(bot.send_message(message.chat.id,language['admin']['dirName']),lambda m:addDir(m,Path=Path,addMessage=True))
def deleteMessage(message:telebot.types.Message):
    if(message.content_type=='document'):
        deleteDBMessage(message.chat.id,message.document.file_id)
    elif message.content_type=='text':
        deleteDBMessage(message.chat.id,message.text)
    elif message.content_type=='audio':
        deleteDBMessage(message.chat.id,message.audio.file_id)
    elif message.content_type=='photo':
        deleteDBMessage(message.chat.id,message.photo.__str__)
    elif message.content_type=='video':
        deleteDBMessage(message.chat.id,message.video.file_id)
    elif message.content_type=='video_note':
        deleteDBMessage(message.chat.id,message.video_note.file_id)
    elif message.content_type=='voice':
        deleteDBMessage(message.chat.id,message.voice.file_id)
    elif message.content_type=='location':
        deleteDBMessage(message.chat.id,message.voice.file_id)
    bot.send_message(message.chat.id,language['admin']['messageDleleted'])

       
def snedColNews(message:telebot.types.Message):
    patchMembers=getNewsSubUsers()
    if len(patchMembers)>0:
            m=bot.send_message(message.chat.id,language['admin']['sending'],reply_to_message_id=message.id)
            for member in patchMembers:
                bot.forward_message(member.userChat,message.id,message.id)
                
            bot.edit_message_text(language['admin']['doneSending'],m.chat.id,m.id)
    else :
            bot.send_message(message.chat.id,language['admin']['noSub'],reply_to_message_id=message.id)
      
        
def sendPatchNews(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(f'1 {language["en"]["it"]}',callback_data='SEND_1/it'),telebot.types.InlineKeyboardButton("1 "+language["en"]['department'],callback_data='SEND_1/dep'))
    markup.add(telebot.types.InlineKeyboardButton("2 "+language["en"]['it'],callback_data='SEND_2/it'),telebot.types.InlineKeyboardButton("2 "+language["en"]['department'],callback_data='SEND_2/dep'))
    markup.add(telebot.types.InlineKeyboardButton("3 "+language["en"]['it'],callback_data='SEND_3/it'),telebot.types.InlineKeyboardButton("3 "+language['en']['department'],callback_data='SEND_3/dep'))
    markup.add(telebot.types.InlineKeyboardButton("4 "+language["en"]['it'],callback_data='SEND_4/it'),telebot.types.InlineKeyboardButton("4 "+language["en"]['CS'],callback_data='SEND_4/dep/cs'))
    markup.add(telebot.types.InlineKeyboardButton("4 "+language["en"]['mathCS'],callback_data='SEND_4/dep/mathcs'),telebot.types.InlineKeyboardButton("4 "+language["en"]['staCS'],callback_data='SEND_4/dep/scs'))
    markup.add(telebot.types.InlineKeyboardButton("4 "+language["en"]['mathP'],callback_data='SEND_4/dep/mathp'),telebot.types.InlineKeyboardButton("4 "+language["en"]['stati'],callback_data='SEND_4/dep/s'))
    markup.add(telebot.types.InlineKeyboardButton("5 "+language["en"]['it'],callback_data='SEND_5/it'),telebot.types.InlineKeyboardButton("5 "+language["en"]['CS'],callback_data='SEND_5/dep/cs'))
    markup.add(telebot.types.InlineKeyboardButton("5 "+language["en"]['mathCS'],callback_data='SEND_5/dep/mathcs'),telebot.types.InlineKeyboardButton("5"+language["en"]['staCS'],callback_data='SEND_5/dep/scs'))
    markup.add(telebot.types.InlineKeyboardButton("5 "+language["en"]['mathP'],callback_data='SEND_5/dep/mathp'),telebot.types.InlineKeyboardButton("5 "+language["en"]['stati'],callback_data='SEND_5/dep/s'))
    bot.send_message(message.chat.id,"Select a patch",reply_markup=makeMarup)               
def sendPatchMessage(message,patch):
    patchMembers=getSubUser(patch)
    if len(patchMembers)>0:
        m=bot.send_message(message.chat.id,language['admin']['sending'],reply_to_message_id=message.id)
        for member in patchMembers:
            bot.forward_message(member,message.id,message.id)
            
        bot.edit_message_text(language['admin']['doneSending'],m.chat.id,m.id)
    else :
        bot.send_message(message.chat.id,language["admin"]['noSub'],reply_to_message_id=message.id)

bot.polling(none_stop=True)
    
 



