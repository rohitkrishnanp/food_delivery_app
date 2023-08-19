# food_delivery_app
A sample project done as part of Service Oriented Computing course.

## Run food_delivery_app

### Manual installation
`pip install -r requirements`  
`uvicorn app.main:app --host 0.0.0.0 --port 5003`

### Using Docker
The app can be run using the below command  
`docker-compose up`  
The app can be shutdown using the below command   
`docker-compose down`  

## Run the API-Gateway
Navigate to api-gateway folder
Execute the below command  
`docker-compose up -d`  
To shutdown   
`docker-compose down`  

## API Documentation  
The api documentation can be found in  
<url_path>:<port>/docs

## Development Setup

<https://code.visualstudio.com/docs/python/python-tutorial>
