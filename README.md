# contract_manager
Project for automation of local government contract management, analysis, notification tasks.

This program gets, parses and evaluates contract management data to provide email notification, KPI charts, automatically generates change order memos for contracts meeting key criteria, handling key manual administrative tasks for  Invoice/ Accounts Payable employees.  It provides insight on: 1) performance against spending limits, 2) contract burn rate status, 3) renewal and expiration option status, 4) contracts in danger of service gaps.

It helps ensure that there are no gaps in service or contract lapses due to either contract expiration or exceeding approved public spending limits which is critical for agencies that rely on a combination of vendors to provide services to local residents and other support agencies. It automates parts of the work flow for government workers and reduces the level of effort associated with contract management where agency ownership of contracts is unclear or not 1 to 1.

## Problem Statement
Agency accounts payable staff play a significant administrative support role in ensuring that operational divisions can provide necessary services to agencies and residents without interruption and adequately balance resources. Effective contract management is important for various reasons including but not limited to:
* ensuring continuity of service for divisions dependent upon outside contractors to support  critical services
* increasing the pool of vendors willing and attracted to compete on municipal contracts by removing barriers to payment
* supporting efforts to engage small & local contractors who traditionally cannot afford long periods of delayed payment
* reducing the need for time intensive change orders

**Fact**: Current performance of this task is uncessarily manual and cumbersome for the 21st century.

Due to the nature of this responsibility, it is not currently performed with an optimal standard frequency--how is that for bureaucracy-speak.  

## Getting Started
```
go get the repo, clone it & use it
```

### Installing
The requirements.txt file contains all of the dependencies necessary to run this program from your machine. Creating a virtual environment and running, in your terminal, the command:
'''pip install -r requirements'''

This assumes that you have created a project folder, changed into that directory, have created a virtual environment there, activated the virtual environment for your project, and are running the above command in that location.
* for example:
  * $ mkdir yourprojectfoldername
  * $ virtualenv yourvenvname
  * $ source yourvenvname/bin/activate
  * $ pip install -r requirements

## Contributing
Want to contribute to this project's development???        Besos!!:kissing_closed_eyes:

* Fork the repo
  * Create a new branch (```git checkout -b improve-feature```)
    * Make desired changes to files  
    * Add changes to reflect changes you made
      * Commit your changes (```git commit -m 'Improve feature'```)
  * Push to the branch (```git push origin improve-feature```)
* Create your pull request

## TODO:
* - [x] create initial project readme with problem statement
* - [x] add change order memo creation feature
* - [x] separate function run, charts and notification by agency division
* - [X] add sample data for format example
* - [ ] chart conversion Matplotlib --> Plotly
* - [ ] expose email recipient targets as dynamic CLI run arguments

## Authors
[Business Process Improvement Office](https://generalservices.baltimorecity.gov/business-process-improvement-office)

## Acknowledgements
Nothing happens in a vacum--except carpet cleaning, and even that is debatable. A special thank you goes to the folks that were banging their heads on this problem and lifted them long enough to ask the magic question, is there a way to automate the boring stuff.  

Special shoutouts to Troy King and Berke Attila for spending the hours to walk through this problem untill it was clear and then telling us to do something about it.
