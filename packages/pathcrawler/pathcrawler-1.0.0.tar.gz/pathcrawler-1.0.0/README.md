# pathcrawler
Small utility because I got tired of typing more than one line to get a recursive list of pathlib.Path objects for a directory.<br>
Install using:
<pre>pip install pathcrawler</pre>
<br>
pathcrawler contains just three functions: crawl, get_directory_size, and format_size.<br>
crawl takes a starting directory and returns a recursive list of pathlib.Path objects for all files in the starting directory and its sub folders.<br>
get_directory_size takes a directory and returns the total size in bytes of the contents of the directory.<br>
format_size takes a number (presumed to be bytes) and returns it as a string rounded to two decimal places with the appropriate unit suffix.<br>
i.e. 
<pre>
>>>import pathcrawler
>>> pathcrawler.format_size(132458)
'132.46 kb'
</pre>
