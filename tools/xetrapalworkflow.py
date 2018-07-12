import sys
sys.path.append("/opt/xetrapal")
import xetrapal
import tweepy
import pandas
import datetime
import math

sys.path.append("/opt/livingdata/lib")



    #anandafb=ananda.get_fb_browser()


def get_tweet_density(tw,screen_name):
    last100=get_last_100_mentions(tw,screen_name)
    if "created_at" in last100.columns:
        last100['createdts']=last100.created_at.apply(lambda x:datetime.datetime.strptime(x.replace("+0000","UTC"),"%a %b %d %H:%M:%S %Z %Y"))
        m=last100.createdts.max()-last100.createdts.min()
        print m
        density=len(last100)/math.ceil(m.total_seconds()/3600)
        print screen_name,density
        
        return density
    else:
        return 0
def get_last_100_mentions(tw,screen_name):
    tweets=tw.search(q="@"+screen_name,count=100)['statuses']
    tweetsdf=pandas.DataFrame(tweets)
    return tweetsdf


def get_tweepy(twconfig,logger=xetrapal.astra.baselogger):
    app_key=twconfig.get("Twython",'app_key')
    app_secret=twconfig.get("Twython",'app_secret')
    oauth_token=twconfig.get("Twython",'oauth_token')
    oauth_token_secret=twconfig.get("Twython",'oauth_token_secret')
    auth=tweepy.OAuthHandler(app_key,app_secret)
    auth.set_access_token(oauth_token,oauth_token_secret)
    tweep=tweepy.API(auth)
    return tweep

def build_userdf(tweep,userlist,logger=xetrapal.astra.baselogger):
    users=[]
    logger.info("Getting list with owner unessentialist, slug indian-journalists")
    for member in tweepy.Cursor(tweep.list_members,"unessentialist","indian-journalists").items():
        users.append(member)
    logger.info("Getting list with owner arunram, slug indian-journalists")
    for member in tweepy.Cursor(tweep.list_members,"arunram","indian-journalists").items():
        users.append(member)
    logger.info("Getting list with owner brunogarcez, slug top-indian-journalists")
    for member in tweepy.Cursor(tweep.list_members,"brunogarcez","top-indian-journalists").items():
        users.append(member)
    logger.info("Getting list with owner edelman_india, slug indian-journalists")
    for member in tweepy.Cursor(tweep.list_members,"edelman_india","indian-journalists").items():
        users.append(member)
    logger.info("Getting list with owner ingridtherwath, slug india-journalists")
    for member in tweepy.Cursor(tweep.list_members,"ingridtherwath","india-journalists").items():
        users.append(member)
    logger.info("Getting users for added list")
    for name in userlist:
        try:
            users.append(tweep.get_user(screen_name=name))
        except:
            print name, "Oops!"
    userjson=[]
    for user in users:
        userjson.append(user._json)
    p=pandas.DataFrame(userjson)
    p=p.drop_duplicates(subset=['screen_name'])
    return p    


ananda=xetrapal.Xetrapal(configfile="/home/ananda/ab/ab.conf")
anandatw=ananda.get_twython()
anandagd=ananda.get_googledriver()
twconfig=xetrapal.karma.get_section(ananda.config,"Twython")
tweep=get_tweepy(twconfig)
