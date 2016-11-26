txt = """
<h1>weppy</h1>

<p>toy web viewer for eppy</p>

<p>You can view the files but cannot edit it yet.</p>

<p>Shows some of the interconnections between the idf objects</p>

<h2>Playing with weppy</h2>

<ul>
<li>open one of the idf files (5ZoneReturnFan.idf is a good one)</li>
<li>click on CONSTRUCTION</li>
<li>click on one of the constructions
<ul><li>click on the "?"</li>
<li>click on "docs"</li>
<li>click on "show links to other objects"
<ul><li>follow the new links</li>
<li>go back</li></ul></li>
<li>click on "run functions of this object"
<ul><li>go back</li></ul></li>
<li>click on "Show objects that mention this object"
<ul><li>follow the new links</li></ul></li></ul></li>
<li>go to PLANTLOOP
<ul><li>click on one of the loops</li>
<li>click on "show node connections"
<ul><li>It will show you what components this connected to.</li></ul></li></ul></li>
<li>go to CHILLER:ELECTRICS
<ul><li>click on "Central Chiller"</li>
<li>at the bottom of that page click on "prev objects &amp; next objects"
<ul><li>will show you a list of objects the chiller is connected to with a diagram of the connection</li></ul></li></ul></li>
</ul>

<p>You can try this with other objects</p>

<p>that is all so far.</p>

<h2>Notes</h2>

<ul>
<li>Weppy was initially written in about 2-3 days. It was written to assist in a presentation on E+.</li>
<li>Now it has become a useful tool to understand how E+ builds it's HVAC.</li>
<li>This understanding is being used to further develop functions in <a href="https://github.com/santoshphilip/eppy">eppy</a></li>
<li>Apart from this, weppy is showing potential for being a good viewer for E+.</li>
<li>You are welcome to fork it and build such a viewer.
<ul><li>the eppy team may be motivated to write functions that will assist you in this.</li></ul></li>
<li>Any comments or ideas for further development can be posted as an issue (or as a comment in an issue) in <a href="https://github.com/santoshphilip/weppy/issues">weppy</a></li>
</ul>

<h2>Installation</h2>

<ul>
<li>clone weppy</li>
<li><code>git clone https://github.com/santoshphilip/weppy.git</code> into a folder of your choice</li>
<li>create a virtual environment</li>
<li>pip install -r requirements.txt</li>
</ul>

<p>Note 1: weppy uses a modified version of eppy. If you already have eppy installed, unistall it by doing <code>pip uninstall eppy</code> then do <code>pip install -r requirements.txt</code></p>

<p>Note 2:Install <code>graphviz</code> from <a href="http://www.graphviz.org/">here</a> to view the diagrams</p>

<h2>Running weppy</h2>

<ul>
<li>cd to the folder where you cloned weppy</li>
<li><code>python weppy.py</code></li>
<li>open "http://localhost:8080" in your browser</li>
</ul>

<h2>where do the idf files come from</h2>

<p>take a look at the file <code>idffilenames.txt</code></p>

<h2>where does the idd file come from</h2>

<p>It is hard coded in <code>eppystuff.py</code>. Change it if you need to.</p>

"""