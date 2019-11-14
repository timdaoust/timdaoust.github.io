## Generated Webiste

This website is just my personal site that hosts my art work.  Thanks very much for taking an interest in the code!

The website itself is built of 3 components
- A template I got from color lib.  You can find it at [here] (https://colorlib.com/wp/template/sonar/)
- Template files that are used to generate matching html.  Look for files called .template
- A python script - generate_website.py.  This script replaces macros in the .template files with appropriate code

### Updating the website

1.  Install Python 
2.  Run 
```
python generate_website.py
```
3.  Edit the .template files to change the website.  Look for sections marked {{section_name}}.  These sections are 
replaced by the relevant function in the python
4.  The python is mainly used to generate pages based on the files in the img/ directory. Simply change the files to change the gallery!

### Licence

You are welcome to use the code generate_website.py and the .template files for your own projects under the Apache 2.0 license. 

The images are copyrighted, and can only be used in accordance with the github fork policy.  You may not represent the images
as your own, and beyond the github user agreement you have no additional rights to the images
 

