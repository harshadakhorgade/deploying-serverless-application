
---

# Deploying a Serverless App Using API Gateway, DynamoDB, and Lambda

This guide explains how to set up a serverless application on AWS. The application includes an API Gateway that interacts with Lambda functions to perform CRUD operations on a DynamoDB table.

---

## Prerequisites
- **AWS Account**: Ensure you have access to the AWS Management Console.
- **IAM User Permissions**: Administrator access or permissions to create IAM roles, Lambda functions, DynamoDB tables, and API Gateway resources.
- **Codebase**: A ZIP file containing your Lambda function code.

---

## Steps to Deploy the Application

### 1. **Create an IAM Role**
This role allows the Lambda function to interact with DynamoDB and write logs to CloudWatch.

#### Steps:
1. Go to **IAM** in the AWS Console.
2. Click **Roles** > **Create Role**.
3. Select **AWS Service**.
4. Choose **Use Case**: **Lambda**.
5. Click **Next**.
6. **Attach Policies**:
   - `AWSLambdaBasicExecutionRole`: Allows Lambda to write logs to CloudWatch.
   - `AmazonDynamoDBFullAccess`: Grants full access to DynamoDB.
7. Click **Next**.
8. Name the role: `user_lambda_role`.
9. Click **Create Role**.

---

### 2. **Create a DynamoDB Table**
DynamoDB is a NoSQL database that will store the data.

#### Steps:
1. Go to **DynamoDB** in the AWS Console.
2. Click **Create Table**.
3. Enter the table name: `mydata` (or any name of your choice).
4. Set **Partition Key**: `email` (type: String).
5. Click **Create Table**.

---

### 3. **Create a Lambda Function**
Lambda is the compute service that will execute your code.

#### Steps:
1. Go to **Lambda** in the AWS Console.
2. Click **Create Function**.
3. Choose **Author from Scratch**.
4. Fill in the details:
   - **Function Name**: `my_lambda_function` (or any name you prefer).
   - **Runtime**: `Python 3.x`.
   - **Execution Role**: Select `user_lambda_role` created earlier.
5. Click **Create Function**.
6. Upload your code:
   - In the **Code Source** section, click **Upload from** > **.zip file**.
   - Upload the ZIP file containing your Lambda function code.
   - Click **Deploy**.

---

### 4. **Create an API Gateway**
API Gateway serves as the entry point for your application, exposing HTTP endpoints to interact with the Lambda function.

#### Steps:
1. Go to **API Gateway** in the AWS Console.
2. Choose **REST API**.
3. Click **Build**.
4. Select **New API**.
5. Enter the details:
   - **API Name**: `my_serverless_api`.
   - **Endpoint Type**: `Regional`.
6. Click **Create API**.

---

### 5. **Create Methods in API Gateway**

#### **GET Method**:
1. In the API Gateway console, click on **Resources**.
2. Click **Create Method** and choose `GET`.
3. Select **Lambda Function** as the integration type.
4. Enable **Lambda Proxy Integration**.
5. Enter your Lambda function's name (`my_lambda_function`).
6. Click **Save**.

#### **POST Method**:
1. Repeat the steps for creating the `POST` method.
2. Use the same Lambda function.

---

### 6. **Deploy the API**
1. In API Gateway, click **Actions** > **Deploy API**.
2. Choose **New Stage**.
3. Enter the stage name: `prod` (or any other name).
4. Click **Deploy**.

---

### 7. **Test the API**
1. Copy the API Gateway URL from the **Invoke URL** (e.g., `https://{api-id}.execute-api.{region}.amazonaws.com/prod`).
2. Test with a browser or tools like Postman.
   - **GET**: Visit the URL in a browser to retrieve data.
   - **POST**: Use Postman to send a POST request with JSON data.

---

## Explanation of the Architecture

### Architecture Diagram:
```plaintext
+-------------+            +-------------+            +---------------+
|             |  HTTP Req  |             | Invoke Fn  |               |
| API Gateway +----------->|   Lambda    +----------->|   DynamoDB     |
|             |            |             |            |               |
+-------------+            +-------------+            +---------------+
```

1. **API Gateway**: Exposes HTTP endpoints for the client.
2. **Lambda**: Executes custom business logic (e.g., process requests, interact with DynamoDB).
3. **DynamoDB**: Stores and retrieves data for the application.

---

## Example Scenarios

