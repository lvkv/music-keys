# Music Keys - SBUHacks 2018

**Map microphone pitch to keystrokes**

## Inspiration
We've always had fun watching daredevils beat Dark Souls with Guitar Hero controllers and dance pads, but we've never seen anyone beat a video game with a _violin_. Well, wait no longer.

## How we built it
Our application uses your laptop microphone (via PyAudio) to continually listen for trigger frequencies within a certain volume threshold, which map to music notes ranging from C3 to B6. Our GUI front end (built with TkInter) listens for trigger notes, which are mapped (by the user) to specific keys. Our keystroke API (win32) then maps keys to keycodes and sends the actual keypress to the operating system, which then plays QWOP (or your choice of easy video game) in the most evil way possible.
## Challenges we ran into
We originally built the application on top of Electron and Node.js, but microphone permissions proved difficult, and we had to (we aren't kidding) modify actual node modules to get them to function on our machines (cough, _node-key-sender_). Not ideal. We then nuked our repo at midnight and basked in the glorious light of Python.
## Accomplishments that we're proud of
* UI Design
* Multithreading
* Extracting pitch and volume from mic input

## What we learned
We realized that different frameworks and languages offer different advantages over other depending on the purpose of the program. Sometimes it's just better to go back to the drawing board if means saving hours of headaches later!

## What's next for Music Keys
Dark Souls.
