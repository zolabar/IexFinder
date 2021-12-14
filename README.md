<img src=Figures/fig2.svg height='200' >

# IexFinder: Interactive Symbolic Calculation of Extreme Values

[![DOI](https://zenodo.org/badge/424138887.svg)](https://zenodo.org/badge/latestdoi/424138887) Jupyter Lab: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/zolabar/IexFinder/HEAD) Voila Web App: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/zolabar/iexfinder/main?urlpath=voila%2Frender%2F/iexfinder_voila.ipynb)(**Binder**) [![example badge](Figures/succeeded.svg)](https://iexfinder.herokuapp.com/)(**Heroku**)


***Zoufiné Lauer-Baré*** ([LinkedIn](https://www.linkedin.com/in/zoufine-lauer-bare-14677a77)) <div itemscope itemtype="https://schema.org/Person"><a itemprop="sameAs" content="https://orcid.org/0000-0002-7083-6909" href="https://orcid.org/0000-0002-7083-6909" target="orcid.widget" rel="me noopener noreferrer" style="vertical-align:top;"><img src="https://orcid.org/sites/default/files/images/orcid_16x16.png" style="width:1em;margin-right:.5em;" alt="ORCID iD icon">https://orcid.org/0000-0002-7083-6909</a></div>

## Description

The ```exFinder``` web application calculates and visualizes the extreme values of multivariate functions: 
<img src="https://render.githubusercontent.com/render/math?math=f:\mathbb{R}^2\to\mathbb{R}">

It is based mathematically on ```SymPy``` and ```NumPy``` and graphically on ```Jupyter Notebook```, ```Plotly``` and ```Voila```. It has step by step features, based on  finding and characterizing stationary points by using the gradient and the Hessian, e.g. [[Alt, 2002]](https://link.springer.com/book/10.1007/978-3-322-84904-5). 

The exFinder project is listed in the [Voila Gallery](https://voila-gallery.org/). 

Mention this project as

*Lauer-Bare, Z. (2021). IexFinder -  Interactive Symbolic Calculation of Extreme Values (Version v1.0.2) [Computer software].* https://doi.org/10.5281/zenodo.5707405


**Usage:** Enter a function in *x* and *y* in Pythonic form into the input field and click on the update button.

<img src=Figures/exFinder_usage_5.PNG >



## References

[Alt, 2002] Alt W. Nichtlineare Optimierung: Eine Einführung in Theorie, Verfahren und Anwendungen. Vieweg+Teubner Verlag; 2002.
