# Balanced Influence Maximization in the Presence of Homophily
Md Sanzeed Anwar,
[Martin Saveski](http://martinsaveski.com),
and Deb Roy

This repository contains code and data that can be used to replicate the analysis in the paper, "[Balanced Influence Maximization in the Presence of Homophily](https://doi.org/10.1145/3437963.3441787)" published in WSDM'21.


## Guide to Files
`models`: contains the source code for network generation and seeding
- `models/net_gen`: contains the network generator models
    - `models/net_gen/homophilic_net_gen.py` implements the homophilic network generation model (Sec. 3.2)
    - `models/net_gen/simple_net_gen.py` implements the non-homophilic network generation model (Sec. 3.1)
- `models/seeding`: contains the seeding models
    - `models/seeding/vanilla_greedy.py` implements the model for the vanilla greedy influence maximization algorithm
    - `models/seeding/balanced_greedy.py` implements the model for the balanced influence maximization algorithm proposed in the paper (Sec. 4.1)
    - `models/seeding/degree_threshold.py` implements the model for the baseline algorithm by Stoica et al. (Sec. 4.3: Baseline)
    
`raw_data/twitter`: contains the four real-world networks used in the performance analysis of our proposed algorithm

`experiments`: contains scripts for all figures in the paper. `experiments/fig_x` corresponds to figure x in the paper, where x = 1,2,...,7
- `experiments/fig_x/run_figx.py` runs the experiment corresponding to figure x
- `experiments/fig_x/get_csv.py` generates a .csv file from the raw result data
- The scripts in `experiments/fig_6` process the output our algorithm, while the scripts in `experiments/fig_7` process the output of the baseline algorithm

`plots`: contains both the .csv files containing the experiment results demonstrated in our paper, as well as the plotting code needed to generate the figures in our paper.

To generate the each plot, run `experiments/fig_x/run_figx.py` which outputs the results in a .json file, then run `experiments/fig_x/get_csv.py` to convert them in the appropriate .csv format, and finally copy .csv file to `plots/_csvs` and run the corresponding script in `plots`. 


## Cite as
```
@inproceedings{anwar2021balanced,
    title={Balanced Influence Maximization in the Presence of Homophily},
    author={Anwar, Md Sanzeed and Saveski, Martin and Roy, Deb},
    year={2021}
    publisher = {Association for Computing Machinery},
    booktitle={Proceedings of the 14th ACM International Conference on Web Search and Data Mining},
    series = {WSDM '21}
}
```


## License
This analysis code is licensed under the MIT license found in the LICENSE file.

