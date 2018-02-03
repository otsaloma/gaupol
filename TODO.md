Gaupol 1.3.2/1.4
================

* [x] Fix subtitles with special characters not being displayed by
      the internal video player (#74)
* [x] Update the `--video-file` argument to not just select the video
      file, but also load it in the internal video player (#75)
* [x] Mark gst-plugins-bad as required for using the built-in video
      player, due to the switch from autovideosink to gtksink that
      happened in Gaupol 1.3 (#73)
