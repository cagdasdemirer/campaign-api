# Deployment
- [Render](https://campaign-api-durg.onrender.com/)

# End-to-End Test Collection
```sh
tests/tets_main.http
```

# Assignment Report

## Questionnaire:
### 1. Where did you find it most difficult and why?
The hardest part was dealing with the database schemas because they were incomplete. I had to make a lot of assumptions about missing rows, which added complexity to the logic. On top of that, there were some unclear points in the response schema, so I had to guess how to structure certain parts.

That said, setting up the async architecture wasn’t too challenging. The endpoints were described well, and their expected behavior was clear, which made that part straightforward.

### 2. Which parts of this code might take the longest and consume the most memory?
The biggest issue here is generating the campaign score summary for every GET request. As the dataset grows, this process will start taking longer and eating up more memory.

It’s because the system doesn’t have any caching or pre-computation for this data. So every time a request comes in, the app has to pull all the data and calculate everything on the fly. If the database queries aren’t optimized with proper indexing, that’ll make it even worse.

### 3. What could be the security vulnerabilities of this system?
There are a few risks here:

- The .env file is exposed, which shouldn’t happen even if it’s for demonstration purposes.
- Debug mode is active, and that’s a big red flag in production. It can expose sensitive information if something goes wrong.
- CORS isn’t configured properly, so it’s open to cross-origin attacks.
- There’s no authentication, not even something basic like JWT.
- HTTPS protocol missing.

Plus, I deployed this on a free-tier machine, so I don’t have full control over open ports, which is another potential security risk.

### 4. How would you design this system on the AWS platform?
If I had to move this to AWS, I’d probably go serverless with Lambda for the FastAPI service. Since there’s just one analysis endpoint, Lambda makes sense for simplicity and cost efficiency.
For the database, I’d use RDS PostgreSQL. It’s not as fast as BigQuery for analytical workloads, but it would handle this use case fine, especially with a better-designed schema.
I’d also add caching with ElastiCache (probably Redis) to store frequently accessed data, like campaign summaries. File storage would go to S3—it’s secure and integrates easily with other AWS services.
For authentication, Cognito would be my choice. It simplifies user management and adds proper security layers.
On the monitoring side, I’d hook up CloudWatch and maybe use X-Ray for distributed tracing. Finally, I’d use API Gateway for routing and add a load balancer in case the traffic grows.

### 5. What could you have done better in a longer time?
If I had more time, I’d definitely focus on testing first. A proper test suite, with unit and integration tests, would make the app more reliable and easier to debug.
I’d also add pagination for the campaign score summaries to handle larger datasets better. Right now, it’s pulling everything in one go, which isn’t scalable.
Authentication and authorization need to be implemented too—both to secure the endpoints and to manage user roles. 
As I mentioned above I would like to implement a cache system for campaign summaries.
Custom exception handling is another area I’d improve. It’d make the error responses clearer and help with debugging.
Lastly, I’d spend more time on the database queries. I’d optimize them with better indexes and maybe rework the schema to improve performance. 
On top of all that, I was also considering containerizing the app with Docker. It’d make deployment more consistent across environments and simplify scaling in the future. With Docker, I could bundle the app with its dependencies, making the setup more portable and less prone to “it works on my machine” issues.
