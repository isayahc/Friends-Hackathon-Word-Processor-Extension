# Friends-Hackathon-Word-Processor-Extension

System for generating sources for information in text processors  

## Features
This extension searches the internet to determine if a source is true or false. If true then a citation will be written for the user

### Running The application

after setting up the initial environment run:

 ```python agent_app.py```

To get start

#### Querying the agent

To query the agent here is a sample query

```
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"query_string": "Magnus Carlsen won the 2018 FIDE World Chess Championship[cit]"}' \
  127.0.0.1/query
```

#### Query Response

#### Query
##### Return
- 

