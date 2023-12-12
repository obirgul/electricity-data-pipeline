## **Tasks Completed**

### **Part 1: Data Collection and Manipulation**

- **Data Scraping**: Gathered data from energy-related APIs. Some of Turkey's energy data were retrieved using EPIAS APIs, Turkey's only electricity market responsible.
- **Data Cleaning**: Employed Pandas for data cleaning and preprocessing.
- **Exploratory Analysis**: Conducted exploratory data analysis to comprehend the dataset in dashboard app.
- **Machine Learning Model**: Utilized scikit-learn to create a simple model based on the dataset.

### **Part 2: Workflow Automation**

- **Workflow Definition**: Designed a robust Airflow for automating data collection, cleaning, and analysis.

### **Part 3: Database Operations**

- **Database Schema Design**: Created a suitable database schema for storing energy data.
- **SQLAlchemy Usage**: Implemented SQLAlchemy to store and query data efficiently.

### **Part 4: Data Transformation**

- Data transformation and cleaning processes were orchestrated using Python functions within Airflow workflows. The implemented Python scripts facilitated data manipulation and cleansing operations for comprehensive data preparation. Leveraging Airflow's task orchestration capabilities, each step of the data transformation process was encapsulated into modular Python functions and organized into logical workflow sequences.

### **Part 5: Visualization (Optional)**

- **Dashboard Creation**: Utilized the Streamlit library in Python to generate a sample web page for our dataset. This approach allowed for quick dashboard creation following data manipulation in Python. Leveraging Streamlit, I visualized the processed data. Streamlit is offering flexibility for additional features such as user interactions, logins, or form implementations to address specific needs.

---

### **Running the Project**

To run the project locally, follow these steps

1. **Clone the Repository**:
    
    ```bash
    git clone <repo-url>
    ```
    
2. **Navigate to Project Directory**:
    
    ```bash
    cd energy-data-analysis
    ```
    
3. **Start the Application**:
Simply execute the following command to build and start the Docker containers:
    
    ```bash
    docker-compose up -d
    ```
    
    This command initiates the environment setup and launches the required services. It builds the Docker images, initializes the databases, and starts the application components.
    
4. **Access the Application**:
    
    Airflow Web Server: Access the Airflow interface at **`http://localhost:8080`** to interact with the workflow orchestration and monitoring tools.
    
    Streamlit Dashboard App: Navigate to **`http://localhost:9101`** to access the Streamlit-powered dashboard application for data analysis and visualization.
    
5. **Shutting Down the Application**:
To stop the application and terminate the running containers, run:
    
    ```bash
    docker-compose down
    ```
    

---