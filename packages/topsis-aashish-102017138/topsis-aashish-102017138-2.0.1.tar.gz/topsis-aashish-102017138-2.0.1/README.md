<h1 class="code-line" data-line-start=0 data-line-end=1 ><a id="TopsisAashish102017138_0"></a>Topsis-aashish-102017138</h1>
<p class="has-line-data" data-line-start="3" data-line-end="4">Topsis-Aashish-102017138 is a Python library for handling problems related to Multiple Criteria Decision Making(MCDM) where there are more than one features to consider while arriving at a situation by using Technique for Order of Preference by Similarity to Ideal Solution(TOPSIS),we can make conclusions to help us arrive at the decision with minimal effort</p>
<h2 class="code-line" data-line-start=6 data-line-end=7 ><a id="Installation_6"></a>Installation</h2>
<p class="has-line-data" data-line-start="7" data-line-end="8">Use the package manager pip to install Topsis-Aashish-102017138</p>
<h2 class="code-line" data-line-start=9 data-line-end=10 ><a id="Syntax_9"></a>Syntax</h2>
<pre><code class="has-line-data" data-line-start="11" data-line-end="18" class="language-sh">topsis &lt;InputDataFile&gt; &lt;Weights&gt; &lt;Impacts&gt; &lt;ResultFileName&gt;
Example:
topsis inputfile.csv “<span class="hljs-number">1</span>,<span class="hljs-number">1</span>,<span class="hljs-number">1</span>,<span class="hljs-number">2</span>” “+,+,-,+” result.csv
or 
topsis inputfile.csv <span class="hljs-number">1</span>,<span class="hljs-number">1</span>,<span class="hljs-number">1</span>,<span class="hljs-number">2</span> +,+,-,+ result.csv

</code></pre>
<h2 class="code-line" data-line-start=21 data-line-end=22 ><a id="Example_21"></a>Example</h2>
<p class="has-line-data" data-line-start="23" data-line-end="24">Sample input data</p>
<table class="table table-striped table-bordered">
<thead>
<tr>
<th>Model</th>
<th>Corr</th>
<th>Rseq</th>
<th>RMSE</th>
<th>Accuracy</th>
</tr>
</thead>
<tbody>
<tr>
<td>M1</td>
<td>0.79</td>
<td>0.62</td>
<td>1.25</td>
<td>60.89</td>
</tr>
<tr>
<td>M2</td>
<td>0.66</td>
<td>0.44</td>
<td>2.89</td>
<td>63.07</td>
</tr>
<tr>
<td>M3</td>
<td>0.56</td>
<td>0.31</td>
<td>1.57</td>
<td>62.87</td>
</tr>
<tr>
<td>M4</td>
<td>0.82</td>
<td>0.67</td>
<td>2.68</td>
<td>70.19</td>
</tr>
<tr>
<td>M5</td>
<td>0.75</td>
<td>0.56</td>
<td>1.3</td>
<td>80.39</td>
</tr>
</tbody>
</table>
<h2 class="code-line" data-line-start=34 data-line-end=35 ><a id="Sample_Output_Data_34"></a>Sample Output Data</h2>
<table class="table table-striped table-bordered">
<thead>
<tr>
<th>Model</th>
<th>Corr</th>
<th>Rseq</th>
<th>RMSE</th>
<th>Accuracy</th>
<th>Topsis Score</th>
<th>Rank</th>
</tr>
</thead>
<tbody>
<tr>
<td>M1</td>
<td>0.79</td>
<td>0.62</td>
<td>1.25</td>
<td>60.89</td>
<td>0.7731301458119156</td>
<td>2</td>
</tr>
<tr>
<td>M2</td>
<td>0.66</td>
<td>0.44</td>
<td>2.89</td>
<td>63.07</td>
<td>0.22667595732024362</td>
<td>5</td>
</tr>
<tr>
<td>M3</td>
<td>0.56</td>
<td>0.31</td>
<td>1.57</td>
<td>62.87</td>
<td>0.4389494866695491</td>
<td>4</td>
</tr>
<tr>
<td>M4</td>
<td>0.82</td>
<td>0.67</td>
<td>2.68</td>
<td>70.19</td>
<td>0.5237626971836845</td>
<td>3</td>
</tr>
<tr>
<td>M5</td>
<td>0.75</td>
<td>0.56</td>
<td>1.3</td>
<td>80.39</td>
<td>0.8128626132980138</td>
<td>1</td>
</tr>
</tbody>
</table>
<h2 class="code-line" data-line-start=52 data-line-end=53 ><a id="License_52"></a>License</h2>
<p class="has-line-data" data-line-start="54" data-line-end="55">MIT</p>
