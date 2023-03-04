'''
Glimpse MVP - (no images)
Imports glimpse method:
    Takes in a YouTube link or video ID and returns a .md file blog

Architecture:
    1. Take Link
    2. Verify Link (id found & is valid video)
        ERROR 400: Video not Found
    3. Transcript Call
        ERROR 401: Transcript not found
    4. Use transcript to get blog
        ERROR 402: OpenAI could not generate a blog
    5. Return Blog to user

    transcript_request(video_link_or_id)
        Return Codes:
            [399, transcript] : Success
            [400] : Video not found
            [401] : Transcript not found at Video

'''
import openai
from youtube_transcript_api import YouTubeTranscriptApi, YouTubeRequestFailed


def glimpse(video):
    '''
    Returns a glimpse of a youtube video

    Args:
        (str) video: either a YT video link or id

    Returns:
        if error:
            (int) error_code: Corresponding to codes in file tag
        else:
            (str) blog: the blog for the prompted video  
    '''

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
                transcript = transcript[:12000]
            
            return [398, transcript]  # SUCCESS


        except Exception as e:
            return [401, video] #TRANSCRIPT NOT FOUND



    def blog_request(transcript):
        try:
            openai.api_key = "KEY"
            blog = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Write a long-form blog that discusses the main points in the following video transcript: {transcript}\
                    \nEnsure your response has a title and section headers formatted in markdown (.md) file format",
                temperature=0.5,
                max_tokens=1000
            ).choices[0].text
            return [399, blog]

        except Exception as e:
            return [402, e]


