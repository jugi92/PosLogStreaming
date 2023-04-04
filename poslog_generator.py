import datetime
from math import ceil
import random
import uuid
from faker import Faker
import json

product_names = json.load(open("products.json", "r"))

def generate_product_name():
    return random.choices(product_names, [random.randint(1,20) for _ in range(len(product_names))])

def string_to_int(string):
    return "".join([str(ord(c)) for c in string])

def generate_price():
    return round(random.gammavariate(2, 1.99), 2)

def generate_lineitem(price, now):
    return f"""<LineItem VoidFlag="false" EntryMethod="RFID" CancelFlag="false" DeleteFlag="false">
        <Sale ItemType="Stock" NotNormallyStockedFlag="false" TaxableFlag="true"
            NonDiscountableFlag="false">
            <ItemID>1607701</ItemID>
            <MerchandiseHierarchy Level="Category" ID="DKT:PassionBrand">1</MerchandiseHierarchy>
            <Description TypeCode="Short">{generate_product_name()}</Description>
            <RegularSalesUnitPrice>{price}</RegularSalesUnitPrice>
            <ExtendedAmount>{price}</ExtendedAmount>
            <ExtendedDiscountAmount>0</ExtendedDiscountAmount>
            <Quantity>{ceil(random.gammavariate(2,0.6))}</Quantity>
            <Tax TaxType="VAT" TaxSubType="Standard" TypeCode="Sale">
                <SequenceNumber>1</SequenceNumber>
                <TaxableAmount TaxIncludedInTaxableAmountFlag="false">{round(price/1.19, 2)}</TaxableAmount>
                <Amount>{round(price - price/1.19, 2)}</Amount>
                <Percent>19</Percent>
                <ReasonCode Description="19%" Name="DKT:HighTaxRate" />
                <Rounding RoundingDirection="Down">0.001667</Rounding>
                <TaxGroupID>1</TaxGroupID>
            </Tax>
            <SerialNumber Type="DKT:ItemLookupCode">3583788755593</SerialNumber>
            <SerialNumber Type="DKT:InputString">3583788755593</SerialNumber>
            <SerialNumber Type="SGTIN">30395DFA835709C0000A28D3</SerialNumber>
            <SerialNumber Type="GTIN">03583788755593</SerialNumber>
            <SerialNumber Type="RFID">0000665811</SerialNumber>
            <Rounding RoundingDirection="Up">0.000000</Rounding>
            <ItemNotOnFileFlag>false</ItemNotOnFileFlag>
            <TaxIncludedInPriceFlag>true</TaxIncludedInPriceFlag>
        </Sale>
        <SequenceNumber>1</SequenceNumber>
        <DateTime TypeCode="Transaction">{now}</DateTime>
    </LineItem>"""

