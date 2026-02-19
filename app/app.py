from icalendar import Calendar, Event
from datetime import datetime, timezone
from flask import Flask, Response, request, render_template
from flask_cors import CORS

import requests as req, ast


app = Flask(__name__)
CORS(app)

def getSche(year, url):
  data = {'schdulLevel': 'Y', 'srchYear': str(year)}
  headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' }

  res = req.post(url, data=data, headers=headers)
  txt = str(ast.literal_eval(res.text))
  schedule = []

  while txt.count('viewSchdulInfo') > 0:
    ind = txt.index('</a>')
    html = txt[txt.index('viewSchdulInfo') + 14:ind]

    k = html.index('>')
    name = html[k + 1:]

    l = html[:k].split(',')
    start = l[1][2:-1]
    end = l[2][2:-1]

    schedule.append([name, start, end])
    txt = txt[ind + 4:]

  return schedule

@app.route('/')
def main():
  return render_template('index.html')

@app.route('/api/get_mi')
def get_mi():
  try:
    host = request.args.get('host')
    url = f'https://{host}/{host.split(".")[0]}/main.do'
    res = req.get(url).text

    res = res[res.index('schdul') + 6:]
    res = res[res.index('mi=') + 3:]
    mi = res[:res.index('"')]
  except: mi = 'error'

  return mi


@app.route('/cal')
def cal():
  host = request.args.get('host')
  mi = request.args.get('mi')

  url = f'https://{host}/{host.split(".")[0]}/ps/schdul/selectSchdulList.do?mi={mi}'
  year = datetime.now().year

  schedule = []
  schedule.extend(getSche(year, url))
  schedule.extend(getSche(year+1, url))

  cal = Calendar()
  cal.add('prodid', '-//DM//KO')
  cal.add('version', '2.0')
  cal.add('x-wr-calname', '학사 일정')
  cal.add('x-wr-timezone', 'Asia/Seoul')

  id = 1

  for i in schedule:
    name, start_str, end_str = i
    evt = Event()

    start = datetime.strptime(start_str, '%Y/%m/%d').date()
    end = datetime.strptime(end_str, '%Y/%m/%d').date()

    evt.add('uid', f'haksa-{id}')
    evt.add('dtstamp', datetime.now(timezone.utc))
    evt.add('summary', name)
    evt.add('dtstart', start)
    evt.add('dtend', end)
    evt.add('status', 'CONFIRMED')

    cal.add_component(evt)
    id += 1

  ics = cal.to_ical().decode('utf-8')
  return Response(ics, mimetype='text/calendar', headers={'Content-Disposition': 'attachment; filename="calendar.ics"'})
