# Change 1

## Better Transcripts 

### Current Benchmarks
	Highest blogged transcript = 12000


### Log:

  File(s): transcript-pg.py & glimpe-pg.py
	
	* Changed "transcript_request". 
		For any transcripts longer than 12k chars (longest openai accepts), the transcript is parsed into 2:
			1 - transcript[:10000]
			2 - transcript[10000:]
			
		And (2) is summarized until it is less than 2k chars. Finally, they are joined

	* 402 error dumps
