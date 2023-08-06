# BA-LORRE

A Python implementation of the **B**ees **A**lgorithm based **L**ocal **O**ptima **R**egion **R**adius **E**xtimator. 
Most of the intelligenent numerical optimization algorithms available are only made to find the global optimum of a given function. 
In contrast, the BA-LORRE is a swarm computation algorithm designed to find *several* local optima, avoiding already explored regions during the search.

The algorithm exploits the [search properties](https://www.sciencedirect.com/science/article/abs/pii/S2210650220303990?via%3Dihub) of the [Bees Algorithm](https://gitlab.com/bees-algorithm/bees_algorithm_python) to identify the position and radius of local optima region in a non-parametric way. Once identified, the local score of those regions is lowered, allowing the algorithm to focus furture search to unexplored regions.

| | |
|:-------------------------:|:-------------------------:|
|<img src="pics/iterations_0.png">  |  <img src="pics/iterations_1.png"> |
|<img src="pics/iterations_2.png">  |  <img src="pics/iterations_3.png"> |

This library allows an off-the-shelf use of the algorithm to find the best local optima of an user-defined target function.

![solutions](pics/lorre_solutions.png)

## Reference
For details on the inner working of the BA-LORRE algorithm, how it's related on the Bess Algorithm and how the optima regions are found, please refer to [this work](https://etheses.bham.ac.uk/id/eprint/10094/7/Baronti2020PhD.pdf).  

If you are using this implementation of the BA-LORRE for your research, feel free to cite this work in your paper using the following BibTex entry:
```bibtex
@article{baronti2020analysis,
  title={An Analysis of the Search Mechanisms of the Bees Algorithm},
  author={Baronti, Luca and Castellani, Marco and Pham, Duc Truong},
  journal={Swarm and Evolutionary Computation},
  volume={59},
  pages={100746},
  year={2020},
  publisher={Elsevier},
  doi={10.1016/j.swevo.2020.100746},
  url={https://doi.org/10.1016/j.swevo.2020.100746}
}
```

# Installation

This module is available on [pip](https://pypi.org/project/ba-lorre) and can be installed as follows:
```sh
$ pip3 install ba_lorre
```
# Usage and Guidelines
As an extension of the original Bees Algorithm, the BA-LORRE shares most of the interface and mirrors its general usage. 

The main class, `LORRE`, has the following signature (mandatory parameters in **bold**):
- **score_function**`: Callable[[list], float]` the function that need to be optimised. It can either be a (lambda) function or a class that overrides the `__call__` function. Either way, `score_function(solution: list) -> float` needs to take a single parameter, a list of *N* `float` representing a position in the search space, and returns the score relative to that position; 
- **range_min**`: list` list of *N* `float`, indicating the lower bound of the search space; 
- **range_max**`: list` list of *N* `float`, indicating the upper bound of the search space; 
- *nb*`: int` number of *sites*;
- *nrb*`: int` number of solutions sampled around each site, per iteration;
- *stlim*`: int` stagnation limit, the number of iteration required to abandon a site if no local progress is made;
- *initial_ngh*`: list` the neighbourhood used for the local search in a site;
- *shrink_factor*`: float` how much a neighbourhood must be shrunk per every iteration that its centre is not updated; 
- *derating_radius_selection_criterion*`: str` the criterion used to identify the optima region radius. Allowed values are *median* and *topological*;
- *derating_type*`: str` the shape of penalty that will apply on every found region. Allowed values are *flat* and *linear*;

In this context *N* is the number of dimensions of the score function to be optimized. At each iteration *nb* x *nrb* solutions are evaluated in the search space.
Examples of scores functions that can be used as a benchmark can be found in [this library](https://gitlab.com/luca.baronti/python_benchmark_functions).

Please note that for simplicity this algorithm solves a *maximization* problem. 
If you need to minimize a function, please provide the *opposite* of the function (i.e. *g(x)=-f(x)*) to the algorithm.
The found solutions won't be affected.

Please refer to the Bees Algorithm [documentation](https://gitlab.com/bees-algorithm/bees_algorithm_python/-/blob/master/README.md) for further details.
## Initialization
The algorithm is first instantiated (as an example, here we are using a simple hyperbolic function to be optimized)
```python
from ba_lorre import LORRE

alg = LORRE(lambda x: -pow(x[0]*x[1],2),
            range_min=[-100, -100],
            range_max=[100, 100],
            nb=5, nrb=20, stlim=20,
            derating_radius_selection_criterion='median',
            derating_type='linear')
```
## Optimization
Then the optimisation itself can be performed in different ways. The most simple method is calling `performFullOptimisation` specifying either the maximum number of iterations or the maximum score wanted as stopping criterion.
```python
>>> alg.performFullOptimisation(max_iteration=50)
(50, -3.4228945713694973e-11)
```
This returns the number of iterations required and the score of the best solution found. 

Alternatively, more control on the optimization process can achieved performing one iteration at a time this way:
```python
alg.performSingleStep()
```
For score functions with 2 dimensions is possible to visualize the iterations of the algorithm calling
```python
alg.visualize_iteration_steps()
```
This is often used for demonstration, debugging and to get a better insight on the algorithm dynamics. 
All the figures in this readme have been taken this way.

## Found Optima Handling
The aim of the algorithm is to return the best local optima of a function. 
Once the optimization process is terminated the found optima can be collected with
```python
alg.getFoundOptima()
```
which will return the position of the found optima.

For score functions with 2 dimensions is possible to visualize the found optima directly on the function's surface with:
```python
alg.showFoundOptima()
```
![solutions](pics/lorre_solutions.png)
Either way, a list of *pruning* criteria can be passed to filter the found optima.

### Pruning Criteria
The algorithm has no prior information on how many local optima the score function is supposed to have.
As a result, spurious and redundant optima can be returned. 

For this reason, this library comes with a set of pruning functions that can be passed to `getFoundOptima` or `showFoundOptima` to eliminate solutions that are unlikely to be a good approximation of real optima.
Available pruning classes are:
- **PruningProximity** putative optima that have been generated at the same time in the same region of an optimum of higher score are removed;
- **PruningAbsScoreCutoff** putative optima with a score lower than the *cutoff* parameter, are removed;
- **PruningPercScoreCutoff** putative optima with a score lower than *cutoff*% of the other optima are removed;

Any number of pruning criteria can be combined:
```python
from ba_lorre import PruningProximity, PruningPercScoreCutoff

alg.getFoundOptima(pruning_functions=[PruningProximity(), PruningPercScoreCutoff(cutoff=.5)])
```
The `PruningAbsScoreCutoff` and `PruningPercScoreCutoff` pruning criteria require insight on the optima distribution to be used properly. 
To help the practitioner a convenience function to visualize the optima score distribution is provided:
```python
alg.showOptimaScoreHistogram()
```
![solutions](pics/sol_distr.png)

