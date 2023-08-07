# postgres-autobkp
Auto Backup for Local Development using python and bash

## How to use
1. Clone this repository
2. Create a folder named `backup` in the root of this repository
``` bash
mkdir backup
```
3. Create a file named `.env` in the root of this repository
``` bash
cp .env .env.example
```
4. Edit the `.env` file with your database credentials with your favorite text editor.
5. Run the script
``` bash
python3 main.py
```
6. You can add this script to your crontab to run it automatically
``` bash
crontab -e
```
7. Add this line to the end of the file
``` bash
0 0 * * * cd /path/to/this/repository && python3 main.py
```
8. Save and exit
9. Enjoy!

