# Get instance
import instaloader
from instaloader.exceptions import TwoFactorAuthRequiredException

L = instaloader.Instaloader()

# Login or load session

userName = "username"
password = "password"

fileName1 = "notFollowingBack.txt"
fileName2 = "updated_notFollowing_Back.txt"

#try:

L.login(userName, password)

#except TwoFactorAuthRequiredException:
 #   L.two_factor_login(11111)

# Obtain profile metadata
profile = instaloader.Profile.from_username(L.context, userName)

# Print list of followees
followers_list = [] #current followers list

following_list = [] #current following list

notFollowing_me = [] #complement of current following and followers list

lastChecked_list = [] #list from txt file from last session

updatedNotFollowingBack = [] #complement of notfollowing_me and lastChecked_list


def getNotFollowingBack():
    for followers in profile.get_followers(): # get list of people that currently follow me
        followers_list.append(followers.username)
   
    for following in profile.get_followees(): # get list of people that I follow
        following_list.append(following.username)
   

    for count in following_list:        #insert names of people that Currently dont follow you back in to notFollowing_me
        if count not in followers_list:
            notFollowing_me.append(count)
        
getNotFollowingBack() #get list of people currrently not following back 

while True:
    try:
        with open(fileName1, 'r') as f: #get names from last session if file exists
            lastChecked_list = f.read().splitlines()
            break
    except:
        print("You are running this script for the first time therefore file DNE...Creating file\n")        #if files dont exist create them and tell user how they will be updated
        print("Created file " + fileName1 + " (updated with people not following you back right now).\n")
        print("Created file " + fileName2 + ", if you run this script again this file will be updated with new users not following you back\n")
        with open(fileName1, 'w') as fp:
            for items in notFollowing_me:
                fp.write("%s\n" % items)

  
with open(fileName2, 'w') as fp:
    for items in notFollowing_me:
        if items not in lastChecked_list: #write complement of notFollowing_me and lastChecked_list to updated_notFollowing_Back.txt
            updatedNotFollowingBack.append(items)
            fp.write("%s\n" % items)

with open(fileName1, 'a') as f:
    for items in updatedNotFollowingBack:
        f.write("%s\n" % items)



print('Done')





        