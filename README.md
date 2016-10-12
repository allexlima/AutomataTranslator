# Welcome to AutomataTranslator
Automata AFN to AFD translation algorithm

### Workspace tips

We advise you to use these tools to make easier your work and save time:

1. Some unix-based OS as [Debian](http://debian.org), [Ubuntu](http://www.ubuntu.com/) or [OSX](http://www.apple.com/in/osx/);
2. [PyCharm IDE](https://www.jetbrains.com/pycharm) (it's [free for students](https://www.jetbrains.com/student/));
3. [JFLAP](http://www.jflap.org/) can be useful for designing your *nondeterministic finite automata* and quickly translate it to *deterministic finite automata through* AutomataTranslator.

### Requirements [not pip-installable]

1. **Python 2.7.x** 
    Download Python 2.7.x interpreter [here](https://www.python.org/).

2. **PyQt4** 
    If you are using debian-based system you can install it using the command: 

    ```
    $ sudo apt-get install python-qt4
    ```

    Otherwise, you can find a compatible version with your system in [PyQt official website](https://www.riverbankcomputing.com/software/pyqt/download).

### Setup

1. Clone the repo

    ```
	$ git clone https://github.com/allexlima/AutomataTranslator.git
	$ cd AutomataTranslator/
	```

2. Create Python Virtual Environment

    ```
	$ virtualenv --no-site-packages env
	```

3. Enable Python Virtual Environment 

    ```
    $ source env/bin/activate
    ```

4. Install the pip-installable dependencies

    ```
	$ pip install -r requirements.txt
    ```

5. Run the **AutomataTranslator**

    ```
	$ python app.py
    ```


For more details and explanations, please read AutomataTranslator our [Wiki](https://github.com/allexlima/AutomataTranslator/wiki).