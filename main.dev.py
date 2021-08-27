from db.session import Session
from db.models import CodeName, User, Message

# create test users
for i in range(1, 10):
    session = Session()

    code_name = User(
        Lev=str(i),
        SIndex=f'020-60{i}',
        name=f'Ali {i}',
        userChat=f'0000000{i}'
    )

    session.add(code_name)
    session.commit()

# create test messages
for i in range(1, 5):
    session = Session()

    code_name = Message(
        dir=f'path/path/{i}',
        messageId=f'000000{i}',
        chatId=f'999999{i}',
        content_type='video',
    )

    session.add(code_name)
    session.commit()

# create test codeNames
for i in range(1, 5):
    session = Session()

    code_name = CodeName(
        dir=f'path/path/{i}',
        ar=f'هنا/هنا/هنا',
        en=f'here/here/here',
    )

    session.add(code_name)
    session.commit()


# test db.queries module
from db.queries import getMessgesIDs


dirs = 'path/path/1'
messages = getMessgesIDs(dirs)
print('\n\n\n\n', messages, '\n\n\n\n')