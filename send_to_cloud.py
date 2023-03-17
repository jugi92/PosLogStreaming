# partially copied from https://github.com/Azure/azure-kusto-python/blob/master/azure-kusto-ingest/tests/sample.py
import io, os
from azure.kusto.data import KustoConnectionStringBuilder
from azure.kusto.data.data_format import DataFormat
from azure.kusto.ingest import KustoStreamingIngestClient, ManagedStreamingIngestClient, IngestionProperties, QueuedIngestClient, ColumnMapping
import poslog_generator


cluster = "https://ingest-jugisadxcluster.westeurope.kusto.windows.net"
#cluster = "https://jugisadxcluster.westeurope.kusto.windows.net"

client_secret = os.environ["KUSTO_CLIENT_SECRET"]
client_id = os.environ["KUSTO_CLIENT_ID"]
authority_id = os.environ["KUSTO_AUTHORITY_ID"]
kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(cluster, client_id, client_secret, authority_id)

#kcsb = KustoConnectionStringBuilder.with_aad_device_authentication(cluster)
#kcsb = KustoConnectionStringBuilder.with_az_cli_authentication(cluster)


client = QueuedIngestClient(kcsb) # fast but queued
#client = KustoStreamingIngestClient(kcsb) # slow but instant
#client = ManagedStreamingIngestClient(dm_kcsb=kcsb)

database_name = "default"
table_name = "PosLog"
ingestion_properties = IngestionProperties(database=database_name, table=table_name, data_format=DataFormat.RAW, column_mappings=[ColumnMapping("xml", "string", ordinal=0)])
count = 0

while True:
    poslog = poslog_generator.generate_poslog()
    str_stream = io.StringIO(poslog)
    client.ingest_from_stream(str_stream, ingestion_properties=ingestion_properties)
    count += 1
    print(count)
