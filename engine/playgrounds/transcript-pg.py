from youtube_transcript_api import YouTubeTranscriptApi, YouTubeRequestFailed

def transcript_request(video):
    '''
    Retrieves/returns the transcript for a prompted video

    Args:
        (str) video: video link or id

    Returns: signal[]
        if error = [0] = (int) error_code

        else = [(int) 398, (str) transcript]

    Return Codes:
        398 - Success
        400 - Transcript not found
    '''
    if "youtube.com" in video:
        video_id = video.split("v=")[1].split("&")[0]
    elif "youtu.be" in video:
        video_id = video.split("/")[-1]
    else:
        video_id = video
    try: 
        transcript = ""
        for item in YouTubeTranscriptApi.get_transcript(video_id):
            transcript += item["text"] + " "

        if len(transcript) > 12000:
            transcript = transcript[:12000]

        return [398, transcript] # SUCCESS

    except Exception:
        return [400, video_id] #TRANSCRIPT NOT FOUND 



# Method that takes in tuples of transcript inputs and expected outputs, runs them, and returns results of tests

def run_tests(tests):
    '''
    Method that takes in tuples of transcript inputs and expected outputs, runs them, and returns results of tests

    Args:
        tuple array - tests: list of tuples, each containing (str) input and (str) expected output

    Returns: (str) results of tests
    '''
    results = []
    for case in tests:
        request = transcript_request(case[0])
        if request[0] == case[1]:
            results.append("Success")
        else:
            results.append("Failure - Expected: " + str(case[1]) + " | Actual: " + str(request[0]))
    return results
# Test cases
tests = [("https://www.youtube.com/watch?v=G6uwkc11NZ8", 398), 
         ("https://www.youtube.com/watch?v=Guwkc11NZ8", 400),
         ("G6uwkc11NZ8", 398)]

# Run tests
results = run_tests(tests)
for result in results:
    print(result)
