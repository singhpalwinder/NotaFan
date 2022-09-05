# Get instance
import instaloader
from instaloader.exceptions import TwoFactorAuthRequiredException

L = instaloader.Instaloader()

# Login or load session
userName = "yourusername"
password = "yourpassword"

fileName = "Not_following_Back.txt"

try:
    L.login(userName, password)
except TwoFactorAuthRequiredException:
    L.two_factor_login(11111)

# Obtain profile metadata
profile = instaloader.Profile.from_username(L.context, userName)

# Print list of followees
followers_list = []

following_list = []

notFollowing_me = []


for followers in profile.get_followers(): # get list of people that follow me
    followers_list.append(followers.username)
   
# (likewise with profile.get_followers())
for following in profile.get_followees(): # get list of people that I follow
    following_list.append(following.username)
   


for count in following_list:
    if count not in followers_list:
        notFollowing_me.append(count)
        


with open(fileName, 'w') as fp:
    for items in notFollowing_me:
        fp.write("%s\n" % items)

    print('Done')





        