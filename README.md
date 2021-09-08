## GA ANALYTICS

This is a REST API. It's built using Flask and Flask Restful Frameworks

## To run the web server

Ensure that you create an env file and add all env-sample variables with the Correct substitutions.

Then run this command:

```
python3 app.py
```

## To run the tests

Ensure add all the variables in env-sample with their correct substitutions to your terminal session using the export command e.g export VAR1='name'.

Then run this command:

```
python3 -m unittest
```

## API Endpoints

```python
Part 1, Q1 - http://localhost:5000/api/v1/total-sessions

Part 1, Q2 - http://localhost:5000/api/v1/sessions-per-user?limit={limit e.g 10}&offset={offset e.g 0}

Part 1 Q3 - http://localhost:5000/api/v1/time-to-order-confirmation

Part 1, Q4(a) -  http://localhost:5000/api/v1/get-coordinates-change?limit={limit e.g 10}&offset={offset e.g 0}

Part 1, Q4(b) - http://localhost:5000/api/v1/orders-placed-with-coordinates-change?limit={limit e.g 10}&offset={offset e.g 0}

Part 2, Q1 - http://localhost:5000/api/v1/get-order-details-per-full-visitor-id?fullVisitorId=14318742381277170233


```
