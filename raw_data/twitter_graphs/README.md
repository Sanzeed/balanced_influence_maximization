# Twitter Graphs
This folder contains the anonymized versions of the Twitter graphs used in the experiments reported in Section 4.3 of the paper. 

We used the Twitter REST API to collect the (ego) networks of four accounts: `@bofa_careers`, `@upsjobs`, `@verizoncareers`, and `@hersheycareers`. We fetched the followers of each account and the followers of the followers to construct the network of connections among the followers of each account. We also fetched the followers’ names and used `genderize.io` to determine their gender (`m` => male / `f`=> female).

The JSON files have the following format:
```
{
  "labels": {
    "node_id": "label",
    ...
  },
  "edges": {
      ["src_node_id", "trg_node_id"], 
      ...
    }
}
```
