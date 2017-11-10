import sqlite3
from flask import Flask, request
import io
import csv
import numpy

app = Flask(__name__)

@app.route('/')
def form():
    return """
        <html>
            <body>
                <center>
                <h1 style = "font-family:algerian; color:#FF0000;">CSV TO DATABASE</h1>

                <form action="/vinod" method="post" enctype="multipart/form-data">
                    <input type="file" name="data_file" />
                    <input type="submit" />
                </form>
                </center>
            </body>
        </html>
    """

@app.route('/vinod', methods=["POST"])
def Read_Csv():
##    reading CSV file

    f = request.files['data_file']
    if not f:
        return "No file"

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
##    print(csv_input)

##    creating tavle ,storing into table and calculation of average

    conn = sqlite3.connect('crisp.db')
    c = conn.cursor()    
    c.execute('''CREATE TABLE HR_COMMA_sep7(Col1 real,Col2 real,Col3 real,\
    Col4 real,Col5 real,Col6 real,Col7 real,Col8 real,Col9 text,Col10 text)''')
    for rows in csv_input :
        c.executemany("INSERT INTO HR_COMMA_sep7(Col1,Col2,Col3,Col4,Col5,Col6,Col7,\
        Col8,Col9,Col10)VALUES(?,?,?,?,?,?,?,?,?,?)", [rows,])              
    xs = []
    c.execute("SELECT avg(col1),avg(Col2),avg(Col3),avg(Col4),avg(Col5)\
    ,avg(Col6),avg(Col7),avg(Col8) FROM HR_COMMA_sep7 ")
    xs.append(c.fetchone())
    print(xs)

    stream.seek(0)
   
    return '''
        <html>
            <body>
                <center>
                <h1 style = "font-family:algerian; color:#FF0000;"></h>
                  place to show the mean
                </center>
                </form>
            </body>
        </html>'''
       

if __name__ == "__main__":
    app.run()
