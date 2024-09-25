# Get instance
import instaloader
from instaloader.exceptions import TwoFactorAuthRequiredException
import credentials


def readData(fileName):
    try:
        with open(fileName, 'r') as f: #get names from last session if file exists
            lastChecked_list = f.read().splitlines()
            return lastChecked_list
    except:
        print("You are running this script for the first time therefore file DNE...Creating file\n")        #if files dont exist create them and tell user how they will be updated
        print("Created file " + fileName + " (updated with people not following you back right now).\n")
        with open(fileName, 'w') as fp:
                fp.write("")
def writeData(fileName, notFollowingBack):

    # add new names to first file 
    with open(fileName, 'a') as f:
        for items in notFollowingBack:
            f.write("%s\n" % items)
def getNotFollowingBack(user, password, auth, lastChecked):
    L = instaloader.Instaloader()

    try:
        L.login(user, password)
    except TwoFactorAuthRequiredException:
        L.two_factor_login(auth)

    # Obtain profile metadata
    profile = instaloader.Profile.from_username(L.context, user)

    # Get lists of followers and following
    followers_list = {follower.username for follower in profile.get_followers()}
    following_list = {followee.username for followee in profile.get_followees()}

    # Find people not following back and not in lastChecked
    return [person for person in following_list if person not in followers_list and person not in lastChecked]
def main():
    userName = credentials.userName
    password = credentials.password
    auth_code= int('123691')
    file = "notFollowingBack.txt"

    # load old data
    old_list = readData(file)

    updated_notFollowingBack = getNotFollowingBack(userName, password, auth_code, old_list)

    # save new data to file
    writeData(file, updated_notFollowingBack)
    print(updated_notFollowingBack)
    print('Done')

if __name__ == "__main__":
    main()