### Sample `POST` Request:
**URL**: `https://{api-id}.execute-api.{region}.amazonaws.com/prod`
**Body**:
```json
{
    "fname": "Harshada",
    "lname": "Khorgade",
    "email": "harshada@gmail.com",
    "message": "Hello World"
}
```

### Sample `GET` Response:
```json
{
    "data": [
        {
            "fname": "Harshada",
            "lname": "Khorgade",
            "email": "harshada@gmail.com",
            "message": "Hello World"
        }
    ]
}
```

---

## Common Issues and Fixes

1. **"403 Forbidden" in API Gateway**:
   - Ensure the Lambda function has correct permissions by attaching the `AWSLambdaBasicExecutionRole` policy.
2. **"Missing Table Error in DynamoDB"**:
   - Verify that the table name in your Lambda code matches the DynamoDB table name.
3. **Lambda Function Errors**:
   - Check the Lambda function logs in **CloudWatch Logs** for debugging.

---




### **Explanation of the Lambda Function Code**

This code implements an AWS Lambda function that handles HTTP requests (via API Gateway) to either display an HTML form (GET request) or store form data into DynamoDB (POST request). Below is a breakdown of the code:

---

### **Imports:**
- **json**: Used for encoding and decoding JSON data.
- **os**: Not used in the code but can be used to interact with the operating system (e.g., to access environment variables).
- **boto3**: The AWS SDK for Python, used to interact with AWS services, in this case, DynamoDB.
- **urllib.parse**: Provides functions for parsing URL-encoded data, especially useful for form submissions.

---

### **`lambda_handler` Function**
This is the entry point for the Lambda function. It receives the `event` and `context` as parameters:
- `event`: Contains information about the incoming request, such as HTTP method, query parameters, and body.
- `context`: Provides runtime information about the Lambda function (not used here).

#### **Function Flow:**
1. **Error Handling**: The function uses a `try-except` block to catch and return any errors that may occur during processing.
2. **Routing the Request**: The `page_router` function is called to route the request based on the HTTP method (`GET` or `POST`).

---

### **`page_router` Function**
This function routes the request based on the HTTP method provided in the event object:
1. **GET Request**:
   - Reads the `contactus.html` file (the contact form) from the local file system.
   - Returns the HTML content as the response with a `200 OK` status.
   
2. **POST Request**:
   - Calls the `insert_record` function to save the submitted form data into DynamoDB.
   - Reads the `success.html` file (a success page) from the local file system.
   - Returns the HTML content as the response with a `200 OK` status.
   
   **Error Handling**: If an error occurs in either case, a `500 Internal Server Error` response is returned with the error message.

---

### **`insert_record` Function**
This function handles the insertion of the form data into DynamoDB:
1. **Form Body Decoding**:
   - If the `formbody` is URL-encoded (common with form submissions), it is decoded into a dictionary.
   - If the form data is a JSON string, it is parsed into a dictionary.
   
2. **DynamoDB Client**: 
   - The `boto3` client for DynamoDB is used to interact with the DynamoDB service.
   
3. **Inserting Data**:
   - The function inserts the form data (`fname`, `lname`, `email`, and `message`) into the `mydata` table in DynamoDB using the `put_item` API.
   
4. **Response**: 
   - After inserting the data, the function returns the DynamoDB response.

---

### **Workflow Summary:**
1. **GET Request**: When the client sends a `GET` request, the Lambda function returns the HTML form (`contactus.html`).
2. **POST Request**: When the client submits the form via a `POST` request, the Lambda function:
   - Decodes and processes the form data.
   - Inserts the data into DynamoDB.
   - Returns a success page (`success.html`).

---

### **Important Notes**:
- **DynamoDB Table**: The code assumes that a DynamoDB table named `mydata` exists with the necessary schema to store the form data. Ensure the table exists before running this function.
- **Error Handling**: The Lambda function is designed to return a `500 Internal Server Error` if any exceptions occur while reading files, processing requests, or interacting with DynamoDB.
- **Local Files**: The HTML files (`contactus.html` and `success.html`) must be available in the Lambda environment, but AWS Lambda typically does not allow direct access to the file system. In practice, you might want to use an S3 bucket to store these HTML files and read them from there instead.

---

This code can be deployed as a serverless application in AWS, where the API Gateway triggers the Lambda function, and DynamoDB is used to store the data from the form submission.
