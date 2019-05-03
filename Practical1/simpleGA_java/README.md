# EA Course TU Delft 2019 - Practical Assigment 1
## The Simple Genetic Algorithm
This Java code (partly) implements the simple Genetic Algorithm (GA) described in assignment 1.

## Compiling & Running
You can use an IDE to compile and run this code, or do it manually.
Netbeans will automatically recognize the folder as a Java project.

To compile manually, execute `make` from your terminal (works on both Linux and Windows).
To run manually execute `./run.sh` if using Linux, or `run` if using Windows.

## How are the folders organized?
All `.java` source code files are in `src/geneticalgorithm`. All compiled classes will end up in `build/classes/geneticalgorithm`.
When the code is run, a folder `experiments` will be created, where useful information will be logged.

## TODO's
* `Launcher.java` contains the main. You can use the main to script your pipeline of experiments.
* In `FitnessFunction.java`, the current evaluation function is *OneMax*. You must change it as described in the assignment.
* Uniform and one-point crossover must be implemented in `Variation.java`.
