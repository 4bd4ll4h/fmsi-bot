from io import StringIO
from json.decoder import JSONDecoder
from os import path
import json
import re
import ssl
import telebot
from telebot.types import Message
from model import dbQuery
from aiohttp import web
import copy

# Finding the absolute path of the config file
scriptPath = path.abspath(__file__)
dirPath = path.dirname(scriptPath)
configPath = path.join(dirPath,'config.json')

config = json.load(open(configPath,encoding='utf8'))
dbSql = dbQuery(config['database'])
language = json.load(open(config['language'],encoding='utf8'))

bot = telebot.TeleBot(config['botToken'], parse_mode='HTML')

# Configuration for webhook
webhookBaseUrl = f"https://{config['webhookOptions']['webhookHost']}"
webhookUrlPath = f"/{config['botToken']}/"

app =web.Application()

# Process webhook calls
async def handle(request ):
    print("helllllooooo")
    if request.match_info.get('token') == bot.token:
        request_body_dict = await request.json()
        update = telebot.types.Update.de_json(request_body_dict)
        
        bot.process_new_updates([update])
        return web.Response()
    else:
        return web.Response(status=403)
async def test(requsest):
    return web.Response(text="<h1>it's working!!</h1>")
app.router.add_post("/{token}/", handler= handle)
app.router.add_get("/",handler=test)
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

def coursesList(userLanguage):
    markup = telebot.types.InlineKeyboardMarkup()
    
    markup.add(telebot.types.InlineKeyboardButton(language[userLanguage]['sem1'], callback_data=f'first_sem_{userLanguage}'), telebot.types.InlineKeyboardButton(language[userLanguage]['sem2'], callback_data=f'second_sem_{userLanguage}')) 
    markup.add(telebot.types.InlineKeyboardButton(language[userLanguage]['sem3'], callback_data=f'third_sem_{userLanguage}'), telebot.types.InlineKeyboardButton(language[userLanguage]['sem4'], callback_data=f'fourth_sem_{userLanguage}')) 
    markup.add(telebot.types.InlineKeyboardButton(language[userLanguage]['sem5'], callback_data=f'fifth_sem_{userLanguage}'), telebot.types.InlineKeyboardButton(language[userLanguage]['sem6'], callback_data=f'sixth_sem_{userLanguage}'))
    markup.add(telebot.types.InlineKeyboardButton(language[userLanguage]['sem7'], callback_data=f'seventh_sem_{userLanguage}'), telebot.types.InlineKeyboardButton(language[userLanguage]['sem8'], callback_data=f'eigth_sem_{userLanguage}'))
    markup.add(telebot.types.InlineKeyboardButton(language[userLanguage]['sem9'], callback_data=f'nineth_sem_{userLanguage}'), telebot.types.InlineKeyboardButton(language[userLanguage]['sem10'], callback_data=f'tenth_sem_{userLanguage}'))
    
    return markup

def makeMarup(mdirs,lang,message):
    
    ids=dbSql.getMessgesIDs(mdirs)
    print(ids)
    if ids:
        for id in ids:
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
            
            

    dirs= dbSql.getMessagesDir(mdirs)
    
    markup = telebot.types.InlineKeyboardMarkup()
    if dirs :
        for dr  in dirs:
            print(dr,mdirs,dr.find(mdirs))
            if dr.find(mdirs)>-1:
                text= dr.replace(mdirs+'/','').split('/')[0]
                markup.add(telebot.types.InlineKeyboardButton(dbSql.getDirName(text,lang), callback_data=mdirs+'/'+text))
        return markup
                
    
def checkDir(dirs:str):
    dirList=dirs.split('/') if len(dirs.split('/'))>0 else [dirs]
    for d in dirList:
        if dbSql.checkDirCode(d)!= True:
            return [d,dbSql.checkDirCode(d)]
    return True

def dirMarkup(codeNames):
    markup = telebot.types.InlineKeyboardMarkup()
    if  codeNames[1][0]:
        markup.add(telebot.types.InlineKeyboardButton('العربية', switch_inline_query_current_chat=f'$i/ar/{codeNames[0]}/()'))  
    if codeNames[1][1]:
        markup.add(telebot.types.InlineKeyboardButton('English', switch_inline_query_current_chat=f'$i/en/{codeNames[0]}/()'))
    return markup
