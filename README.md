Evolution of Flight - http://www.designingemergence.com/portfolio/evolution-of-flight/


Evolution is the most successful creative process in the world. Over the millennia, it has been responsible for designs that we wouldn’t have come up with in our wildest dreams. With Evolution of Flight, I wanted to test whether I could use human intuition to speed up the evolutionary process and use it to design airplanes. 

Requirements:

  - Rhinoceros 3D
  - Rhinopython
  - Lasercutter or other means of testing designs
  - Test rig
  
Files:

  - Evolution of Flight.3dm: Rhino file containing 2 generations of evolved planes.
  - createPlane.py: Rhinopython script to create a single airplane
  - evolvePlanes.py: Full script to create and evolve all planes
  - generation0.p: File containing genetic info for initial generation
  - generation1.p: File containing genetic info for first generation
  
Method:

  - Ensure that Rhino is installed
  - Open Rhino
  - Using the 'RunPythonScript' command, run the evolveplanes.py script
  - When prompted for generation, enter '0'
  - The script will generate 100 random planes.
  - Select 10 planes, lasercut and 10 test them, noting down the distance flown
  - Rerun the script, and enter generation '1'
  - Enter the ID for the first plane chosen followed by the distance it flew
  - Repeat for the remaining 9 planes
  - The script will crossbreed the planes based on their success 
  - 100 new planes will be generated on a separate layer
  - Choose 10 more planes from generation 1 to test and repeat the process
  - As you continue to evolve planes, you will see that they fly further and further.
