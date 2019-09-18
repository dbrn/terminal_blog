from database import Database
from datetime import datetime


class Blog(object):
    def __init__(self, blog_author, blog_title, blog_description):
        self.author = blog_author
        self.title = blog_title
        self.description = blog_description
        self.collection_name = "blog"
        self.id = None
        self._db = Database("127.0.0.1", 27017, "fullstack").database

    def save_blog(self):
        i = 0
        while True:
            data = self._db[self.collection_name].find({"id": i})
            if data.count() == 0:
                self.id = i
                break
            else:
                i += 1
        self._db[self.collection_name].insert(self.json())

    def json(self):
        return {
            "id": self.id,
            "author": self.author,
            "title": self.title,
            "description": self.description
        }

    @staticmethod
    def retrieve_blog(author):
        db = Database("127.0.0.1", 27017, "fullstack").database
        blog = db["blog"].find({"author": author})
        return [item for item in blog]

    @staticmethod
    def list_all_blogs():
        db = Database("127.0.0.1", 27017, "fullstack").database
        blogs = [blog for blog in db["blog"].find({})]
        del db
        return blogs

    @staticmethod
    def check_user(name):
        db = Database("127.0.0.1", 27017, "fullstack").database
        results = db["blog"].find({"author": str(name)})
        del db
        if results.count() > 0:
            return True
        return False


class Post(object):
    def __init__(self, blog, post_title, content, creation=None):
        self._db = None
        self.blog_id = blog["id"]
        self.id = self.set_post_id()
        self.author = blog["author"]
        self.title = post_title
        self.contents = content
        if creation is None:
            self.creation = datetime.utcnow()
        else:
            self.creation = creation

    def set_post_id(self):
        self._db = Database("127.0.0.1", 27017, "fullstack").database
        i = 0
        while True:
            data = self._db["posts"].find({"blog_id": self.blog_id, "id": i})
            if data.count() == 0:
                return i
            i += 1

    def save(self):
        self._db["posts"].insert({
            "blog_id": self.blog_id,
            "id": self.id,
            "author": self.author,
            "title": self.title,
            "date": self.creation,
            "contents": self.contents
        })

    @staticmethod
    def get_posts(blog_id):
        _db = Database("127.0.0.1", 27017, "fullstack").database
        posts = [post for post in _db["posts"].find({"blog_id": blog_id})]
        return posts
