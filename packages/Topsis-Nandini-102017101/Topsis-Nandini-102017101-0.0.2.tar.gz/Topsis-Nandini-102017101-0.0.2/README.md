<h1 class="code-line" data-line-start=0 data-line-end=1 ><a id="Project_Description_0"></a>Project Description</h1>
<h2 class="code-line" data-line-start=1 data-line-end=2 ><a id="TopsisNandini102017101_1"></a>Topsis-Nandini-102017101</h2>
<p class="has-line-data" data-line-start="2" data-line-end="4">Topsis-Nandini-102017101 is a Python Package implementing Topsis method used for multi-criteria decision analysis. Topsis stands for ‘Technique for Order of Preference by Similarity to Ideal Solution’.<br>
Topsis-Nandini-102017101 intends to make the process of TOPSIS simple in python.</p>
<p class="has-line-data" data-line-start="5" data-line-end="6">Key features of the package are -</p>
<ul>
<li class="has-line-data" data-line-start="6" data-line-end="7">Easy to use</li>
<li class="has-line-data" data-line-start="7" data-line-end="8">Numpy Based</li>
<li class="has-line-data" data-line-start="8" data-line-end="10">Ideal for Students</li>
</ul>
<h2 class="code-line" data-line-start=10 data-line-end=11 ><a id="Installation_10"></a>Installation</h2>
<p class="has-line-data" data-line-start="12" data-line-end="13">Use the package manager pip to install Topsis-Nandini-102017101</p>
<h2 class="code-line" data-line-start=14 data-line-end=15 ><a id="Syntax_14"></a>Syntax</h2>
<p class="has-line-data" data-line-start="15" data-line-end="16">Enter csv filename followed by .csv extentsion, then enter the weights vector with vector values separated by commas, followed by the impacts vector with comma separated signs (+,-) and output file name with .csv extension</p>
<pre><code class="has-line-data" data-line-start="17" data-line-end="19" class="language-sh">topsis &lt;InputDataFile&gt; &lt;Weights&gt; &lt;Impacts&gt; &lt;ResultFileName&gt;
</code></pre>
<p class="has-line-data" data-line-start="19" data-line-end="20">Example:</p>
<pre><code class="has-line-data" data-line-start="21" data-line-end="23" class="language-sh">topsis inputfile.csv “<span class="hljs-number">1</span>,<span class="hljs-number">1</span>,<span class="hljs-number">1</span>,<span class="hljs-number">2</span>” “+,+,-,+” result.csv
</code></pre>
<p class="has-line-data" data-line-start="23" data-line-end="24">or vectors can be entered without &quot; &quot;</p>
<pre><code class="has-line-data" data-line-start="25" data-line-end="27" class="language-sh">topsis inputfile.csv <span class="hljs-number">1</span>,<span class="hljs-number">1</span>,<span class="hljs-number">1</span>,<span class="hljs-number">2</span> +,+,-,+ result.csv
</code></pre>
<p class="has-line-data" data-line-start="27" data-line-end="28">But the second representation does not provide for inadvertent spaces between vector values. So, if the input string contains spaces, make sure to enclose it between double quotes (&quot; &quot;).</p>
<h1 class="code-line" data-line-start=29 data-line-end=30 ><a id="Example_29"></a>Example</h1>
<h3 class="code-line" data-line-start=31 data-line-end=32 ><a id="Sample_input_data_31"></a>Sample input data</h3>
<table class="table table-striped table-bordered">
<thead>
<tr>
<th>Fund Name</th>
<th>P1</th>
<th>P2</th>
<th>P3</th>
<th>P4</th>
<th>P5</th>
</tr>
</thead>
<tbody>
<tr>
<td>M1</td>
<td>0.65</td>
<td>0.42</td>
<td>5.3</td>
<td>43.8</td>
<td>12.54</td>
</tr>
<tr>
<td>M2</td>
<td>0.94</td>
<td>0.88</td>
<td>4</td>
<td>61.5</td>
<td>16.83</td>
</tr>
<tr>
<td>M3</td>
<td>0.72</td>
<td>0.52</td>
<td>3.2</td>
<td>69.7</td>
<td>18.54</td>
</tr>
<tr>
<td>M4</td>
<td>0.89</td>
<td>0.79</td>
<td>5.4</td>
<td>49</td>
<td>14.02</td>
</tr>
<tr>
<td>M5</td>
<td>0.75</td>
<td>0.56</td>
<td>6.9</td>
<td>49.4</td>
<td>14.4</td>
</tr>
<tr>
<td>M6</td>
<td>0.6</td>
<td>0.36</td>
<td>4.2</td>
<td>68.3</td>
<td>18.37</td>
</tr>
<tr>
<td>M7</td>
<td>0.89</td>
<td>0.79</td>
<td>6.7</td>
<td>44.6</td>
<td>13.25</td>
</tr>
<tr>
<td>M8</td>
<td>0.79</td>
<td>0.62</td>
<td>3.8</td>
<td>51.7</td>
<td>14.23</td>
</tr>
</tbody>
</table>
<p class="has-line-data" data-line-start="44" data-line-end="45">weights vector = [ 1 , 1 , 1 , 1 , 1 ]</p>
<p class="has-line-data" data-line-start="46" data-line-end="47">impacts vector = [ + , + , + , + , + ]</p>
<h3 class="code-line" data-line-start=48 data-line-end=49 ><a id="Sample_output_data_48"></a>Sample output data</h3>
<table class="table table-striped table-bordered">
<thead>
<tr>
<th>Fund Name</th>
<th>P1</th>
<th>P2</th>
<th>P3</th>
<th>P4</th>
<th>P5</th>
<th>Topsis Score</th>
<th>Rank</th>
</tr>
</thead>
<tbody>
<tr>
<td>M1</td>
<td>0.65</td>
<td>0.42</td>
<td>5.3</td>
<td>43.8</td>
<td>12.54</td>
<td>0.287855029</td>
<td>8</td>
</tr>
<tr>
<td>M2</td>
<td>0.94</td>
<td>0.88</td>
<td>4</td>
<td>61.5</td>
<td>16.83</td>
<td>0.631106388</td>
<td>2</td>
</tr>
<tr>
<td>M3</td>
<td>0.72</td>
<td>0.52</td>
<td>3.2</td>
<td>69.7</td>
<td>18.54</td>
<td>0.412672373</td>
<td>5</td>
</tr>
<tr>
<td>M4</td>
<td>0.89</td>
<td>0.79</td>
<td>5.4</td>
<td>49</td>
<td>14.02</td>
<td>0.605503106</td>
<td>3</td>
</tr>
<tr>
<td>M5</td>
<td>0.75</td>
<td>0.56</td>
<td>6.9</td>
<td>49.4</td>
<td>14.4</td>
<td>0.536194294</td>
<td>4</td>
</tr>
<tr>
<td>M6</td>
<td>0.6</td>
<td>0.36</td>
<td>4.2</td>
<td>68.3</td>
<td>18.37</td>
<td>0.36630047</td>
<td>7</td>
</tr>
<tr>
<td>M7</td>
<td>0.89</td>
<td>0.79</td>
<td>6.7</td>
<td>44.6</td>
<td>13.25</td>
<td>0.635938379</td>
<td>1</td>
</tr>
<tr>
<td>M8</td>
<td>0.79</td>
<td>0.62</td>
<td>3.8</td>
<td>51.7</td>
<td>14.23</td>
<td>0.373853804</td>
<td>6</td>
</tr>
</tbody>
</table>
<h3 class="code-line" data-line-start=61 data-line-end=62 ><a id="Please_Note_61"></a>Please Note:</h3>
<ul>
<li class="has-line-data" data-line-start="62" data-line-end="63">Categorical values are not handled</li>
<li class="has-line-data" data-line-start="63" data-line-end="67">Enter the path for your input csv file<br>
-Enter the weights vector with each weight separated by commas<br>
-Enter the impact vector with each impact separated by commas<br>
-Enter the name of csv file in which you want to store output dataframe.</li>
</ul>
<h2 class="code-line" data-line-start=70 data-line-end=71 ><a id="License_70"></a>License</h2>
<p class="has-line-data" data-line-start="72" data-line-end="73">MIT</p>
<p class="has-line-data" data-line-start="74" data-line-end="75"><strong>Free Software, Hell Yeah!</strong></p>