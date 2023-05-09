# fnsi-check
This is a small python code that queries PMA for target seed count info.

You can either feed a list of ortho's (via csv) or a single ortho as a variable into the PMA. The requests library will then iterate through all plots and produce FNSI data.

The current version does not include any error tracking - I have noticed that occasionally in the late afternoon, some API calls will fail with a 500 code. There doesn't seem to be any logic behind it - but future work should ignore/retry.

Single_ortho_full.py returns all plots for a single ortho.

List_orthos_noofset.py returns 100 plots for a list of ortho's (provided in csv)

list_orthos.py returns all plots for a list of ortho's (provided in csv) - This will take a long time.
