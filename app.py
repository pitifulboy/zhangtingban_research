from random import randrange
from flask import Flask, render_template
from pyecharts import options as opts
from pyecharts.charts import Bar

from A_dapan_zhangdie_fudufenbu import draw_zhangdie_fenbu_bar
from A_n_days_dapan import n_days_dapan

app = Flask(__name__, static_folder="templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/oneday_zhagndiefenbu")
def get_bar_chart_oneday_zhagndiefenbu():
    querydate = '20220621'
    # 添加当日涨跌情况
    c = draw_zhangdie_fenbu_bar(querydate)
    return c.dump_options_with_quotes()


@app.route("/days_amounts")
def get_bar_chart_days_amounts():
    enddate = '20220621'
    # 添加当日涨跌情况
    c = n_days_dapan(enddate)
    return c.dump_options_with_quotes()


if __name__ == "__main__":
    app.run()
