from random import randint
import tweepy as tw
from datetime import date

NUMBER_OF_TWEETS = 32


def authorize():
    consumer_key = '5jDiXLd404QSfqy4uxTmgqBpN'
    consumer_secret = 'OzwUGFO6XsdwyAXemnjkRryimrbduzJ88b3wpuUD8v9zKcGPFI'
    access_token = '1095423038475157505-YbTSKnreAtj85pN0ojZNVVtbd5fvdQ'
    access_token_secret = '6cG8qGxXzI0N7fjFFoKEPfC88jikcaX5KxCrZpkoEZD51'

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tw.API(auth)


api = authorize()


def get_user():
    user = input("Enter the user's handle: ")
    user_stats = api.get_user(user)
    num_tweets = user_stats.statuses_count
    print(num_tweets)
    while num_tweets < NUMBER_OF_TWEETS:
        print("User does not have enough tweets to play the game")
        user = input("Enter the user's handle: ")
        user_stats = api.get_user(user)
        num_tweets = user_stats.statuses_count
    return user


def get_tweets(user):
    user = '%' + user + ' -filter:retweets -filter:replies'
    tweets = tw.Cursor(api.search, q=user, max_ids=user, include_rts=False, lang="en",
                                        since=date.today()).items(NUMBER_OF_TWEETS)
    all_tweets = [tweet.text for tweet in tweets]
    return all_tweets[:NUMBER_OF_TWEETS]


def twitter_game():
    play = 'Y'
    num_points = 0
    num_tries = 0
    game_type = input(
        "Enter Y if you want to choose the twitter handles to play with. \nOtherwise, "
        "enter N to play with Kanye and Elon: ")

    while (game_type.upper() != 'Y') and (game_type.upper() != 'N'):

        print("\nSilly! You have to enter Y or N to play the game! Try again.")
        game_type = input("Enter Y if you want to choose the twitter handles to play with. "
                          "\nOtherwise, enter N to play with Kanye and Elon: ")
    while play.upper() == 'Y':
        num_tries+=1
        if game_type.upper() == 'Y':
            user1 = get_user()
            user2 = get_user()
        else:
            user1 = "kanyewest"
            user2 = "elonmusk"

        user1_tweets = get_tweets(user1)
        user2_tweets = get_tweets(user2)

        tweet_position = randint(0, NUMBER_OF_TWEETS - 1)
        which_user = randint(1, 2)

        if which_user == 1:
            print(user1_tweets[tweet_position])

            guess = input("Enter the handle who you think tweeted this: ")

            if guess == user1:
                print("Congratulations, you get a point!")
                num_points+=1
            else:
                print("Aww shucks, you lose")
        else:
            print(user2_tweets[tweet_position])

            guess = input("Enter the handle who you think tweeted this: ")

            if guess == user2:
                print("Congratulations, you get a point!")
                num_points+=1
            else:
                print("Aww shucks, you lose")
        play = input("\nEnter Y if you want to keep playing: ")
    print("Number of total points: " + str(num_points))
    print("Number of total tries: " + str(num_tries))
    print("Percentage successful: " + str(num_points / num_tries * 100) + '%')


twitter_game()
