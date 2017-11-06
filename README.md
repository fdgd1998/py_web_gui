# py_web_gui
Tiny RPC framework that enables Python to use a web view in a browser session as a GUI.

Prerequisites
-------------

In order to use the s04 infrastructure, you will need a computer with a linux-like terminal (I haven't tried building labs on Windows, but did make a reasonable effort at writing portable infrastructure). You will need `git` and `zip`. You will also need `python 2.7`.

While you won't need much to build the business logic of an assignment, you *will* require a PDF tool to build the assignment documents. In this repository, I do not include any complete assignment, but if you choose to use this code in its entirety, the following are prerequisites for building PDFs:

### Prerequisites for building PDF assignment documents

You will need `gem` (provided by a recent version of `ruby`), and `wkhtmltopdf` installed and available at a command line.

- Download and install `wkhtmltopdf` [here][wkhtmltopdf]. Don't use the one hosted by Ubuntu, it is missing some important components.
- Install the required gems: `gem install redcarpet github-markup`.

Building labs
-------------

To build a completed lab (create the `.zip` archives for funprog (as provided by the [igor][igor] project), and a solution), use the `make_assignment.py` script.
For example:

````
./make_assignment.py labs/gas
````
will create `.lab_1.zip`, `.analyzer_1.zip`, and `solution.lab_1/` - the complete set of files to be ever shipped to students.

Running the lab
---------------

A solution can be tested via `./test.py`, or `python test.py`.

Run the UI via `./server.py`, or `python server.py`, and use your favorite web browser (we tested everything on Chrome) to visit [localhost:8000](http://localhost:8000). If there are any problems, you can change the port number by editing `server.py`.

Creating new labs
-----------------

Each assignment *must* contain:

- `config.json`, which tells the framework everything it needs to know in order to biuld the assignment.
- a sub-folder `cases`, containing the `.in` and `.out` files with contiguous numeric names beginning with `1`.
- a sub-folder `resources`, containing anything that is needed by both the autograder and the UI (data sets, for example).
- `verifier.py`, which implements `verify( result, input_data, gold )`: comparing `result` produced by the student code against `gold`, which is the known good solution (the `.out` file). `input_data` (the `.in` file) is also available. If solutions are not unique, verifier should check an *invariant* which determines whether or not the solution is correct.
- `wrapper.py`, which implements `run_test( input_data )`: a function that knows how to invoke student code given `input_data` (the `.in` file).
- `empty.py`: the file students will work in to produce a solution.
- `solution.py`: a staff solution for the assignment.

Any documents  with the assignment (the assignment PDF, for example) can be written in [markdown][markdown], which is also used to format doucments on GitHub. Each markdown document to be built should be added to the `markdown` key in `config.json`.

Furthermore, if the assignment has a web-hosted UI (enabled via a flag in `config.json`), the UI belongs in a sub-folder `ui`.

[wkhtmltopdf]: http://wkhtmltopdf.org/downloads.html
[markdown]: https://help.github.com/articles/basic-writing-and-formatting-syntax/
[igor]: https://github.com/pwnall/igor
