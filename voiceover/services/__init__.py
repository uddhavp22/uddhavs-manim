"""Speech backends.

Import the one you want directly, e.g.

    from voiceover.services.say import SayService

Each module is kept out of this namespace on purpose: importing the package
should never pull in gTTS, an API key check, or a microphone probe for a
service the scene does not use.
"""
