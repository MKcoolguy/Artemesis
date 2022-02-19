<h1 align-"center">S.A.U.C.E. 2.0.</h1>
<p>
</p>

  S.A.U.C.E. or Structural Analysis Using Contactless Evaluation is a small contactless device that is designed to assess, analyze, and monitor the structural integrity of manufactured structures by utilizing object detection technology, thermal imaging, range finding, and vibrational monitors. The information gathered is collected and stored for further analysis. Version 2.0 is a continuation of our original project with a newfound focus on portability and compatibility with robotic systems that would allow us to expand on the existing features by allowing use in locations that would otherwise be inaccessible.
  
  Designed as an entry into the NASA Minds project.

## Dashboard

  The Dashboard sub folder contains the python code for displaying metrics and a general control panel for our device.

#### Requires
Dash, Dash HTML Components, Dash Core Components, Dash Bootstrap Components, Plotly, and Pandas. Install using your package manager of choice.

Anaconda:
```
conda install -c conda-forge dash
conda install -c conda-forge dash-core-components
conda install -c conda-forge dash-html-components
conda install -c conda-forge dash-bootstrap-components
conda install -c conda-forge plotly
conda install -c conda-forge pandas
```
Pip:
```
pip install dash
pip install dash-core-components
pip install dash-html-components
pip install dash-bootstrap-components
pip install plotly
pip install pandas
```

#### To Run
  index.py is the primary dashboard server, ensure you run that either locally in your terminal or with something like pm2.

## Helpers

  The helpers subdirectory is a set of scripts necessary for major parts of our project to function, such as live video streaming from the S.A.U.C.E. module itself.

#### Requires
Just PiCamera

Install it through the terminal, below example is for debian-based distros.
```
apt-get install python3-picamera
```

#### To Run
  Call the scripts directly (python3 scriptname.py). These will be rolled into the dashboard as time goes forward.

## Authors
Dr. Tae Lee (tslee@ggc.edu), Dr. Sairam Tangirala (stangira@ggc.edu)

Byron Fisher (bfisher1@ggc.edu), Khamilah Nixon (knixon4@ggc.edu), Kristoffer Hendricks (khendricks@ggc.edu), Matteo Kitic (mitic@ggc.edu), Samuel Mckinney (smckinney1@ggc.edu), Valerie Morse (vmorse@ggc.edu)
