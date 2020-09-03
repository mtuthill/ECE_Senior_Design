# ECE492
<br/>
To run UI on Windows: <br/>
Use command prompt
run "python3" which should bring up the windows store to install Python3. If not you'll need to be install python3
run "pip3 install PyQt5"
Then lastly run "python3 pythonUI.py" which should run the UI and load it

OR

Use a WSL running Ubuntu (or another distro) <br/>
<br/>
On the WSL: <br/>
Had to install PyQt5 using sudo apt-get install python3-pyqt5 <br/>
Had to install gnuplot-nox using sudo apt install gnuplot-nox <br/>
Had to install gnuplot-qt using sudo apt install gnuplot-qt <br/>
<br/>
On my Windows OS:<br/>
Had to download Xming X Server for Windows using the link below <br/>
https://sourceforge.net/projects/xming/ <br/>
<br/>
After that, should be able to run UI and see it show up in a Xming window<br/>
