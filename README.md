# HK returns
Script automating returns assignment in ERP 

## Usage 
Module provides main function with the following arguments:

Argument | Description
-- | - 
sales_input_path | path to sales database
returns_input_path | path to file with returns to be made
client | customer number
is_client_soldToCur | type of customer number (sold to or sold to cur)
return_output | path to file with parsed sales with added returns
parsed_output | path to file with parsed returns

## Input files
### Sales database columns
- `Billing doc`
- `SoldToCur`
- `Sold-to party`
- `Product`
- `qt`
- `alreadyReturned`
### Returns file columns
- `material`
- `material2` (if customer provides more than one material code in one line of return)
- `material3` (if customer provides more than one material code in one line of return)
- `qt`


