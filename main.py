from AccessToken import APP_ACCESS_TOKEN, BASE_URL
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import matplotlib.pyplot as plt
import requests
import urllib


# method for getting self information using requests
def self_info():
    request_url = (BASE_URL + '/users/self/?access_token=%s') % APP_ACCESS_TOKEN
    print 'Requesting info for: '+request_url
    # the reply from the api is in json format
    my_info = requests.get(request_url).json()
    if my_info['meta']['code'] == 200:
        if len(my_info['data']):
            print 'Username : %s'% (my_info['data']['username'])
            print 'No. of followers : %s'% (my_info['data']['counts']['followed_by'])
            print '# people you are following: %s'% (my_info['data']['counts']['follows'])
            print 'No. of posts: %s'% (my_info['data']['counts']['media'])
        else:
            print 'No such user exists'
    else:
        print 'Error occurred'


# method to get userid by a username
def get_user_id(insta_username):
    request_url = (BASE_URL + '/users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url for user id : %s' % request_url
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


# method for user information from id retrieved by get_user_id()
def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + '/users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


# method for self recent posts
def get_own_post():
    request_url = (BASE_URL + '/users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url for own post : %s' % request_url
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            choose_post(own_media)
            print 'Your post has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


# method for downloading user's recent media posts
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + '/users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url for user post : %s' % request_url
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            choose_post(user_media)
            print 'Your post has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


# method to select post according to user's choice
def choose_post(user_media):
    print '1. Select Recent Image\n2. Select Least liked post\n3. Select Recent video '
    select = int(raw_input("enter the choice of post : "))
    if select == 1:
        i = -1
        for media in user_media['data']:
            i = i+1
            if media['type'] == 'image':
                image_name = user_media['data'][i]['id'] + '.jpeg'
                image_url = user_media['data'][i]['images']['standard_resolution']['url']
                urllib.urlretrieve(image_url, image_name)
                break
    elif select == 2:
        lowest = user_media['data'][0]['likes']['count']
        i=-1
        for media in user_media['data']:
            i = i+1
            if media['likes']['count'] < lowest:
                lowest = media['likes']['count']
                index = i
        if user_media['data'][index]['type'] == 'image':
            image_name = "least_liked.jpg"
            image_url = user_media['data'][index]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
        elif user_media['data'][index]['type'] == 'video':
            video_name = "least_liked_video.mp4"
            video_url = user_media['data'][index]['videos']['standard_resolution']['url']
            urllib.urlretrieve(video_url, video_name)
    elif select == 3:
        i=-1
        vid_index = -1
        for media in user_media['data']:
            i = i+1
            if media['type'] == 'video':
                vid_index = i
        if vid_index == -1:
            print "no videos found"
            exit()
        video_name = user_media['data'][vid_index]['id']+'.mp4'
        video_url = user_media['data'][vid_index]['videos']['standard_resolution']['url']
        urllib.urlretrieve(video_url, video_name)


# method to get id of a recent post by user
def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + '/users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url for recent post : %s' % request_url
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()


# method to like the post of user by getting it's post id
def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + '/media/%s/likes') % media_id
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url to like : %s' % request_url
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


# method to get list of people liking the recent media for a user
def get_like_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + '/media/%s/likes?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET Liked media url : %s' % request_url
    liked_list = requests.get(request_url).json()
    if(liked_list['meta']['code']) == 200:
        if len(liked_list['data']):
            print 'people who liked it :'
            for people in liked_list['data']:
                print people['username']
            print 'Number of likes : %d' % len(liked_list['data'])
        else:
            print "no likes on the post"
    else:
        print 'some error occurred'


# method to put a comment on the post of a user with help of post id
def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + '/media/%s/comments') % media_id
    print 'POST url for commenting post: %s' % request_url

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


def get_comment_list(insta_username):
    media_id = get_post_id(insta_username)
    request_url = BASE_URL + '/media/%s/comments?access_token=%s' % (media_id, APP_ACCESS_TOKEN)
    print "GET url for Comments list : %s" % request_url
    print '\n'
    comment_list = requests.get(request_url).json()
    if(comment_list['meta']['code']) == 200:
        if len(comment_list['data']):
            for comments in comment_list['data']:
                print comments["from"]["username"]+'  says : '+comments["text"]
                # print comments["text"]


# method to get recent media liked by self
def get_recent_liked():
    request_url = BASE_URL+'/users/self/media/liked?access_token=%s' % APP_ACCESS_TOKEN
    print "Get url for recent likes : %s" % request_url
    liked_list = requests.get(request_url).json()
    if liked_list['meta']['code'] == 200:
        for media in liked_list['data']:
            print "liked for user    %s:" % media['user']['username']
            #print media['user']['username']
            print "type : %s" % media['type']
            if media['tags'] and media['caption']:
                print "tags : %s  , caption : %s" % (media['tags'][0], media['caption']['text'])
            print "\n"


# method to delete negative comments
def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + '/media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):

            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if blob.sentiment.p_neg > blob.sentiment.p_pos:
                    print 'Negative comment : %s' % comment_text
                    delete_url = (BASE_URL + '/media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % delete_url
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % comment_text
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


# method to analyze comments
def analyze_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + '/media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    comment_info = requests.get(request_url).json()
    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):

            for x in range(0, len(comment_info['data'])):
                # comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                print "analyzing ...."
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                negative = []
                positive = []
                if blob.sentiment.p_neg > blob.sentiment.p_pos:
                    negative.append(blob.sentiment.p_neg)
                else:
                    positive.append(blob.sentiment.p_pos)
    slices = [len(negative), len(positive)]
    print "negative : %d" % len(negative)
    print "positive :%d" % len(positive)
    cols = ['y', 'r']
    activities = ['negative', 'positive']
    plt.pie(slices, startangle=90, shadow=True, explode=(0.1, 0), autopct='%1.1f%%', colors=cols, labels=activities)
    plt.show()




# execution starts from here
def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"
        print "e.Get a list of people who have liked the recent post of a user\n"
        print "f.Like the recent post of a user\n"
        print "g.Get a list of comments on the recent post of a user\n"
        print "h.Make a comment on the recent post of a user\n"
        print "i.Delete negative comments from the recent post of a user\n"
        print "j.Get Recent Media liked by self"
        print "k.Exit"

        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input("Enter the username of the user: ")
            get_user_post(insta_username)
        elif choice == "e":
            insta_username = raw_input("Enter the username of the user: ")
            get_like_list(insta_username)
        elif choice == "f":
            insta_username = raw_input("Enter the username of the user: ")
            like_a_post(insta_username)
        elif choice == "g":
            insta_username = raw_input("Enter the username of the user: ")
            get_comment_list(insta_username)
        elif choice == "h":
            insta_username = raw_input("Enter the username of the user: ")
            post_a_comment(insta_username)
        elif choice == "i":
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comment(insta_username)
        elif choice == "j":
            get_recent_liked()
        elif choice == "k":
            exit()
        else:
            print "wrong choice"


# execution begins here
delete_negative_comment('forinstaprojects')