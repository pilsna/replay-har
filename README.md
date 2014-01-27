replay-har
==========

A command line tool for replaying HTTP archive files.
It reads HTTP archive files (.har) as input and outputs CSV files.
The tool replays all the requests and measures response size and time. 
It's supposed to provide a way of measuring the speed of the internet connection in different locations.

The tool has been tested with HAR files genereted in Chrome Developer tools and Fiddler4.

To build the .exe file, execute this command:
python setup.exe py2exe

To distribute this tool, place the replayHAR.exe in the root of a folder.
Create a folder called data, and place the .har files inside that folder.
