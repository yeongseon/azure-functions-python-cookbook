# Recipes

Recipes are curated implementation patterns for common Azure Functions scenarios. They provide a structured approach to building, deploying, and maintaining serverless applications using the Azure Functions Python v2 programming model. Each recipe addresses a specific workload or integration pattern, offering a production-ready starting point that incorporates best practices for performance, security, and scalability.

## Recipe Catalog

The following table summarizes the recipes available in this cookbook. Each recipe is designed to be self-contained and easily adaptable to your specific project requirements.

| Recipe | Trigger | Use Case |
|--------|---------|----------|
| HTTP API Basic | HTTP | REST endpoints, CRUD operations |
| HTTP API with OpenAPI | HTTP | API with auto-generated documentation |
| GitHub Webhook Receiver | HTTP | Event-driven webhook processing |
| Queue Worker | Queue | Background job processing |
| Timer Scheduled Job | Timer | Periodic task execution |

### HTTP API Basic

This recipe demonstrates how to build a standard RESTful API using HTTP triggers. It covers handling different HTTP methods, parsing request bodies, and returning appropriate JSON responses with correct status codes.

When to use:
- Building simple microservices that expose REST endpoints.
- Implementing CRUD operations for a data store or backend service.
- Creating lightweight web APIs for mobile or web applications.

Key concepts:
- Mapping HTTP routes to specific Python functions.
- Extracting parameters from query strings and request bodies.
- Using the standard Azure Functions HttpRequest and HttpResponse objects.

Reference the full recipe file: [recipes/http_api_basic.md](../recipes/http_api_basic.md)

### HTTP API with OpenAPI

This recipe extends the basic HTTP API by integrating OpenAPI (Swagger) documentation. It shows how to use decorators or configuration to automatically generate an interactive API console and specification file.

When to use:
- Building APIs that will be consumed by external developers or teams.
- Requiring a standardized way to document and test API endpoints.
- Integrating with API management tools that rely on OpenAPI specifications.

Key concepts:
- Defining request and response schemas for API documentation.
- Using OpenAPI decorators to describe endpoint functionality and parameters.
- Serving the Swagger UI directly from the Azure Function app.

Reference the full recipe file: [recipes/http_api_openapi.md](../recipes/http_api_openapi.md)

### GitHub Webhook Receiver

This recipe focuses on processing incoming webhooks from GitHub. It includes validation logic to ensure that requests are authentic and demonstrates how to handle various event types asynchronously.

When to use:
- Automating workflows in response to GitHub events like pull requests or pushes.
- Building custom integrations with GitHub Actions or other CI/CD tools.
- Real-time monitoring of repository activity or issue management.

Key concepts:
- Verifying GitHub webhook signatures for security and authenticity.
- Parsing complex JSON payloads from diverse GitHub event types.
- Implementing logic to branch based on specific event actions.

Reference the full recipe file: [recipes/github_webhook.md](../recipes/github_webhook.md)

### Queue Worker

This recipe illustrates the producer-consumer pattern using Azure Storage Queues. It shows how to trigger a function whenever a new message is added to a queue, allowing for decoupled background processing.

When to use:
- Handling long-running tasks that shouldn't block an HTTP request.
- Offloading heavy processing workloads to background workers.
- Implementing reliable message-based communication between different services.

Key concepts:
- Configuring queue triggers to process messages as they arrive.
- Managing visibility timeouts and handling message retries.
- Scaling the number of worker instances based on the queue depth.

Reference the full recipe file: [recipes/queue_worker.md](../recipes/queue_worker.md)

### Timer Scheduled Job

This recipe shows how to run Python code on a fixed schedule using cron expressions. It is ideal for periodic maintenance tasks, report generation, or data synchronization routines.

When to use:
- Performing nightly data backups or cleanup operations.
- Generating and sending periodic reports or notifications.
- Syncing data between external systems at regular intervals.

Key concepts:
- Defining execution schedules using standard NCrontab expressions.
- Ensuring singleton execution of scheduled tasks across multiple instances.
- Monitoring execution history and handling missed occurrences.

Reference the full recipe file: [recipes/timer_trigger.md](../recipes/timer_trigger.md)

## Recipe Contract

Every recipe in this cookbook follows a standard structure to ensure consistency and ease of use. This contract guarantees that you will find all the necessary information to understand and implement the pattern effectively.

- **Overview**: A concise, one-paragraph problem statement that describes the challenge the recipe aims to solve and the high-level approach taken.
- **When to Use**: A detailed set of scenarios where this specific pattern applies, helping you decide if the recipe is right for your current project.
- **Architecture**: A clear explanation of the main flow and moving parts, often including a description of how data moves through the system.
- **Project Structure**: A visual and textual layout of the file structure, showing where configuration, code, and tests should reside.
- **Run Locally**: Step-by-step commands and instructions for testing the recipe on your local machine using the Azure Functions Core Tools.
- **Production Considerations**: Critical guidance on scaling, retries, idempotency, and observability to ensure the solution is robust and production-ready.
- **Scaffold Starter**: Detailed instructions on how to generate the initial project structure using the `azure-functions-scaffold` tool, saving you time on boilerplate setup.

## Writing a New Recipe

We welcome contributions of new recipes that solve common problems for Python developers on Azure Functions. If you have a pattern you'd like to share, please follow the established structure to maintain consistency across the cookbook.

To create a new recipe:
1. Copy the `recipes/_template.md` file to a new file in the `recipes/` directory.
2. Fill out all sections defined in the Recipe Contract, ensuring clear and concise language.
3. Include a representative code sample that uses the Python v2 programming model.
4. Add a summary of your new recipe to the catalog table in this file.

Following this template ensures that your contribution integrates seamlessly and provides the same level of value as existing entries.

---

The recipe documentation is designed to be a living resource. As the Azure Functions platform evolves and new patterns emerge, we will continue to update and expand this catalog to serve the needs of the Python community. Each entry represents a distilled version of real-world implementation experience, aimed at reducing the time from idea to production for serverless applications.

Whether you are building a simple HTTP endpoint or a complex event-driven system, these recipes provide the building blocks you need. By following the standardized contract, you can trust that each implementation has considered the essential aspects of serverless development, from local debugging to global scale.

We encourage you to explore the catalog, try out the recipes in your own projects, and provide feedback on how they can be improved. Together, we can build a comprehensive guide for Python developers leveraging the power of Azure Functions.
