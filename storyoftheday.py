import tweepy, json, datetime

auth=tweepy.OAuthHandler("LYuZ8TRRBuJ7IQcoyyZYwe0uy","eIwCZsZ4IOQqe8p3nI4ybAJHcShILcpmwYkzLXW5xLSTplzDRl")
auth.set_access_token("928145131886317568-6bAb5L7Xj9OfiPYfgGTfMrYG6kCdZjC", "iRivk0tnYtPHaTLlwNipd6pECm7RcOHrNp0hPVvqx8AWb")

api = tweepy.API(auth)
tweets={}
#use 5 hours to adjust from GMT to EST
enddate=datetime.datetime(year=datetime.date.today().year, month=datetime.date.today().month, day=datetime.date.today().day, hour=5)
startdate=enddate-datetime.timedelta(days=1)
accounts=["nytimes","WashingtonPost","TheEconomist","FoxNews","CNN","USATODAY","WSJ"]
data=[]
for name in accounts:
    #get latest 200 tweets from each account
    status=api.user_timeline(screen_name=name,count=200)
    for x in range(len(status)):
        data.append(status[x])
    lasttweet=json.loads(json.dumps(status[199]._json))
    #ensure that the 200 tweets covers the entire range. if not, keep pulling tweets
    while datetime.datetime.strptime(lasttweet["created_at"][:19]+lasttweet["created_at"][25:],"%a %b %d %H:%M:%S %Y")>startdate:
        morestatus=api.user_timeline(screen_name=name,count=200,max_id=lasttweet["id"])
        lasttweet=json.loads(json.dumps(morestatus[199]._json))
        for z in range(len(morestatus)):
            data.append(status[z])

for i in range(len(data)):
    tweet=json.loads(json.dumps(data[i]._json))
    tweet_created_date=datetime.datetime.strptime(tweet["created_at"][:19]+tweet["created_at"][25:],"%a %b %d %H:%M:%S %Y")
    if tweet_created_date>startdate and tweet_created_date<enddate:
        #find tweet score
        try: #is a retweet
            tweetscore=tweet["retweeted_status"]["favorite_count"]+3*tweet["retweet_count"]
        except: #regular tweet
            tweetscore=tweet["favorite_count"]+3*tweet["retweet_count"]
        #add to dictionary
        tweets[tweetscore]=tweet
besttweets=sorted(tweets.keys(), reverse=True)
for x in range(20):
    for y in range(x+1,100):
        if tweets[besttweets[x]]["text"][:20]==tweets[besttweets[y]]["text"][:20]:
            del besttweets[y]
for z in reversed(range(10)):
    api.update_status("Story #"+str(z+1)+" of "+str(startdate.strftime("%A"))+", from "+tweets[besttweets[z]]["user"]["name"]+": "+"http://twitter.com/tweets/statuses/"+tweets[besttweets[z]]["id_str"])
