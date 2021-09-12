#!/usr/bin/env python
# -*-coding:utf-8 -*-

from gtts import gTTS
from playsound import playsound
import win32com.client as win


def text2voice():
    """文字转语音 - 谷歌 gtts模块"""
    tts = gTTS(text="我人傻了, 刘辉真的没有偷我视频, 事情是这样的, 我发觉我很多视频都不适合推荐", lang="zh-CN")
    tts.save("test.mp3")
    playsound("test.mp3")


def word_pronunciation():
    speak = win.Dispatch("SAPI.SpVoice")
    speak.Speak("come on, baby!")
    speak.Speak("宝贝儿，你好!")



if __name__ == "__main__":
	text2voice()
	# word_pronunciation()