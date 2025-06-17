# knapsack
Welcome to the knapsack challenge!
This is a fun challenge where you can submit your own solution to this version of the knapsack problem.
<!-- leaderboard:start -->
## Leaderboard
| Name       | Weight | Volume | Value |
|------------|--------|--------|-------|
| jaume_2.csv | 9.98 | 24.29 | 2696.14 |
| pablo_gomis_better_ordering.csv | 9.98 | 24.29 | 2696.14 |
| qrg.csv | 9.98 | 24.29 | 2696.14 |
| jaume_1.csv | 9.98 | 24.29 | 2696.14 |
| pablo_gomis_sack1.csv | 9.98 | 24.29 | 2696.14 |
| jacopo_sack.csv | 10.00 | 24.52 | 2693.39 |
| pyari_sack.csv | 8.46 | 24.74 | 2170.03 |
| tobi_sh_001.csv | 9.93 | 24.48 | 2132.82 |
| my_sack_2.csv | 7.69 | 7.36 | 485.24 |
| my_sack_3.csv | 2.40 | 4.25 | 348.25 |
| my_sack_1.csv | 3.30 | 4.69 | 312.62 |
<!-- leaderboard:end -->
## The challenge
Take a look to the [items](data/knapsack_items.csv) file to see the items you can choose from.

You can select as many items as you want, but you have to respect the following constraints:
- The total weight of the items in your sack must not exceed 10 kg.
- The total volume of the items in your sack must not exceed 25 L.
- You can only use each item once.

The winner will be the sack with the highest value, which is calculated as the sum of the values of the items in the sack.

Note: Take into account that all the items interact with other items, modifying the value of that item if the combo item is present in the sack. 
Take into consideration that there are positive and negative combos!
## How to contribute
1. Create a file under [sacks](sacks/) directory with the name of your sack like `my_super_awesome_sack.csv`. This will be your submission name.
2. Add on that file the items you want to try to pack in your sack. The file should be a CSV with an id of each item you want to submit, having 1 id per line like:
   ```csv
    1,
    2,
    3,
    ```
3. Submit a PR with your sack file. This will verify your items follow the constrains of max weight and max volume.
4. Once your PR is merged, you will be able to see your sack on the leaderboard.