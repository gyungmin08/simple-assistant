class Speech:
    def __init__(self):
        self.r = sr.Recognizer()
        self.config = ConfigParser()
        self.config.read("config.ini", encoding="utf-8")

        self.username = self.config["user"]["username"]
        self.windows_username = getpass.getuser()
        self.download_path = os.path.join("C:\\Users", self.windows_username, "Downloads")

        self.copy_key = ["ctrl", "c"]
        self.paste_key = ["ctrl", "v"]

        self.yes = ["응", "그래", "오케이", "오케", "알았어", "고마워", "좋아", "예스"]
        self.no = ["아니", "아니야", "싫어", "노", "안돼"]

        self.func1_call = ["안녕"]
        self.func2_call = ["컴퓨터 꺼 줘", "컴퓨터 꺼줘"]
        self.func3_call = ["잘가"]
        self.func4_call = ["유튜브"]
        self.func4_mp4 = ["영상", "영상만"]
        self.func4_mp3 = ["오디오", "오디오만", "소리", "음악", "소리만", "음악만"]

        self.func1()

        text = self.listenKorean()
        if text is not None:
            print(text)
            self.AISpeaker(text)
        else:
            self.textToSpeech("알아듣지 못했어요.")


    def listenKorean(self, phrase_time_limit=5):
        with sr.Microphone() as source:
            audio = self.r.listen(source, phrase_time_limit=phrase_time_limit)
        try:
            text = self.r.recognize_google(audio, language="ko-KR")
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print(e)
            return None


    def AISpeaker(self, text):
        if self.jaroDistance(text, ["안녕"]):
            self.func1()
        elif self.jaroDistance(text, ["컴퓨터 꺼 줘"]):
            self.func2()
        elif self.jaroDistance(text, ["유튜브"]):
            print()
            self.func3()
        else:
            self.textToSpeech("알아듣지 못했어요.")


    def func1(self):
        self.textToSpeech(f"안녕하세요 {self.username}님. 무엇을 도와드릴까요?")


    def func2(self):
        self.textToSpeech("정말 컴퓨터를 끌까요?")
        text = self.listenKorean()
        print(text)
        if self.jaroDistance(text, self.yes):
            self.textToSpeech("컴퓨터를 끌게요.")
            os.system("shutdown -s")
        elif self.jaroDistance(text, self.no):
            self.textToSpeech("작업을 취소할게요.")
        else:
            self.textToSpeech("알아듣지 못했어요.")


    def func3(self):
        self.textToSpeech("영상을 다운로드할까요? 오디오를 다운로드할까요?")
        text = self.listenKorean()


        if self.jaroDistance(text, ["영상", "영상만"]):
            self.textToSpeech("링크를 선택해 주세요.")
            time.sleep(1)
            self.textToSpeech("영상 다운로드를 시작할게요.")
            pyautogui.hotkey("ctrl", "c")
            url = pyperclip.paste()
            os.system(f"youtube-dl -f mp4 {url} -o {self.download_path}\\{url.split('/')[-1]}.mp4")


        elif self.jaroDistance(text, ["오디오", "오디오만", "소리", "음악", "소리만", "음악만"]):
            self.textToSpeech("링크를 선택해 주세요.")
            time.sleep(1)
            self.textToSpeech("오디오 다운로드를 시작할게요.")
            pyautogui.hotkey("ctrl", "c")
            url = pyperclip.paste()
            os.system(f"youtube-dl -f bestaudio {url} -o {self.download_path}\\{url.split('/')[-1]}.mp3")

        self.textToSpeech("다운로드를 완료했어요.")


    def textToSpeech(self, text):
        audiofile_path = f"audio/output.mp3"

        tts = gTTS(text=text, lang="ko")
        tts.save(audiofile_path)
        playsound2.playsound(audiofile_path)


    def jaroDistance(self, text, textlist, threshold=0.8):
        if len(textlist) > 0:
            j = 0
            for i in textlist:
                if jellyfish.jaro_distance(text, i) > threshold:
                    j += 1
            if j != 0:
                if len(textlist) / j > threshold:
                    return True
        else:
            if jellyfish.jaro_distance(text1, text2) > threshold:
                return True


if __name__ == "__main__":
    import speech_recognition as sr
    from gtts import gTTS
    import playsound2
    import os
    import os.path
    import jellyfish
    from configparser import ConfigParser
    import getpass
    import pyautogui
    import pyperclip
    import time

    Speech()
