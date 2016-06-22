Using Speech Recognition to Generate Subtitles from Video
=========================================================

**WARNING:** Speech recognition is only available in Gaupol 0.19.x.
Earlier versions don't have that feature and later versions are
currently waiting for the feature to be restored after the long delay it
took to port the `pocketsphinx` speech recognition library to GStreamer
1.0.

Making subtitles from scratch usually consists of two tedious tasks: (1)
figuring out the times when someone starts and ends speaking – in
subtitle length pieces – and (2) typing down text corresponding to that
speech. An approach often worth attempting is to automate a large part
of this work by using speech recognition to generate subtitles from
given video. This method cannot be expected to produce release quality
subtitles on its own, but it should provide a rough first draft, which
can be finished by usual manual methods. With most video sources, the
actual speech recognition cannot be expected to perform well, but voice
recognition should provide decent results for the start and end times of
subtitles. The extraction of those start and end times is the primary
point for this feature to exist in Gaupol and the likely sensible use
for this feature in a subtitling workflow.

Gaupol's speech recognition uses the [CMU Sphinx][sphinx] speech
recognition toolkit developed at Carnegie Mellon University – to be
exact, the `pocketsphinx` plugin for the [GStreamer][gstreamer]
multimedia framework.

We will begin with a description of the parameters that define how the
speech recognition operates, followed by general tips on how to use this
feature and how it fits in a subtitling workflow.

## Parameters

### Voice Recognition

There are three parameters to control the voice recognition, i.e. the
detection of the difference between speech and silence and splitting
detected speech into subtitle length pieces.

* **Noise level** defines the noise volume level. Anything below that
  level will be considered noise and above it speech. Lowering this
  level will cause more possible speech detected and raising this level
  will cause less possible speech detected.

* **Silence length** is the minimum amount (in milliseconds) of silence
  required to terminate the current subtitle and start a new one.
  Decreasing this length will result in a large amount of short
  subtitles and increasing this length will result in a small amount of
  long subtitles.

* **Advance length** is the amount (in milliseconds) by which detected
  subtitles are made to appear earlier (if the previous subtitle allows
  it). You might want subtitles to appear slightly before speech, since
  it takes a moment for the viewer to react to the appearance of a
  subtitle.

### Speech Recognition

Detected voice is further deciphered into words by three models: an
acoustic model, a phonetic dictionary and a language model. The default
models shipped with `pocketsphinx` are US English models. Models for
other languages can be downloaded from the
[CMU Sphinx directory][sphinx-models]. Acoustic models are directories
with multiple files, phonetic dictionaries are single files usually with
a `.dic` filename extension and language models are also single files
usually with a `.DMP` extension. For example, the default models shipped
with `pocketsphinx` are in a usual installation in the following files.

```
/usr/share/pocketsphinx/model
|-- hmm
|   `-- en_US
|       `-- hub4wsj_sc_8k
|           |-- feat.params
|           |-- mdef
|           |-- means
|           |-- noisedict
|           |-- sendump
|           |-- transition_matrices
|           `-- variances
`-- lm
    `-- en_US
        |-- cmu07a.dic
        `-- hub4.5000.DMP
```

The default English model might work for other languages as well if
you're only interested in voice recognition. If, on the other hand,
you're interested in speech recognition, you'll need language-specific
models. But be warned, the models you can download from CMU Sphinx,
might not work "out of the box".

Last, but not least, you can make your own models, tuned to your own
recording conditions, your own voice or your own language. See the
[CMU Sphinx wiki][sphinx-wiki] for instructions.

## Tips

Results will greatly depend on the cleanliness of the audio track you
use. For something like conference presentations with very little
background noise and the same person speaking the whole time to a good
quality microphone you can expect fairly good results. When there are
multiple speakers, different noise levels (e.g. different scenes of a
film) or disturbing non-verbal audio (e.g. background music or sound
effects) the results will be considerably worse.

Gaupol's speech recognition dialog is designed to allow experimentation.
You can start with default values for parameters and hit the
<kbd>Start</kbd> button. If the results look bad, hit the
<kbd>Stop</kbd> button, edit the parameters and start again. You'll
probably want to set the noise level low rather than high and the
silence length short rather than long, since it's easier to later delete
and merge subtitles than it is to create or split subtitles. Once you
find the right parameters to fit your particular video, let it process
all the way through and once done you can close the dialog. Among the
results you'll see subtitles with no text – only a number in square
brackets. This means that voice was detected, but it could not be
deciphered into words. These subtitles might often be non-verbal sounds
or speech in a different language.

Once you have the results of speech recognition, you might want to let
Gaupol extend the durations of those subtitles, since subtitles will
often disappear too soon if they end right when speaking ends. From
Gaupol's <kbd>Tools</kbd> menu select <kbd>Adjust Durations</kbd> and
set it to extend durations to match a reasonable reading speed.

After the automatic processing you'll need to manually go over the
subtitles checking the times and typing the text. See the documentation
on [creating subtitles](creating-subtitles.md) on how to best do that.

## Problems

### Speech Recognition Menu Item Is Unavailable

Speech recognition has been added in Gaupol version 0.19. If you have
Gaupol 0.19 or later installed, but the <kbd>Speech Recognition</kbd>
item in the <kbd>Tools</kbd> menu is grayed out, you're lacking some
dependency.

You need the [GStreamer][gstreamer] multimedia framework and its Python
bindings, as well as GStreamer plugins to decode whatever video and
audio formats you wish to use. To verify GStreamer is correctly
installed and accessible from Python, you should be able to import the
`gst` module at the Python prompt without error.

```
$ python
Python 2.6.7 (r267:88850, Jun 13 2011, 20:39:28)
[GCC 4.6.1 20110611 (prerelease)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import gst
>>>
```

From [CMU Sphinx][sphinx] you need `sphinxbase` and `pocketsphinx`. To
verify that these are installed correctly and accessible from GStreamer,
`gst-inspect` should be able to find plugins `vader` and `pocketsphinx`,
i.e. commands

```
gst-inspect vader
gst-inspect pocketsphinx
```

should both give a long output of the properties of those elements.

[gstreamer]: https://gstreamer.freedesktop.org/
[sphinx]: http://cmusphinx.sourceforge.net/
[sphinx-models]: https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/
[sphinx-wiki]: http://cmusphinx.sourceforge.net/wiki/
