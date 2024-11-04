#! /opt/homebrew/bin/python3.11
import instaloader
from instaloader.exceptions import TwoFactorAuthRequiredException
import credentials
from notifications import Notification
import argparse
import os

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
            f.write(f"{items}\n")
def getNotFollowingBack(L, lastChecked, target):

    
    # Obtain profile metadata
    profile = instaloader.Profile.from_username(L.context, target)

    # Get lists of followers and following
    followers_list = {follower.username for follower in profile.get_followers()}
    following_list = {followee.username for followee in profile.get_followees()}

    # Find people not following back and not in lastChecked
    return [person for person in following_list if person not in followers_list and person not in lastChecked]
def send_notification(names):
    noti = Notification(credentials.pushOver_appToken, credentials.pushOver_userKey)

    if names:
        try:
            noti.send_textNotification(credentials.pushOver_device, names)
        except:
            print('There was a issue sending the notification')
    else:
        print('Nothing to send in body of message')

def download_posts(L,  target_user):
    download_path = "downloads"
    L = instaloader.Instaloader(download_videos=False, save_metadata=False, compress_json=False)
    
    # Set download path
    L.dirname_pattern = os.path.join(download_path, "{target}")

    # Obtain profile metadata and download posts
    profile = instaloader.Profile.from_username(L.context, target_user)
    try:
        all_posts = profile.get_posts()
        for i, post in enumerate(all_posts):
            if i >= 15:  # Download only the last 15 posts
                break
            L.download_post(post, target=target_user)
        print("Download completed successfully.")
    except Exception as e:
        print(f"There was an issue downloading posts: {e}")
def login(user, password, mfa_code):
    session_file = credentials.last_session
    L = instaloader.Instaloader()
    
    try:
        if os.path.exists(session_file):
            L.load_session_from_file(user, session_file)
        else:
            raise FileNotFoundError  # Trigger login process if file doesn't exist
    except (FileNotFoundError):
        print("Session file not found or invalid. Logging in with 2FA auth code...")
        try:
            # Login with username and password
            L.login(user, password)
        except TwoFactorAuthRequiredException:
            L.two_factor_login(mfa_code)

    # Save the session after successful login
    L.save_session_to_file(session_file)
    return L
def main():
    
    userName = credentials.userName
    password = credentials.password
    file = credentials.last_run

    desc = "Program to check not following back accounts on instagram using instaloader"
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-c', '--auth_code', dest='auth_code', help='Current 2fa code required to login to get profile details')
    parser.add_argument('-d', action="store_true", help='Add the -d flag to download images') # enable download mode
    parser.add_argument('-u', '--user-target', nargs='+', type=str,  dest="user_target", help="List of one or more usernames" )
    args = parser.parse_args()
    
    auth_code = args.auth_code
    user_target = args.user_target

    # if download mode is enabled ensure a name is also provided to run on
    if args.d and not user_target:
        parser.error("List of usernames is required when download mode is enabled")

    insta = login(userName, password, auth_code)

    # load old data
    old_list = readData(file)

    print("Using credentials file in CWD for login details.....")
    if not args.d:
        updated_notFollowingBack = getNotFollowingBack(insta,  old_list, userName)

        # save new data to file
        writeData(file, updated_notFollowingBack)

        if updated_notFollowingBack:
            print('Sending notification with the results')
        else:
            print('No change since last check')

    if args.d:
        for creator in user_target:
            download_posts(insta, creator.strip())

    print('Done')

if __name__ == "__main__":
    main()