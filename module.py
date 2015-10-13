import sqlite3
import md5;
import re;
def sanitize(input):
    return re.sub('"', "  ", input)

def encrypt(username,password):
    m = md5.new()
    m.update(username+password)
    return m.hexdigest()
    #hashes and salts the pasword for permanent storage or retrieval
    #returns hashed password

def authenticate(username, password):
    username = sanitize(username)
    conn = sqlite3.connect("myDataBase.db")
    c = conn.cursor()
    ans = c.execute('select * from logins where username = "'+username+'" and password = "'+encrypt(username,password)+'";') 
    for r in ans:
        return True;
    return False;
    #returns a boolean that describes whether the user has succesfully logged in.

def newUser(username,password):
    username = sanitize(username)
    conn = sqlite3.connect("myDataBase.db")
    c = conn.cursor()
    ans = c.execute('select * from logins where username = "%s";' % username)
    for r in ans:
        return False
    ans = c.execute('insert into logins values("'+username+'","'+encrypt(username,password)+'");')
    conn.commit()
    return True

def makePost(username, title, contents):
    username = sanitize(username)
    title = sanitize(title)
    contents = sanitize(contents)
    conn = sqlite3.connect("myDataBase.db")
    c = conn.cursor()
    ans = c.execute('select * from posts where title = "%s";' % title)
    for r in ans:
        return False;
    ans = c.execute('insert into posts values("'+username+'","'+title+'","'+contents+'");')
    conn.commit()
    return True;
    #adds a post to the databes from username with title = title and contents = contents
    #returns a boolean representing if the operation was successful
    #operation will be unsuccessful if a post with the same title already exists

def getPost(title):
    title = sanitize(title)
    conn = sqlite3.connect("myDataBase.db")
    c = conn.cursor()
    ans = c.execute('select * from posts where title ="%s";' % title) 
    for r in ans:
        return r[2]
    #returns the content of post with title = title
    #may only be useful for debugging

def getAllPosts():
    conn = sqlite3.connect("myDataBase.db")
    c = conn.cursor()
    c.execute('select * from posts;')
    return c.fetchall();
    #returns a 2d array where the first index represents row id. The second index works as follows:
    #the 0 index store sthe name of the original poster
    #the 1 index represents the title of the post
    #the 2 index stores the contents of the post.


def addToPost(title, content):
    title = sanitize(title)
    content = sanitize(content)
    conn = sqlite3.connect("myDataBase.db")
    c = conn.cursor()
    newContent = " "+getPost(title)+content
    c.execute('update posts set contents = "%s" where title="%s";'% (newContent,title))
    conn.commit()
    return True;
    #adds content to content of original post and returns a boolean representing wether or not the operation was successful

def removePost(username,title):
    title = sanitize(title)
    if(username == "Admin"):
        conn = sqlite3.connect("myDataBase.db")
        c = conn.cursor()
        
        c.execute('delete from posts where title="%s";' % title)
        conn.commit()
        return True;
    return False
    #removes post with tile=title from database if it exists and username = admin
    #returns false if operation failed

