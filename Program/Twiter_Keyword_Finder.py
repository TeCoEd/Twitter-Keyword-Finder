### Twitter Trend Search###
### TeCoEd ###
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
import time;
import datetime
import sys, subprocess, urllib, time, tweepy
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(9, GPIO.OUT)

keyword = input("Please enter your keywords ")
#GPIO.setup(9, GPIO.IN)

'''variable to change XLS cell number to add next tweet'''
global cell_ref_number
cell_ref_number = 1

#############################################################
############### Connect to Google Spreadsheet ###############
#############################################################
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

###########################################################
##### Prepares Spreedsheet ################################
###########################################################
now = datetime.datetime.now()
print (now.strftime("%Y-%m-%d %H:%M"))
current_time = now.strftime("%Y-%m-%d %H:%M")
sheet = client.open("Dr Who Twitter Tracker").sheet1
sheet.update_acell('A1', 'Time')
sheet.update_acell('A2', current_time)
sheet.update_acell('A3', 'Keyword')
sheet.update_acell('A4', keyword)

####TWITTER SECTION###
# == OAuth Authentication ==###############
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key= '*******************************'
consumer_secret= '******************************************8'

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located 
# under "Your access token")
access_token= '******************************'
access_token_secret= '***********************************'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
#####################################################
############# Checks Keyword Tweets ##############
####################################################

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        global cell_ref_number

        GPIO.output(9, GPIO.LOW)
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print ('@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore')))

        time.sleep(5)
        
        print ('')

        ####This is the related tweeter message ###
        GPIO.output(9, GPIO.HIGH)

        message  = ('@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore')))
        
        print ("Found one")
        print (cell_ref_number)

        # use creds to create a client to interact with the Google Drive API
        #sheet = client.open("Dr Who Twitter Tracker").sheet1

        sheet.update_acell('B' + str(cell_ref_number), message)
        cell_ref_number = cell_ref_number + 1

        return True
       

    def on_error(self, status):
        print (status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    print ("Showing all new tweets for", keyword)

    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow dR wHO
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth, l)
    stream.filter(track=[keyword]) ###changed for test
