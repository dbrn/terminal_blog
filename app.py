# python 3.6+
from blog import Blog, Post
from datetime import datetime


def write_post(blog):
    print(f"Writing post in blog: {blog['title']}\n")
    title = input("Insert post title: ")
    contents = input("Insert contents: ")
    date = input("Insert date (YYYYMMDD) or leave blank: ")
    if date != "":
        date = datetime.strptime(date, "%Y%m%d")
        post = Post(blog, title, contents, date)
    else:
        post = Post(blog, title, contents)
    post.save()
    print(f"Post {title} has been succesfully saved")


def read_posts():
    end = False
    print()
    blogs = list_blogs()
    print()
    while end is False:
        answer = input(
            "Insert the ID of the blog to read or input (Q) to quit: ")
        if answer.lower() == "q":
            print("Goodbye!")
            end = True
        else:
            for item in blogs:
                if answer == str(item["id"]):
                    print(f"Opening blog: {item['title']}...\n")
                    posts = Post.get_posts(item["id"])
                    if len(posts) == 0:
                        print(f"No posts found in blog {item['title']}")
                    for p in posts:
                        print(f"POST ID:\t{p['id']}\n"
                              f"AUTHOR:\t{p['author']}\n"
                              f"TITLE:\t{p['title']}\n"
                              f"PUBLISHED:\t{p['date']}\n"
                              f"\n"
                              f"{p['contents']}\n\n")
                    end = True
                    break
            else:
                print(f"Blog ID {answer} not found! Try again.")
    print("Goodbye!")


def blog_menu(blog=None):
    if blog is None:
        read_posts()
    else:
        while True:
            answer = input("Read (R) or (W) write posts? ")
            if answer.lower() == "r":
                read_posts()
                break
            elif answer.lower() == "w":
                write_post(blog)
                break
            else:
                print("Wrong command! Try again.")


def list_blogs():
    blogs = Blog.list_all_blogs()
    for blog in blogs:
        print(f"{blog['id']} - {blog['title']} by {blog['author']}")
    return blogs


def main():
    blog = None
    username = input("Insert your username: ")
    if Blog.check_user(username):
        print(f"Welcome back {username}")
        blog = Blog.retrieve_blog(username)
        blog_menu(blog[0])
    else:
        print(f"Username {username} not found.")
        while True:
            answer = input("Do you want to create a new blog? (Y/N)")
            if answer.lower() == "y":
                blog = Blog(blog_author=str(username),
                            blog_title=input("Insert at title for your blog: "),
                            blog_description=input("Insert a description: "))
                blog.save_blog()
                print(f"Blog {blog.title}, saved with ID {blog.id}")
                blog_menu(blog)
                break
            elif answer.lower() == "n":
                blog_menu()
                break
            else:
                print("Wrong answer, retry!")


if __name__ == "__main__":
    main()
