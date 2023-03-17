# PosLog analysis with Azure Data Explorer

This repo shows an example where PosLog files (POS=Point of Sale, commonly used in Retail) are generated with random content and streamed to Azure Data Explorer.
The queries are used to build a dashboard about the current sales data on top.

It shows the ease of use converting xml to json and filtering down on the specific line items of the transactions.
In a productive scenario it would be recommended to do the conversion from XML to json only once in the process and basing the following queries on top of that.

Example PosLog XML comes from: 
https://doc.posdata.decathlon.io/poslog/use-cases/retailstore-use-cases/RetailStorePoslogs/7-240-240-20170621133911-101-1966.xml