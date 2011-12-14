乱数漢 ~ *Ransukan*<br />
Simple tool to try out different selection algorithms.
Kanji frequency distribution (japanese) is used as primary data source.

---

Installation:

	python install.py

Usage:

	python ransukan.py

or 

	pythonw rk.pyw

Notes: 

* Requires **Python** 2.7
* Require **PyQt** 4.8
* All other required modules should be installed using *install.py*. In case something fails, here's full list:
	* Elixir (requires sqlalchemy)
	* BeautifulSoup
	* matplotlib (requires numpy)

---

Resources info:

* KANJIDIC2 includes only 2500+ frequency ranked kanji (total 13k+)
* Project kanji db is based on most complete frequency list (20k+), courtesy of foosoft.net
* The following randomizers are used:
	* [Quantum Random Bit Generator Service]
	* [QRNG]
	* [RANDOM.ORG]

[Quantum Random Bit Generator Service]: http://random.irb.hr/
[QRNG]: http://qrng.physik.hu-berlin.de/
[RANDOM.ORG]: http://www.random.org/clients/http/
