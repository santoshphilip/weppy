txt = """<h1>weppy</h1>

<p>toy web interface for eppy</p>

<p>You can view the files but cannot edit it yet.</p>

<p>Shows some of the interconnections between the idf objects</p>

<h2>Installation</h2>

<p>clone weppy</p>

<p>git clone https://github.com/santoshphilip/weppy.git into a folder of your choice</p>

<p>create a virtual environment</p>

<p>pip install -r requirements.txt</p>

<p>Note: weppy uses a modified version of eppy. If you already have eppy installed, unistall it by doing <code>pip uninstall eppy</code> then do <code>pip install -r requirements.txt</code></p>

<h2>Running weppy</h2>

<p>cd to the folder where you cloned weppy</p>

<p>run:</p>

<p>python weppy.py</p>

<p>open "http://localhost:8080" in your browser</p>

<h2>Playing with weppy</h2>

<ul>
<li>open one of the idf files</li>
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
<ul><li>follow the new links</li></ul></li>
<li>go to PLANTLOOP
<ul><li>click on one of the loops</li>
<li>click on "show node connections"
<ul><li>It will show you what components this connected to.</li></ul></li></ul></li></ul></li>
</ul>

<p>You can try this with other objects</p>

<p>that is all so far.</p>

<h2>where do the idf files come from</h2>

<p>take a look at the file <code>idffilenames.txt</code></p>

<h2>where does the idd file come from</h2>

<p>It is hard coded in <code>eppystuff.py</code>. Change it if you need to.</p>

<h2>Notes</h2>

<p>This was written in about 2-3 days. Does not seem to break so far. It was written to assist me in a presentation on E+.</p>

"""