def insertMessageID(dr:str,message:Message):
    
    if(message.content_type=='document'):
        dbSql.insertMessageId(dr,message.chat.id,message.document.file_id,message.content_type)
    elif message.content_type=='text':
        dbSql.insertMessageId(dr,message.chat.id,message.text,message.content_type)
    elif message.content_type=='audio':
        dbSql.insertMessageId(dr,message.chat.id,message.audio.file_id,message.content_type)
    elif message.content_type=='photo':
        dbSql.insertMessageId(dr,message.chat.id,message.photo.__str__,message.content_type)
    elif message.content_type=='video':
        dbSql.insertMessageId(dr,message.chat.id,message.video.file_id,message.content_type)
    elif message.content_type=='video_note':
        dbSql.insertMessageId(dr,message.chat.id,message.video_note.file_id,message.content_type)
    elif message.content_type=='voice':
        dbSql.insertMessageId(dr,message.chat.id,message.voice.file_id,message.content_type)
    elif message.content_type=='location':
        dbSql.insertMessageId(dr,message.chat.id,message.voice.file_id,message.content_type)


def forwardContact(message):
    bot.forward_message('-1001451209844',message.chat.id,message.id)
    bot.reply_to(message,language['ar']['grade_selected'])

def changeSetting(userLanguage:str,message):
    markup  = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    markup.add(telebot.types.InlineKeyboardButton(language[userLanguage]['addIndex']), telebot.types.InlineKeyboardButton(language[userLanguage]['patchNews'])) 
    markup.add(telebot.types.InlineKeyboardButton(language[userLanguage]['back']),telebot.types.InlineKeyboardButton(language[userLanguage]['colNews'])) 
   
    bot.send_message(message.chat.id,text=language[userLanguage]['chooseSetting'],reply_markup=markup)
def saveIndex(message):
    dbSql.setIndex(message.from_user.id,message.text)
    bot.send_message(message.chat.id,language['ar']['grade_selected'])


@bot.message_handler(commands=['start'])
def start(message):
    if  not dbSql.setAccount(message.from_user.id,message.chat.id):
        lang=dbSql.getLanguage(message.from_user.id)
        bot.send_message(message.chat.id,text=language[lang]['greet'].format(message.from_user.first_name),reply_markup=mainReplyKeyboard(lang),disable_web_page_preview=True)
        grade(message,lang)
    elif(not dbSql.checkInfo(message.from_user.id,"Lev")):
        lang=dbSql.getLanguage(message.from_user.id)
        bot.send_message(message.chat.id,text=language[lang]['greetComBack'].format(message.from_user.first_name),reply_markup=mainReplyKeyboard(lang),disable_web_page_preview=True)
        grade(message,lang,True)

@bot.message_handler(commands=['help'])
def help(message):
    if message.chat.id== config['chatId']:
        bot.send_message(message.chat.id,language[dbSql.getLanguage(message.from_user.id)]['adminHelp'])
    else:
        bot.send_message(message.chat.id,language[dbSql.getLanguage(message.from_user.id)]['helpMessage'])
