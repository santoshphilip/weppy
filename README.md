# weppy
toy web viewer for eppy

You can view the files but cannot edit it yet.

Shows some of the interconnections between the idf objects

## Playing with weppy
- open one of the idf files (5ZoneReturnFan.idf is a good one)
- click on CONSTRUCTION
- click on one of the constructions
    - click on the "?"
    - click on "docs"
    - click on "show links to other objects"
        - follow the new links
        - go back
    - click on "run functions of this object"
        - go back
    - click on "Show objects that mention this object"
        - follow the new links
- go to PLANTLOOP
    - click on one of the loops
    - click on "show node connections"
        - It will show you what components this connected to.
- go to CHILLER:ELECTRICS
    - click on "Central Chiller"
    - at the bottom of that page click on "prev objects & next objects"
        - will show you a list of objects the chiller is connected to with a diagram of the connection

You can try this with other objects

that is all so far.

## Notes
- Weppy was initially written in about 2-3 days. It was written to assist in a presentation on E+.
- Now it has become a useful tool to understand how E+ builds it's HVAC.
- This understanding is being used to further develop functions in [eppy](https://github.com/santoshphilip/eppy)
- Apart from this, weppy is showing potential for being a good viewer for E+.
- You are welcome to fork it and build such a viewer.
    - the eppy team may be motivated to write functions that will assist you in this.
- Any comments or ideas for further development can be posted as an issue (or as a comment in an issue) in [weppy](https://github.com/santoshphilip/weppy/issues)

## Installation
- clone weppy
- `git clone https://github.com/santoshphilip/weppy.git` into a folder of your choice
- create a virtual environment
- pip install -r requirements.txt

Note 1: weppy uses a modified version of eppy. If you already have eppy installed, unistall it by doing `pip uninstall eppy` then do `pip install -r requirements.txt`

Note 2:Install `graphviz` from [here](http://www.graphviz.org/) to view the diagrams

## Running weppy
- cd to the folder where you cloned weppy
- `python weppy.py`
- open "http://localhost:8080" in your browser


## where do the idf files come from
take a look at the file `idffilenames.txt`

## where does the idd file come from
It is hard coded in `eppystuff.py`. Change it if you need to.


