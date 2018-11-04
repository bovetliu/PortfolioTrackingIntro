# Portfolio Tracking, Automated Stock Trading

This project is intended to track stock allocation recorded in a mysql database table every
two minutes. Target users of this software will be office workers having no time to constantly watch 
for change of stock market, and want to avoid sudden stock slump or want to apply results of analysis 
in real-world US stock trading.
 ![Programming_running](resources/pics/Programming_running.png "Programming_running")


## Installation

* [Installation using Amazon Machine Image](./installation_ami.md)  
* [Installation at local](./installation_local.md)

## Setting up
* [Setting up](./setting_up.md)
* [Schedule instance starting and shutting down](./schedule_instance_starting_and_shutting_down.md)

## Usage
1. Write your stock allocation data to a Mysql data table, like following
   ![001_insert_portfolio_data](resources/pics/001_insert_portfolio_data.png "001_insert_portfolio_data")
2. Make sure Portfolio Tracker is running, TWS or IBGateway is on,
3. Go to `/mainPanel`, and select `PortfolioTrackAdvisor`, then click "Prepare"
4. In the pop-up modal, input portfolio name, and desired cash to be allocated at "startingCash"  
    ![004_pop_up_form_pta](resources/pics/004-pop-up-form-pta.png "004_pop_up_form_pta")
5. Click button "create", then click start
6. If market is closed at the time of creating this PortfolioTrackAdvisor, we can see limit orders
   submitted. Position of each symbol is calculated based allocation percentage and recent quote 
   price of each symbol. If market is open at the time, we shall see orders get submitted and executed.
    ![006_pta_run_at_mkt_close](resources/pics/006-pta-run-at-mkt-close.png "006_pta_run_at_mkt_close")
7. Then Portfolio Tracker is going to track change of allocations of this portfolio using newest 
   `record_date`. This means one can choose to write allocations to database each day, or write whole
   portfolio allocations to database only when a change has been made to portfolio allocation.

## Question

1. Will my stock selection be stolen by using this software?  
   Answer: no, there is no back-door code reporting stock selection, that is your intellectual 
   property. You can choose to run the EC2 in a VPC, which blocks any unwanted network traffic.

2. What is estimated AWS expense of running this software?
   Answer: ~13 USD per month. EC2 will only be running when marget is open. 

## Contributing
1. still thinking, want to keep this project simple, execution level only, and only for 
   amateurs 

## Tests

## History

Started at Jun. 1st. 2017

## Credits

## License
