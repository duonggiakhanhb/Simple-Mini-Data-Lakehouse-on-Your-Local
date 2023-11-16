# Simple Mini Data Lakehouse on Your Local

This repository enables you to set up a local data lakehouse environment to work with fake banking data generated into SQL using Apache Spark and various tools like MinIO, Dremio, Nessie Catalog, and Apache Iceberg.

## Introduction

This setup allows you to:

- Generate synthetic banking data using Python Faker library.
- Use Apache Spark to load this data into a data lakehouse environment.
- Utilize MinIO for object storage.
- Employ Dremio for data cataloging, query, and analytics.
- Benefit from versioning and metadata management via Nessie Catalog and Apache Iceberg.
- Interact with the data through SQL-like queries using Dremio's interface.
- Visualize and analyze data with Superset.

## Folder Structure

```
faker/
  create-table.py
  fake-data.py
/spark-notebook
  spark.ipynb
/docker-compose.yml
/README.md
```
- `faker/`: Contains scripts essential for generating simulated banking data.
- `spark-notebook/`: Houses the Spark notebook instrumental in data loading processes.
- `docker-compose.yml`: Central configuration file for orchestrating MinIO, Dremio, Nessie Catalog, and other necessary services.


## Technologies Used

- **Apache Spark:** Distributed data processing engine used for ETL (Extract, Transform, Load) tasks on large datasets.
- **Iceberg:** Table format for the Data Lakehouse, providing ACID transactions and schema evolution capabilities.
- **Dremio:** Data lakehouse query engine for interactive analytics, supporting SQL queries across various data formats.
- **Nessie:** Git-like versioning and branching for the Data Lakehouse, allowing precise control over data versions.
- **MinIO:** Object storage solution used for scalable and efficient storage of large volumes of data.

These technologies and tools work cohesively to establish a local data lakehouse environment, facilitating data generation, storage, processing, querying, and visualization for synthetic banking data.

## Steps to Build the Data Lakehouse


1. **Clone Repository:**
- Clone the repository to your local environment:
    ``` 
    git clone https://github.com/your_username/your_repo.git
    ```

2. **Install Dependencies and Generate Data:**
- Install dependencies and generate the banking data:
    ```
    pip install -r requirements.txt
    python faker/fake-data.py
    ```



3. **Start MinIO:**
- Start the MinIO service using Docker Compose
  ```
  docker-compose up -d minio
  ```
- Login to MiniO with **username and password: minioadmin**
- Create an access key and a bucket named "data-lakehouse" in MinIO.
![Create Minio access key](assets/image/minio_accessKey.png)
  Create a bucket named "data-lakehouse" in MinIO.
![Create Minio bucket](assets/image/minio_bucket.png)
  After successfully creating the bucket, you will see the following screen.
![Minio bucket created](assets/image/minio_empty.png)

4. **Configure Environment:**
- Add MinIO access key and path to the `.env` file.
![Configure environment](assets/image/env.png)

5. **Build and Start Services:**
- Build and launch the services:
    ```
    docker-compose build
    docker-compose up -d
    ```

6. **Setting up Dremio:**
- Access the Dremio UI at `localhost:9047`.
- Create a new account and add a source using metadata specified in the `.env` file:
  - create a new account
  ![Create Dremio account](assets/image/dremio_account.png)
  - add a new source
  ![Create Dremio source](assets/image/dremio_add_source.png)
  - select the source type as Nessie
  ![Select Dremio source type](assets/image/dremio_source_type.png)
  - add the Nessie Catalog URL
  ![Add Dremio source URL](assets/image/dremio_source_url.png)
  - add path, access key and more properties
    ```
    fs.s3a.path.style.access true
    fs.s3a.endpoint minio:9000
    dremio.s3.compat true
    ```
    ![Add Dremio source properties](assets/image/dremio_source_properties.png)
  - After successfully adding the source, you will see the following screen. It's empty because we haven't loaded any data yet.
  ![Dremio source added](assets/image/dremio_source_added.png)


7. **Data Loading:**
- Access the provided Spark notebook link.
![Spark notebook link access](assets/image/spark_log.png)
- Execute the `spark.ipynb` notebook to load data into the data lakehouse.
![Spark home](assets/image/spark_home.png)
![Spark notebook](assets/image/spark_notebook.png)
- After completion, refresh Dremio to visualize the newly loaded data.
![Dremio data loaded](assets/image/dremio_data_loaded.png)

8. **Querying Data:**
- Create a new View named **payment** in Dremio to query the data.
  ```sql
  SELECT DATE_DIFF(TO_DATE(TO_TIMESTAMP(TransactionDate, 'YYYY/MM/DD HH24:MI:SS', 1)), 1) AS TransactionDate, SUM(Amount) AS TotalAmount
  FROM nessie.transactions
  WHERE TransactionType='Payment'
  GROUP BY TransactionDate
  ```
  Click **Save View as**, named it **payment** and save it in **nessie** source.
![Dremio create view](assets/image/dremio_create_view.png)

9. **Dashboard with Apache Superset:**

- Navigate to the Superset UI at `localhost:8088` and login with username and password: `admin`.
![Superset login](assets/image/superset_login.png)
- Establish a new database connection, selecting Dremio as the database type.
  Click **Settings** -> **Database Connection** -> **+ Database** -> chossen **Orther** as the database type.
  Utilize the URL format: 
    ``` 
    dremio+flight://{username}:{password}@{host}:{port}/dremio?UseEncryption=false 
    ```
  Example: 
    ``` 
    dremio+flight://dremio:dremio123@dremio:9047/dremio?UseEncryption=false 
    ```
![Superset create database](assets/image/superset_create_database.png)

- Add a new dataset using the **payment** view created in Dremio.
![Superset create dataset](assets/image/superset_create_dataset.png)
- Create a new chart and add the dataset to visualize the data.
![Superset create chart](assets/image/superset_create_chart.png)

## Conclusion
This repository presents a streamlined and accessible framework for creating a local data lakehouse environment. By combining tools like MinIO, Dremio, Nessie Catalog, and Apache Iceberg, it provides a versatile platform for generating simulated banking data and efficiently loading it using Apache Spark.

Through step-by-step instructions, this setup enables users to explore data pipelines, experiment with diverse querying techniques, and perform analytical tasks in a controlled local environment. Whether for learning, experimentation, or prototyping, this data lakehouse setup offers a valuable playground for data enthusiasts, analysts, and developers.

We hope this repository serves as a solid foundation for your data exploration journey. Your feedback, contributions, and suggestions are warmly welcomed as we strive to improve and expand the capabilities of this local data lakehouse.

Thank you for exploring this repository, and happy data processing!

![Thank you](https://www.memesmonkey.com/images/memesmonkey/de/de36b9389eb6b84b72182275ed963547.jpeg)

## References
[Alex Merced - Creating a Local Data Lakehouse using Spark/Minio/Dremio/Nessie](https://www.linkedin.com/pulse/creating-local-data-lakehouse-using-alex-merced%3FtrackingId=owFrZg3DS7Ot0LnLS6Oz7A%253D%253D/?trackingId=owFrZg3DS7Ot0LnLS6Oz7A%3D%3D)

[Apache Superset](https://superset.apache.org/docs/intro)

[Apache Iceberg](https://iceberg.apache.org/)

[Apache Spark](https://spark.apache.org/)

[Dremio](https://www.dremio.com/)

[MinIO](https://min.io/)

[Nessie Catalog](https://projectnessie.org/)

## Author

- Adam Nguyen
- GitHub: [github.com/duonggiakhanhb](https://github.com/duonggiakhanhb)

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the [LICENSE](LICENSE) file for details.


