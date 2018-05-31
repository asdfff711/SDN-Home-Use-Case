from flask import Flask, render_template
import pygal

app = Flask (__name__)


@app.route('/')
def index():
    # pie_chart = pygal.Pie(half_pie = True)
    # pie_chart.title = 'Upload Usage'
    # pie_chart.add('IE', 19.5)
    # pie_chart.add('Firefox', 36.6)
    # pie_chart.add('Chrome', 36.3)
    # pie_chart.add('Safari', 4.5)
    # pie_chart.add('Opera', 2.3)
    # pie_chart.render()
    # graph_data = pie_chart.render_data_uri()
    graph_data, down_list = createPie("dl_usage.txt", 'Download Usage')
    up_data, up_list = createPie("up_usage.txt", 'Upload Usage')
    tot_data, tot_list = createPie("tot_usage.txt", 'Total Usage')
    return render_template("home.html", graph_data = graph_data, up_data = up_data, tot_data = tot_data, uploads = up_list, downloads = down_list, total = tot_list)

def createPie(filename, title):
    list = []
    pie = pygal.Pie(half_pie = True)
    pie.title= title
    total = 0

    with open(filename, 'r') as f:
        count = 1
        for line in f:
            parts = line.split(" ")
            pie.add(parts[0], int(parts[1]))
            dict = {'count': str(count), 'proto': parts[0], 'bytes': parts[1]}
            count += 1
            list.append(dict)
    pie.render()
    return pie.render_data_uri(), list



if __name__ == '__main__':
    app.run(debug=True)