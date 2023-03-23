# partially copied from https://github.com/Azure/azure-kusto-python/blob/master/azure-kusto-ingest/tests/sample.py
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait 
import io, os
from azure.kusto.data import KustoConnectionStringBuilder
from azure.kusto.data.data_format import DataFormat
from azure.kusto.ingest import KustoStreamingIngestClient, ManagedStreamingIngestClient, IngestionProperties, QueuedIngestClient, ColumnMapping
import poslog_generator

def main():
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
    pool = ThreadPoolExecutor(max_workers=10)
    futures = []

    while count < 1000:# 40000000 / 15 / 60:
        poslog = poslog_generator.generate_poslog()
        str_stream = io.StringIO(poslog)
        future = pool.submit(client.ingest_from_stream, stream_descriptor=str_stream, ingestion_properties=ingestion_properties)
        futures.append(future)
        count = len(futures)
        if count % 10 == 0:
            print(count)

    print("Awaiting futures")
    done, not_done = wait(futures)
    print("All futures awaited")
    print(list(done)[0].exception())

if __name__ == "__main__":
    main()
