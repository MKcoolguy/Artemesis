<h1 align-"center">S.A.U.C.E. 2.0.</h1>
<p>
</p>

  S.A.U.C.E. or Structural Analysis Using Contactless Evaluation is a small contactless device that is designed to assess, analyze, and monitor the structural integrity of manufactured structures by utilizing object detection technology, thermal imaging, range finding, and vibrational monitors. The information gathered is collected and stored for further analysis. Version 2.0 is a continuation of our original project with a newfound focus on portability and compatibility with robotic systems that would allow us to expand on the existing features by allowing use in locations that would otherwise be inaccessible.
  
  Designed as an entry into the NASA Minds project.

## Dashboard

  The Dashboard sub folder contains the python code for displaying metrics and a general control panel for our device. For any future plans, I would reccomend that people continuing on the project clean up directory structure and dependecies.

#### Requirements, Installation, and Execution

This was built using a Raspberry Pi 3 Model B+ with a DHT11 temperature sensor, an HC-SR04 distance sensor, and both a standard RPi Camera and a FLIR camera.

Your development system and the Pi will require Python3 which can be found [here](https://www.python.org/downloads/).

Due to many students seeking to continue this project and/or fork this project and running into dependency issues/not using venvs, this project has been migrated to [Poetry](https://python-poetry.org/). You should install that using the instructions found [here](https://python-poetry.org/docs/).

After installing Poetry, simply clone the repo, navigate into Artemis/Dashboard/ and execute "poetry run python index.py" which will run a testing version of a flask website with the dashboard on it.

## Authors
Dr. Tae Lee (tslee@ggc.edu), Dr. Sairam Tangirala (stangira@ggc.edu)

Byron Fisher (bfisher1@ggc.edu), Khamilah Nixon (knixon4@ggc.edu), Matteo Kitic (mkitic@ggc.edu), Samuel Mckinney (smckinney1@ggc.edu), Valerie Morse (vmorse@ggc.edu)