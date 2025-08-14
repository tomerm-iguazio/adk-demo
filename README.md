# Restaurant Insights Agent - MLRun ADK Demo

A restaurant insights agent demonstrating ADK integration with MLRun application runtime, datastore, and artifacts. The agent provides restaurant reviews, sanitation reports, and weather information by city using MLRun's artifact retrieval system.

## Features
- **Restaurant Reviews**: Fetches and analyzes restaurant reviews (stored as MLRun artifact)
- **Sanitation Reports**: Provides restaurant sanitation data (stored as separate MLRun artifact)  
- **Weather Integration**: Real-time weather information by city
- **Location Services**: Restaurant location lookup
- **MLRun Integration**: Demonstrates datastore and artifact retrieval with ADK runtime

## Setup & Installation

1. **Install Demo Content**:
   ```bash
   # Add all adk-demo content to your /User directory
   cp -r adk-demo/* /User/

2. **Configure Secrets**:
    ```bash
    # Copy the template and configure your secrets
    cp /User/secrets.env.template /User/secrets.env
    # Edit secrets.env with your actual API keys and credentials

3. **Upload parquet files**: 
   - Upload restaurants_reviews.pq to v3io://projects/adk-project/
   - Upload restaurants_sanitation_reports.pq to s3://bucket_name/path/...
   <br><br>
   You can upload these files manually or via ingestion. 
   Please make sure you are authorized to access these file
   locations using the credentials provided in secrets.env.
