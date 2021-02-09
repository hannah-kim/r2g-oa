## Requirement and Usage 
Needs Python 3. No modules are required.
 
To run the program, please use
 
    python main.py 

To execute sample commands for testing, use  
    
    python main.py --test
    
## Files
* main.py : my implementation of product inventory system
    * Product class for storing item name, item SKU
    * Warehouse class for storing warehouse ID, stock limit, currently stocked items, total stock quantity
    * Inventory class for managing products and warehouses
        * add_product function : add product to catalog
        * add_warehouse function : create warehouse
        * list_products function : print product catalog
        * list_warehouses function : print list of warehouses
        * list_warehouse function : print info on a warehouse
        * stock function : stock item(s) to a warehouse 
        * unstock function : unstock item(s) to a warehouse
        * check_cmd function : helper function to parse command, write command history to a file, execute command
    * tabulate function : print lists of products or warehouses in a table
    * log function : write command history to "log.txt" file
    * main function to get user commands
    * test function : execute sample commands from sample_commands.txt
* sample_commands.txt : list of sample commands for test
* log.txt (output) : command history will be stored here 

## My approach
For each user command, check_cmd() checks if it's in a valid format (e.g., no typos, int/str check).
If valid, the corresponding inventory management function is called.
It checks if the command is valid (e.g., non-existing SKU, negative quantity).
If valid, the corresponding products / warehouses are updated.
Regardless of validity, all entered user commands are dumped in a batch of two.
For every other command, a thread writes the last two commands into log.txt file.   

## Sample results
``` 
> ADD WAREHOUSE 970
> ADD WAREHOUSE 45s 100
ERROR: Enter valid commands
> ADD WAREHOUSE 45
> ADD WAREHOUSE 2
> LIST WAREHOUSES
--------------------------------
WAREHOUSE ID | TOTAL QTY | LIMIT
--------------------------------
970          | 0         | inf  
45           | 0         | inf  
2            | 0         | inf  
--------------------------------
> ADD PRODUCT "Sofia Vegara 5 Piece Living Room Set" 38538505-0767-453f-89af-d11c809ebb3b
> ADD PRODUCT "BED" 5ce956fa-a71e-4bfb-b6ae-5eeaa5eb0a70
> ADD PRODUCT "TRUNK" 5ce956fa-a71e-4bfb-b6ae-5eeaa5eb0a70
ERROR adding product TRUNK 5ce956fa-a71e-4bfb-b6ae-5eeaa5eb0a70 : existing SKU
> STOCK 38538505-0767-453f-89af-d11c809ebb3b 970 1000
> STOCK 38538505-0767-453f-89af-d11c809ebb3b 45 105
> UNSTOCK 38538505-0767-453f-89af-d11c809ebb3b 2 105
ERROR unstocking 38538505-0767-453f-89af-d11c809ebb3b in the warehouse 2 : not in stock
> UNSTOCK 38538505-0767-453f-89af-d11c809ebb3b 45 105
> LIST WAREHOUSE 970
Warehouse # 970 ( 1000 / inf )
----------------------------------------------------------------------------------
ITEM NAME                            | ITEM SKU                             | QTY 
----------------------------------------------------------------------------------
Sofia Vegara 5 Piece Living Room Set | 38538505-0767-453f-89af-d11c809ebb3b | 1000
----------------------------------------------------------------------------------
> LIST WAREHOUSE 45
Warehouse # 45 ( 0 / inf )
> LIST PRODUCTS
---------------------------------------------------------------------------
ITEM NAME                            | ITEM SKU                            
---------------------------------------------------------------------------
Sofia Vegara 5 Piece Living Room Set | 38538505-0767-453f-89af-d11c809ebb3b
BED                                  | 5ce956fa-a71e-4bfb-b6ae-5eeaa5eb0a70
---------------------------------------------------------------------------
```
