import base64
import datetime as dt
from email.mime import base
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from .models import TradeData

# import any csv file
def import_csv(request):
    try:
        if request.method == "POST" and request.FILES["myfile"]:

            myfile = request.FILES["myfile"]
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            print(excel_file)
            empexceldata = pd.read_csv("." + excel_file, encoding="utf-8")
            print(type(empexceldata))
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():

                fromdate_time_obj = dt.datetime.strptime(
                    str(dbframe.datetime), "%Y-%m-%d %H:%M:%S"
                )
                obj = TradeData.objects.create(
                    datetime=fromdate_time_obj,
                    close=dbframe.close,
                    high=dbframe.high,
                    low=dbframe.low,
                    open=dbframe.open,
                    volume=dbframe.volume,
                    instrument=dbframe.instrument,
                )
                print(type(obj))
                obj.save()

            return render(
                request, "importexcel.html", {"uploaded_file_url": uploaded_file_url}
            )
    except Exception as identifier:
        print(identifier)

    return render(request, "importexcel.html", {})


# for downloaded excel files
def importer(request):
    # set path of file
    df = pd.read_excel("strategy/myfile.xlsx")
    print((df.datetime))
    format_data = "%Y-%m-%d %H:%M:%S"
    # converting data to objects
    for df in df.itertuples():
        fromdate_time_obj = dt.datetime.strptime(str(df.datetime), format_data)
        obj = TradeData.objects.create(
            datetime=fromdate_time_obj,
            close=df.close,
            high=df.high,
            low=df.low,
            open=df.open,
            volume=df.volume,
            instrument=df.instrument,
        )
    print(type(obj))
    obj.save()
    # print(df.dtypes)
    return render(request, "importexcel.html", {})


def index(request):
    chart = return_graph()
    return render(request, "index.html", {"chart": chart}, status=200)


# for converting data to graph
def return_graph():

    data = TradeData.objects.all()
    plt.switch_backend("AGG")
    values = data.values("datetime", "close")
    df = pd.DataFrame.from_records(values)

    # print(df.head(20))
    df["close"] = df["close"].astype(float)
    df["datetime"] = pd.to_datetime(df["datetime"])
    # print(df["close"])
    df["50_sma"] = df["close"].rolling(window=50, min_periods=1).mean()
    df["20_sma"] = df["close"].rolling(window=20, min_periods=1).mean()
    df["Signal"] = 0.0
    df["Signal"] = np.where(df["20_sma"] > df["50_sma"], 1.0, 0.0)
    df["Position"] = df["Signal"].diff()
    # ploting lines.
    df[["close", "50_sma", "20_sma"]].plot(figsize=(13, 6))
    # ploting buy marker
    plt.plot(
        df[df["Position"] == 1].index,
        df["20_sma"][df["Position"] == 1],
        "^",
        markersize=10,
        color="g",
        label="buy",
    )
    # ploting sell marker
    plt.plot(
        df[df["Position"] == -1].index,
        df["20_sma"][df["Position"] == -1],
        "v",
        markersize=10,
        color="r",
        label="buy",
    )
    plt.ylabel("Price", fontsize=15)
    plt.xlabel("Sequence", fontsize=15)
    plt.title("HINDALCO SMA Crossover", fontsize=20)
    plt.legend()
    plt.grid()

    print(df.head(20))
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode("utf-8")
    buffer.close()

    return graph
