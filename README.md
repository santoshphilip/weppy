# weppy
toy web interface for eppy

You can view the files but cannot edit it yet.

Shows some of the interconnections between the idf objects

## Installation
clone weppy

git clone https://github.com/santoshphilip/weppy.git into a folder of your choice

create a virtual environment

pip install -r requirements.txt

Note: weppy uses a modified version of eppy. If you already have eppy installed, unistall it by doing `pip uninstall eppy` then do `pip install -r requirements.txt`


## Running weppy
cd to the folder where you cloned weppy

run:

python weppy.py

open "http://localhost:8080" in your browser

## Playing with weppy
- open one of the idf files
- click on CONSTRUCTION
- click on one of the constructions
    - click on the "?"
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
            - It will hsoe you what components this connected to.

You can try this with other objects

that is all so far.

## where do the idf files come from
take a look at the file `idffilenames.txt`

## where does the idd file come from
It is hard coded in `eppystuff.py`. Change it if you need to.

## Notes
This was written in about 2-3 days. Does not seem to break so far. It was written to assist me in a presentation on E+.

