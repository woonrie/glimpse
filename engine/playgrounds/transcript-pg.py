from youtube_transcript_api import YouTubeTranscriptApi, YouTubeRequestFailed
from summa import summarizer
import json

def sum(text, ratio):
        sum = summarizer.summarize(text, ratio=ratio)
        return sum

def transcript_request(video):
        '''
        Retrieves/returns the transcript for a prompted video

        Args:
            (str) video: video link or id

        Returns: signal[]
            if error = [0] = (int) error_code

            else = [(int) 398, (str) transcript]
        '''
        try:
            if "youtube.com" in video:
                video_id = video.split("v=")[1].split("&")[0]
            elif "youtu.be" in video:
                video_id = video.split("/")[-1]
            else:
                try: 
                    transcript = ""
                    for item in YouTubeTranscriptApi.get_transcript(video):
                        transcript += item["text"] + " "
                    return [398, transcript] # SUCCESS
                except YouTubeRequestFailed as e:
                    return [401] #TRANSCRIPT NOT FOUND

        except Exception as e:
            return [400] # VIDEO NOT FOUND
    
        try: 
            transcript = ""
            for item in YouTubeTranscriptApi.get_transcript(video_id):
                transcript += item["text"] + " "
        
            if len(transcript) > 12000:
                tran = transcript[:10000]
                script = transcript[10000:]
                while True:
                    if len(script) > 2000:
                        script = sum(script, ratio=0.5)
                    else:
                        transcript = tran + " " + script
                        break
            
            
            return [398, transcript]  # SUCCESS

            

        except Exception as e:
            return [401,video] #TRANSCRIPT NOT FOUND

def test(video):
    transcript = transcript_request(video)
    if transcript[0] == 398:
        with open("transcript-dump.txt", "w") as file:
            file.write(transcript[1])
    elif transcript[0] == 401:
        print(transcript[0], +  " " + transcript[1])
    else:
        print(transcript[0])

'''
Transcript Playground - push changes to code above before main glimpse.py - Test below

Can pull up to 20 minutes of footage

Relevant Codes:
    [398] = Transcript request successful
    [400] = Video not found at link or id
    [401] = Transcript not found at valid link/id
'''

with open("C:/Users/morot/Documents/bmg/glimpse/engine/playgrounds/videos.json", "r") as file:
    videos = json.loads(file.read())

#
