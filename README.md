# Assignment Report

## Questionnaire:
1. Where did you find it most difficult and why?
Database schemas were also far from normalization and there were unclear points in Response.json. There were also missing dates in daily_scores. It took me time to clarify these.
2. Which parts of this code might take the longest and consume the most
memory?
Producing a summary of all campaign scores for each get request will tire the system as the data population increases.
3. What could be the security vulnerabilities of this system?
I uploaded the .env file to the test repo and left the debug options open, unlike production. Also, at least a JWT authentication could have been added. Also, since the machine I deployed app is free tier, I do not have full control over open ports.
4. How would you design this system on the AWS platform?
I would move the database to AWS PostgreSQL, with better schema. It would not provide as good OLAP performance as BigQuerry, but it would do the job. Since the service consists of a single analysis endpoint, I would move it to Serverless Lambda. I would also connect the monitor part to AWS API Gateway.
6. What could you have done better in a longer time?
Unit testing would be required. I would like to add pagination, authentication vs authorization. I would also like to implement a custom exception handler.
 