def generate_poslog():
    my_uuid = uuid.uuid4()
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
    no_lineitems = ceil(random.gammavariate(2, 10))
    prices = [generate_price() for i in range(no_lineitems)]

    return f"""
    <POSLog xmlns="http://www.nrf-arts.org/IXRetail/v6.0.0/poslog"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" MajorVersion="6" MinorVersion="0"
        FixVersion="0"
        xsi:schemaLocation="http://www.nrf-arts.org/IXRetail/v6.0.0/poslog ../POSLogV6.0.0.xsd">
        <Transaction TrainingModeFlag="false" TypeCode="SaleTransaction">
            <BusinessUnit>
                <UnitID Name="Munich" TypeCode="RetailStore">7-240-240</UnitID>
            </BusinessUnit>
            <BusinessUnit>
                <UnitID Name="DE" TypeCode="DKT:Country">15-7-7</UnitID>
            </BusinessUnit>
            <Channel OnLineOffLineTypeCode="OffLine">
                <ChannelID Description="RetailStore" />
                <TouchPointID ManagedTypeCode="Retailer" PhysicalDigitalCode="Physical" Name="POS" />
            </Channel>
            <WorkstationID TypeCode="POS" SerialNumber="NEWPOS-GBC024006">101</WorkstationID>
            <SequenceNumber>1966</SequenceNumber>
            <TransactionID>{my_uuid}</TransactionID>
            <POSLogDateTime TypeCode="Message">{now}</POSLogDateTime>
            <POSLogDateTime TypeCode="Transaction">{now}</POSLogDateTime>
            <OperatorID OperatorName="Posdata" AssociateID="Posdata9999">9999</OperatorID>
            <CurrencyCode>EUR</CurrencyCode>
            <TrailerText>
                <Text>
                    REVDQVRITE9OIFNVUlJFWSBRVUFZUy4KVGVsOiAwMjA3IDM5NCAyMDAwCk1vbmRheSAtIEZyaWRheSA5YW0gLSA5cG0KU2F0dXJkYXkgOWFtIC0gOHBtClN1bmRheSAxMC4zMGFtIC0gNXBtCgpTQ09PVEVSIFRPV04gOSBFRiBUSQoxNjA3NzAxICAgICAgICAgICAgICAgICAgICAgIKMgICAxMjQuOTkKUkZJRCA6IDAwMDA2NjU4MTEKQkVMVCBGT1IgQk9UVExFCjIwMDc0NjYgICAgICAgICAgICAgICAgICAgICAgoyAgICAgMi45OQpSRklEIDogMDAwMTIwNjcwMQpCQUNLUEFDSyBBUlAgMTAgQkxBQwo2MzAzMjIgICAgICAgICAgICAgICAgICAgICAgIKMgICAgIDIuNDkKUkZJRCA6IDAwMDcxNjIwMDMKPT09PT09PT09PT0KVG90YWwgICAgoyAgIDEzMC40NwoKMyBJdGVtKHMpCgpNYXN0ZXJjYXJkICAgICAgICAgICAgICAgICAgoyAgIDEzMC40NwoKUkFURSAgICAgICAgIFZBVCBBTVQgICAgICAgICAgIEFNVCBFWENMCjIwJSAgICAgICAgICCjICAgIDIxLjc1ICAgICAgIKMgIDEwOC43MwoKVGhlIDIxLzA2LzE3IDEzOjM5IFBPUyAgICAgNiBUcmFuIDE5NjYKT3BlcmF0b3IgIDogTkxTICAgU3RvcmUgICA6ICA3MDAyNDAKClJFVFVSTlMgUE9MSUNZOiAzNjUgZGF5cwp0byByZXR1cm4gcHJvZHVjdHMsIGp1c3Qga2VlcAp0aGUgcmVjZWlwdCBvciBzaWduIHVwIGZvciBvdXIKZmFudGFzdGljIGZyZWUgREVDQVRITE9OIENBUkQhClZBVCBudW1iZXIgOiBHQiA2NzkgMjYyMiA5NgoKNjYwNzAwMjQwMDAwMDYwMDAwMTk2NjIwMTcwNjIxMTMzODI0</Text>
            </TrailerText>
            <ReceiptNumber>{string_to_int(str(my_uuid))}</ReceiptNumber>
            <RetailTransaction TransactionStatus="Finished">
                {"".join([generate_lineitem(price, now) for price in prices])}
                <Total TotalType="TransactionGrandAmount" TypeCode="Sale">{round(sum(prices), 2)}</Total>
                <Total TotalType="TransactionNetAmount" TypeCode="Sale">{round(sum(prices)/1.19, 2)}</Total>
                <Total TotalType="TransactionTaxAmount" TypeCode="Sale">{round(sum(prices) - (sum(prices)/1.19), 2)}</Total>
                <Total TotalType="DiscountAmount" TypeCode="Sale">0</Total>
            </RetailTransaction>
            <BeginDateTime TypeCode="DKT:Sales">{now}</BeginDateTime>
            <BeginDateTime TypeCode="DKT:Payment">{now}</BeginDateTime>
            <EndDateTime TypeCode="DKT:Sales">{now}</EndDateTime>
            <EndDateTime TypeCode="DKT:Payment">{now}</EndDateTime>
        </Transaction>
    </POSLog>
    """

if __name__ == "__main__":
    print(generate_poslog())
