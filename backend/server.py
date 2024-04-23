import json
import sys
from flask import Flask, request
# For Fetching Comments 
from googleapiclient.discovery import build 
# For filtering comments 
import re 
# For filtering comments with just emojis 
import emoji
# Analyze the sentiments of the comment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# For visualization 
import matplotlib.pyplot as plt
import matplotlib
#to convert to base64
import io
import base64
#get transcript of video
from youtube_transcript_api import YouTubeTranscriptApi 
from youtube_transcript_api.formatters import TextFormatter
##
import google.generativeai as genai
##
matplotlib.use('Agg')

##################################




 






################################

app = Flask(__name__)


@app.route("/analyze",methods =['GET','POST'])
def analyze():
    
    API_KEY = 'AIzaSyDPFGdbuM5JLUDr1xXkZfSgRHTRkICzVd8'
    youtube = build('youtube', 'v3', developerKey=API_KEY) # initializing Youtube API
     
    # Taking for video id from json request
    video_idurl = request.json
    v1 = video_idurl.get("videoURL")
    video_id=v1[-11:]

    #getting captions from the video
    video_captions= YouTubeTranscriptApi.get_transcript(video_id)
    formatter = TextFormatter()
    captions = formatter.format_transcript(video_captions).replace("\n", " ")
    summary=summarizeText(captions)
    # captions = []
    # for text in video_captions:
    #     txt= text.get('text')
    #    # print(txt,sys.stderr)
    #     captions.append(txt)
    #     print('\n\n\n')
    print(captions)


    
    # Getting the channelId of the video uploader
    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()
            
    
    print(video_response, file=sys.stderr)
    
    # Splitting the response for channelID
    video_snippet = video_response['items'][0]['snippet']
    uploader_channel_id = video_snippet['channelId']
    comments = []
    nextPageToken = None
    while len(comments) < 600:
        reques = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100,  # You can fetch up to 100 comments per request
            pageToken=nextPageToken
        )
        response = reques.execute()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            # Check if the comment is not from the video uploader
            if comment['authorChannelId']['value'] != uploader_channel_id:
                comments.append(comment['textDisplay'])
        nextPageToken = response.get('nextPageToken')
    
        if not nextPageToken:
            break
    # Print the 5 comments
     #   print('\n\n',sys.stderr)
       # print(comments[:5],sys.stderr)


    
  



    #########################################Filtering comments####################################################



    hyperlink_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    
    threshold_ratio = 0.65
    
    relevant_comments = []
    
    # Inside your loop that processes comments
    for comment_text in comments:
    
        comment_text = comment_text.lower().strip()
    
        emojis = emoji.emoji_count(comment_text)
    
        # Count text characters (excluding spaces)
        text_characters = len(re.sub(r'\s', '', comment_text))
    
        if (any(char.isalnum() for char in comment_text)) and not hyperlink_pattern.search(comment_text):
            if emojis == 0 or (text_characters / (text_characters + emojis)) > threshold_ratio:
                relevant_comments.append(comment_text)
    
    # Print the relevant comments
    #print('\n\n',sys.stderr)
    #print(relevant_comments[:5],sys.stderr)
                
    ###########################################Storing comments###############################################################


    f = open("ytcomments.txt", 'w', encoding='utf-8')
    for idx, comment in enumerate(relevant_comments):
        f.write(str(comment)+"\n")
    f.close()
    #print('\n\n',sys.stderr)
    #print("Comments stored successfully!",sys.stderr)



    ###########################################Analyzing comments###############################################################


    def sentiment_scores(comment, polarity):
    
        # Creating a SentimentIntensityAnalyzer object.
        sentiment_object = SentimentIntensityAnalyzer()
    
        sentiment_dict = sentiment_object.polarity_scores(comment)
        polarity.append(sentiment_dict['compound'])
    
        return polarity
 
        
    polarity = []
    positive_comments = []
    negative_comments = []
    neutral_comments = []
    
    f = open("ytcomments.txt", 'r', encoding='`utf-8')
    comments = f.readlines()
    f.close()
    print("Analysing Comments...")
    for index, items in enumerate(comments):
        polarity = sentiment_scores(items, polarity)
    
        if polarity[-1] > 0.05:
            positive_comments.append(items)
        elif polarity[-1] < -0.05:
            negative_comments.append(items)
        else:
            neutral_comments.append(items)
    
    # Print polarity
    #print('\n\n',sys.stderr)

    #print(polarity[:5],sys.stderr)
    #########################################Overall polarity###################################################


    avg_polarity = sum(polarity)/len(polarity)
    print("\n Average Polarity:", avg_polarity)
    if avg_polarity > 0.05:
        Response_of = "The Video has got a Positive response"
        print("\n The Video has got a Positive response")
    elif avg_polarity < -0.05:
        print("\n The Video has got a Negative response")
        Response_of = "The Video has got a negative response"
    else:
        print("\n The Video has got a Neutral response")
        Response_of = "The Video has got a Neutral response"
    
    print("\n The comment with most positive sentiment:", comments[polarity.index(max(
        polarity))], "with score", max(polarity), "and length", len(comments[polarity.index(max(polarity))]),sys.stderr)
    print("\nThe comment with most negative sentiment:", comments[polarity.index(min(
        polarity))], "with score", min(polarity), "and length", len(comments[polarity.index(min(polarity))]),sys.stderr)

    ###########################################Plotting graphs########################################################


    positive_count = len(positive_comments)
    negative_count = len(negative_comments)
    neutral_count = len(neutral_comments)
    
    # labels and data for Bar chart
    labels = ['Positive', 'Negative', 'Neutral']
    comment_counts = [positive_count, negative_count, neutral_count]
    
    # Creating bar chart
    plt.bar(labels, comment_counts, color=['blue', 'red', 'grey'])
    
    # Adding labels and title to the plot
    plt.xlabel('Sentiment')
    plt.ylabel('Comment Count')
    plt.title('Sentiment Analysis of Comments')
    
    # Displaying the chart
    #dia = plt.show()
    ##################

    s = io.BytesIO()
    plt.savefig(s, format='png')
    plt.close()
    s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
    

      
    ######################

    my_json_string = json.dumps({'Response_of': Response_of ,'video_id': video_id, 'video_response': video_response,'channel_ID':uploader_channel_id,'fig':s, 'Summary': summary})
    return(my_json_string)

#########################################################################################################

# AIzaSyB0DRi0H3GFCvgiiE5U4eoVOqSubll-b6k
def summarizeText(transcript_text):
    
    genai.configure(api_key="AIzaSyB0DRi0H3GFCvgiiE5U4eoVOqSubll-b6k")
    prompt = """Welcome, Video Summarizer! Your task is to distill the essence of a given YouTube video transcript into a concise summary. Your summary should capture the key points and essential information, presented in bullet points, within a 250-word limit. Let's dive into the provided transcript and extract the vital details for our audience."""
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

####################################################################################################################




if __name__ == "__main__":
    app.run(debug=True)