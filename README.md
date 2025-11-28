# Macbook Init
A companion to dotfiles for bootstrapping a new Mac:

```bash
 - Installs packages
 - Downloads DMGs
 - Runs configuration scripts 
 ```

## Adding new bash script
There is two step process to add a new bash script for installing tools or configurations:

1. Create a shell script with this format `<order_number>_name.sh` inside the scripts folder
1. Add the new shell script to the json config at the root `tasks.json`

After these two steps the script will be available for install
