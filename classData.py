import shelve
import os
import random

import classPost

DIR = "data/"

s = "QWERTYUIOPASDFGHJKLMNBVCXZ1234567890"
def GenerateID():
    return "".join(random.choices(s, k=16))


class DataBase:
    def __init__(self):

        if not os.path.exists(DIR):
            os.mkdir(DIR)


    def __loadUsersData(self):

        self.users = shelve.open(DIR + "USERS")
        print(f"Reged users: {len(self.users.keys())}")

        self.admins = shelve.open(DIR + "ADMINS")

        self.posts = shelve.open(DIR + "POSTS")
        self.proposed = shelve.open(DIR + "PROPOSED")


    def load(self):
        self.__loadUsersData()

    def close(self):
        self.users.close()
        self.admins.close()
        self.posts.close()
        self.proposed.close()

    def __del__(self):
        self.close()

    def addProposed(self, mess):

        mess.media_group_id = str(mess.media_group_id)

        cont = mess.__dict__[mess.content_type]

        if mess.content_type != "text":
            if type(cont) == list:
                cont = cont[-1].file_id
            else:
                cont = cont.file_id

        if mess.content_type != "text":
            if mess.media_group_id in self.proposed.keys():

                post = self.proposed[mess.media_group_id]
                post.media += [{"type": mess.content_type, "id": cont}]
                self.proposed[mess.media_group_id] = post

                return mess.media_group_id


        id = mess.media_group_id
        if id == 'None':
            id = GenerateID()


        text = mess.text
        if text == None:
            text = mess.caption

            if text == None:
                text = ""

        if mess.content_type != "text":
            media = [{"type": mess.content_type, "id": cont}]
        else:
            media = []

        self.proposed[id] = classPost.Post(mess.from_user.username, mess.chat.id, text, media)
        return id

    def EditProposed(self, post_id: str, key: str, value: str):
        try:
            post = self.proposed[post_id]
            post.__dict__[key] = value
            self.proposed[post_id] = post

            return True
        except Exception as e:
            print("такого поста или ключа нет", str(e))
            return False

    def MoveProposedInPost(self, post_id: str):
        try:
            self.posts[post_id] = self.proposed[post_id]
            del self.proposed[post_id]
            return True

        except Exception as e:
            print("такого поста нет", str(e))
            return False

    def GetOneProposed(self):
        """
        Get One ProposedID which post don`t delited and first in queue

        :return:
        """
        posts = self.proposed.items()
        if len(posts) == 0:
            return None

        post = min(posts, key=lambda x: x[1].priority)

        if post[1].priority < 10000:
            return post[0]
        else:
            return None
