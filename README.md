For Mac OS X, you can use `Homebrew`::

    brew install portaudio

For Debian / Ubuntu Linux::

    apt-get install portaudio19-dev python-all-dev

Install python dependencies::

    make requirements

Add google auth json file in config with the name google-auth.json


Extract audio from video::

    bin/process_raw [input video directory] [output audio directory]


Extract text from audio::

    bin/extract_text [input audio directory] [output text directory] <options>


Extract entities from text::

    bin/extract_entity [input text directory] [output entity directory] <options>
