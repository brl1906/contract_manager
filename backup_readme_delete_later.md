# Project Title

This program gets, parses and evaluates a structured contract management file to provide both email notification and KPI charts for an Invoice/ Accounts Payable employee, providing insight on: 1) performance against spending limits, 2) contract burn rate status, 3) renewal and expiration option status.

It helps ensure that there are no gaps in service or contract lapses due to either contract expiration or exceeding approved public spending limits which is critical for agencies that rely on a combination of vendors to provide services to local residents and other support agencies. It automates parts of the work flow for government workers and significantly reduces the level of effort associated with contract management where agency ownership of contracts is unclear or not 1 to 1.

## Demo


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.


## Built With

* [Python 3.6] - Language used
* [datetime](https://docs.python.org/3/library/datetime.html),
[configparser](https://docs.python.org/3/library/configparser.html),[smtplib](https://docs.python.org/3/library/smtplib.html), - Libraries used
* [Numpy](https://docs.scipy.org/doc/numpy/reference/index.html), [Pandas](https://pandas.pydata.org/) - Frameworks used



### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Bug / Feature Request

If you find a bug please open an issue [here](https://github.com/brl1906/ContractManager_DGS/issues) providing as much documentation as possible on the program's behavior on your machine.

If you want to request a new function, please hit us up by describing your request in detail [here](https://github.com/brl1906/ContractManager_DGS/issues).

## Contributing

Want to contribute to this project's development?  besos!!:kissing_closed_eyes:

Here are 7  simple steps you can do while listening to Miles Davis's [Seven Steps to Heaven](https://www.youtube.com/watch?v=Hhfe1SUe2-A):
* Fork the repo & read our [Process For Submitting Pull Requests](https://gist.github.com/PurpleBooth/b24679402957c63ec426) to us
  * Create a new branch (```git checkout -b improve-feature```)
    * Make desired changes to files
    * Add changes to reflect changes you made
      * Commit your changes (```git commit -m 'Improve feature'```)
  * Push to the branch (```git push origin improve-feature```)
* Create your [pull request](https://github.com/brl1906/ContractManager_DGS/pulls)

## To-do

* - [x] separate function run, charts and notification by agency division
* - [ ] add error handler for bad email addresses
* - [ ] convert print to logs
* - [ ] change default test email recipient to target AP personnel
* - [ ] chart conversion Matplotlib --> Plotly
* - [ ] expose email recipient targets as dynamic CLI run arguments

## Authors

[**Babila Lima**](https://generalservices.baltimorecity.gov/business-process-improvement-office)


## License

This project is licensed under the MIT License - if interested, you can check out the [LICENSE file](https://github.com/brl1906/ContractManager_DGS/blob/master/LICENSE) in the repo.

## Acknowledgments

Shout out to *Troy Parrish* for raising the issue and opportunity and spending her valuable work hours to help diagnose and diagram her work and her needs.

Hand claps to [*Billie Thompson*](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2#file-readme-template-md) in London and [*Harsh Vijay*](https://github.com/iharsh234/WebApp) in India for providing inspiration through clear documentation and engaging readme examples.

* Hat tip to anyone who's code was used
* Inspiration
* etc
