pushstore_parser.py
===================
A simple python script to parse Apple Push Notification service files (".pushstore").

About
-----
`pushstore_parser.py` is designed to parse ".pushstore" files found on iOS devices for potential forensic artifacts. These files are typically found in the `/var/mobile/Library/SpringBoard/PushStore/` directory, and are stored in a binary Property List ("plist") format. Specifically, they are `NSKeyedArchiver` formatted plists. I highly recommend reading [this blog post](https://www.mac4n6.com/blog/2016/1/1/manual-analysis-of-nskeyedarchiver-formatted-plist-files-a-review-of-the-new-os-x-1011-recent-items) on parsing and understanding `NSKeyedArchiver` plists.

Setup
-----
`pushstore_parser.py` uses the `biplist` module available from `pip`. It can be installed using the following command:

    pip install -r requirements.txt

Usage
-----
After extracting the plist files from a test device, you can run `pushstore_parser.py` as follows:

    $ python pushstore_parser.py com.apple.TestFlight.pushstore
    AppNotificationCreationDate|RequestedDate|TriggerDate|AppNotificationMessage
    2016-09-21 14:41:24.782053|N/A|N/A|Silly App 0.2.3 (0.2.3) is now available for testing.
    2016-09-21 14:13:04.631264|N/A|N/A|Silly App 0.2.3 (0.2.3) is now available for testing.

Timestamps will be in UTC time.

License
-------
`pushstore_parser.py` is licened under the Apache License, Version 2.0. This means it is freely available for use and modification in a personal and professional capacity.