# Callback handler
@bot.callback_query_handler(func=lambda call: True)
def callbackHandler(call):
    lang=dbSql.getLanguage(call.message.from_user.id)
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
        dbSql.setUserInfo(call.from_user.id,call.data.split('_')[1],'true')
        if call.data.split('_')[1]=='PatchNews':
            grade(call.message,lang,called=True)
        else:
            bot.send_message(call.message.chat.id,language[lang]['subscribed'],reply_to_message_id=call.message.id)
    elif call.data[:5]=='unSub':
        dbSql.setUserInfo(call.from_user.id,call.data.split('_')[1],'false')
        bot.send_message(call.message.chat.id,language[lang]['unSubscribed'],reply_to_message_id=call.message.id)

    elif 'IT' in call.data:
        if call.data.split('_')[1]=='1':
            dbSql.setLev('1/it',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='2':
            dbSql.setLev('2/it',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='3':
            print(call.from_user.id)
            dbSql.setLev('3/it',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='4':
            dbSql.setLev('4/it',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='5':
            dbSql.setLev('5/it',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
    elif 'Dep' in call.data:
        if call.data.split('_')[1]=='1':
            dbSql.setLev('1/dep',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='2':
            dbSql.setLev('2/dep',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='3':
            dbSql.setLev('3/dep',call.message.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
    elif 'CS' in call.data:
        if call.data.split('_')[1]=='4':
            dbSql.setLev('4/dep/cs',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='5':
            dbSql.setLev('5/dep/cs',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
    elif 'mathCS' in call.data:
        if call.data.split('_')[1]=='4':
            dbSql.setLev('4/dep/mathcs',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='5':
            dbSql.setLev('5/dep/mathcs',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
    elif 'staCS' in call.data:
        if call.data.split('_')[1]=='4':
            dbSql.setLev('4/dep/scs',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='5':
            dbSql.setLev('5/dep/scs',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
    elif 'mathP' in call.data:
        if call.data.split('_')[1]=='4':
            dbSql.setLev('4/dep/mathp',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='5':
            dbSql.setLev('5/dep/mathp',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
    elif 'stati' in call.data:
        if call.data.split('_')[1]=='4':
            dbSql.setLev('4/dep/s',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
        if call.data.split('_')[1]=='5':
            dbSql.setLev('5/dep/s',call.from_user.id)
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(call.message.chat.id,language[lang]['grade_selected'])
    elif call.data=='grade_setting_back':
        markup  = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(language[lang]['subscribe'],callback_data='sub_PatchNews'), telebot.types.InlineKeyboardButton(language[lang]['unSubscribe'],callback_data=f'unSub_PatchNews')) 
        bot.edit_message_text(text=language[lang]['patchNewsInfo'],message_id=call.message.id,chat_id=call.message.chat.id)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.id,reply_markup=markup)
    elif len(call.data.split('/'))>0:
        try:
            bot.edit_message_text(dbSql.getDirName(call.data.split('/')[0],lang),call.message.chat.id,call.message.id)
            bot.edit_message_reply_markup(call.message.chat.id,call.message.id,reply_markup=makeMarup(call.data,lang,call.message))
        except:return
        


# Text handler
@bot.message_handler(content_types=['text'])
def text(message:telebot.types.Message):
    print(message.chat.id)
    userLanguage = dbSql.getLanguage(message.from_user.id)
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
        print(message.text)
        markup  = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(language[userLanguage]['subscribe'],callback_data='sub_PatchNews'), telebot.types.InlineKeyboardButton(language[userLanguage]['unSubscribe'],callback_data=f'unSub_PatchNews')) 
        bot.send_message(message.chat.id,language[userLanguage]['patchNewsInfo'],reply_markup=markup)
    elif message.text in ['/help',language[userLanguage]['help']]:
        bot.send_message(message.chat.id,language[userLanguage]['helpMessage'])
    if message.chat.id==config['chatId']:
        if '$i/' in message.text:
            arg=message.text.split('/')
            if dbSql.setDir(arg[1],arg[2],arg[3][1:len(arg[3])-1]):
                bot.send_message(message.chat.id,language[userLanguage]['grade_selected'],reply_to_message_id=message.id)
            else:
                bot.send_message(message.chat.id,language[userLanguage]['fail_insert_dir'],reply_to_message_id=message.id)

        elif message.reply_to_message and message.text[0:2]=='$c':
            checker=checkDir(message.text.replace('$',''))
            print(checker)
            if checker== True:
                insertMessageID(message.text[1:].lower().strip(),message.reply_to_message)
                bot.send_message(message.chat.id,language[userLanguage]['saved'],reply_to_message_id=message.id)
            else:
                bot.send_message(message.chat.id,language[userLanguage]['dir_name_missing'].format(checker[0]),reply_markup=dirMarkup(checker),reply_to_message_id=message.id)
        elif message.reply_to_message and message.text[0:2]=='$m':
            li= message.text.split()
            print(li)
            for patch in li[1:] :
                print(patch)
                patchMembers=dbSql.getSubUser(patch)
                if len(patchMembers)>0:
                    m=bot.send_message(message.chat.id,language[userLanguage]['sending'],reply_to_message_id=message.id)
                    for member in patchMembers:
                        bot.forward_message(member,message.reply_to_message.chat.id,message.reply_to_message.id)
                        
                    bot.edit_message_text(language[userLanguage]['doneSending'],m.chat.id,m.id)
                else :
                    bot.send_message(message.chat.id,language[userLanguage]['noPatch'].format(patch),reply_to_message_id=message.id)

bot.delete_webhook(drop_pending_updates=False)       
bot.set_webhook(url=webhookBaseUrl + webhookUrlPath)

    
    # Start aiohttp server
if __name__ == '__main__':
    print("app started")
    web.run_app(
        app
    )



