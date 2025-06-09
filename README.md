# Credit Approval System

This is a credit approval system that processes loan applications and customer data to make credit decisions.

## Prerequisites

- Docker
- Docker Compose

## Project Structure

```
credit_approval_system/
├── credit_approval_system/    # Main application code
├── Dockerfile                 # Docker configuration
├── docker-compose.yml        # Docker Compose configuration
├── requirements.txt          # Python dependencies
├── loan_data.xlsx           # Sample loan data
└── customer_data.xlsx       # Sample customer data
```

## Running the Project with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd credit-approval-system
   ```

2. **Build and start the containers**
   ```bash
   docker-compose up --build
   ```
   This command will:
   - Build the Docker image using the Dockerfile
   - Start the application container
   - Set up any required services defined in docker-compose.yml

3. **Access the application**
   - The application will be available at `http://localhost:8000` (or the port specified in your docker-compose.yml)

4. **Stop the application**
   ```bash
   docker-compose down
   ```

## Development

### Running Tests
```bash
docker-compose run --rm app pytest
```

### Viewing Logs
```bash
docker-compose logs -f
```

## Data Files

The project includes two sample data files:
- `loan_data.xlsx`: Contains historical loan application data
- `customer_data.xlsx`: Contains customer information

These files are used for training and testing the credit approval model.

## Environment Variables

The following environment variables can be configured in the `docker-compose.yml` file:

- `DEBUG`: Set to "True" for development, "False" for production
- `SECRET_KEY`: Application secret key
- `DATABASE_URL`: Database connection string

## Troubleshooting

1. If you encounter permission issues:
   ```bash
   sudo docker-compose up --build
   ```

2. If the containers fail to start:
   ```bash
   docker-compose down
   docker system prune -f
   docker-compose up --build
   ```

3. To check container status:
   ```bash
   docker-compose ps
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Product Video: 

https://drive.google.com/file/d/1uY0T6g3C9F-xCJgyOnr9MVVOMnfN3eqk/view?usp=sharing
