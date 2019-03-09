#!python3
# encoding: utf-8

import re
import requests
from bs4 import BeautifulSoup


def current_currency():
	data = {}
	url = "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html"
	r = requests.get(url)
	if r.status_code == requests.codes.OK:
		content = r.text
		soup = BeautifulSoup(content, "html.parser")
		currencies = soup.select("td.currency")
		if currencies is not None:
			for it in currencies:
				rate = it.parent.select("span.rate")
				currenty = it.attrs['id']
				if rate is not None:
					data[it.attrs['id']] = rate[0].text
	return data

def history_rate(country):
	data = []
	url = "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/eurofxref-graph-{}.en.html".format(country.lower())
	r = requests.get(url)
	if r.status_code == requests.codes.OK:
		content = r.text
		c = re.compile("chartData\.push\(\{\s*date:\s*new Date\((\d+),(\d+),(\d+)\),\s*rate:\s*(\d+\.\d+)\s*\}\);")
		a = re.findall(c, content)
		for it in a:
			data.append((int(it[0]), int(it[1]) + 1, int(it[2]), it[3]))
	return data


if __name__ == '__main__':
	print('EUROPEAN CENTRAL BANK')
	print('欧洲央行外汇牌价')

	current = current_currency()
	for e in current.items():
		print(e[0], e[1])
	print("USDCNY", round(float(current['CNY']) / float(current['USD']), 4))

	history = history_rate('CNY')
	print(history)

