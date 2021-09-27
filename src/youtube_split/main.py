import os, pafy
import numpy as np
from scipy.io.wavfile import write
from resemblyzer import preprocess_wav, VoiceEncoder
from youtube_transcript_api import YouTubeTranscriptApi
from pydub import AudioSegment


def split_audio(target_audio, transcript, audio_title):
    directory = "./" + audio_title + "/"

    for i,line in enumerate(transcript):
        is_exist = os.path.exists(directory)
        if not is_exist:
            os.makedirs(directory)

        text = line["text"]
        start = line["start"]
        duration = line["duration"]
        start_ms = start*1000
        duration_ms = duration*1000
        segment = target_audio[start_ms:(start_ms+duration_ms)]
        segment.export(os.path.join(directory, audio_title + "_" + str(i) + '.wav'), format="wav")

def diarization(speakers, speaker_samples, wav, target_audio):
    if len(speakers) > 1:
        encoder = VoiceEncoder("cpu")
        print("Running the continuous embedding on cpu, this might take a while...")
        _, cont_embeds, wav_splits = encoder.embed_utterance(wav, return_partials=True, rate=32)
        speaker_embeds = [encoder.embed_utterance(speaker_wav) for speaker_wav in speaker_samples]
        similarity_dict = {name: cont_embeds @ speaker_embed for name, speaker_embed in zip(speakers, speaker_embeds)}
        
        audio = AudioSegment.empty()
        similarities = list(similarity_dict.values())[0].tolist()
        print(len(wav_splits))
        print(len(similarities))
        for i,s in enumerate(similarities):
            if i < len(wav_splits)-1:
                if s >0.75:
                    audio += target_audio[wav_splits[i].start:wav_splits[i+1].start]

        audio.export("joe.wav", format="wav")

    else:
        pass

target_url = "https://www.youtube.com/watch?v=2O-iLk1G_ng&t=3068s&ab_channel=PowerfulJRE"

speaker_1 = "joe_rogan"
speaker_2 = "bernie_sanders"

video = pafy.new(target_url)
bestaudio = video.getbestaudio()

audio_title = speaker_1 + "_" + speaker_2
bestaudio.download(audio_title + ".m4a")

videoid = video.videoid
transcript = YouTubeTranscriptApi.get_transcript(videoid)

target_audio = AudioSegment.from_file(audio_title + ".m4a")[0:2*60*1000]
target_audio.export(audio_title + ".wav", format="wav")
target_audio = AudioSegment.from_wav(audio_title + ".wav")

print("preprocessing")
wav = preprocess_wav(audio_title + ".wav")
print("splitting")
segments = [[8, 20], [58, 80]]
speaker_names = [speaker_1, speaker_2]
speaker_wavs = [wav[int(s[0] * target_audio.frame_rate):int(s[1] * target_audio.frame_rate)] for s in segments]

# split_audio(target_audio, transcript, audio_title)
diarization(speaker_names, speaker_wavs, wav, target_audio)
