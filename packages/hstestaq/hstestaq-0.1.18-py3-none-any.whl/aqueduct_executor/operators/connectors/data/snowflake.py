from typing import Any, Callable, Dict, List, Optional

from aqueduct_executor.operators.connectors.data import config, relational, utils
from aqueduct_executor.operators.connectors.data import connector, extract, load
from aqueduct_executor.operators.utils.enums import ArtifactType
from sqlalchemy import create_engine, engine
from pyspark.sql import SparkSession, DataFrame


class SnowflakeConnector(relational.RelationalConnector):
    def __init__(self, config: config.SnowflakeConfig):
        url = "https://{account_identifier}.snowflakecomputing.com".format(
            account_identifier=config.account_identifier,
        )
        conn_engine = _create_engine(config)

        self.snowflake_spark_options = {
            'sfURL': url,
            'sfAccount': config.account_identifier,
            'sfUser': config.username,
            'sfPassword': config.password,
            'sfDatabase': config.database,
            'sfSchema': config.schema,
            'sfWarehouse': config.warehouse,
        }
        super().__init__(conn_engine)


def _create_engine(config: config.SnowflakeConfig) -> engine.Engine:
    # Snowflake Dialect:
    # https://github.com/snowflakedb/snowflake-sqlalchemy
    url = "snowflake://{username}:{password}@{account_identifier}/{database}/{schema}?warehouse={warehouse}".format(
        username=config.username,
        password=utils.url_encode(config.password),
        account_identifier=config.account_identifier,
        database=config.database,
        schema=config.db_schema,
        warehouse=config.warehouse,
    )
    return create_engine(url)

def extract_spark(self, params: extract.RelationalParams) -> Any:
    assert params.usable(), "Query is not usable. Did you forget to expand placeholders?"

    df = spark.read.format("snowflake").options(**self.snowflake_spark_options).option("query", params.query)

def load_spark(
        self, params: load.RelationalParams, df: DataFrame, artifact_type: ArtifactType
    ) -> None:

    df.write.format("snowflake") \
    .options(**self.snowflake_spark_options) \
    .option("dbtable", params.table) \
    .mode(params.update_mode) \
    .save()