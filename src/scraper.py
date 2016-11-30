import urllib2, re, sys, json
from bs4 import BeautifulSoup
from jinja2 import Template

class Scraper:
    def __init__(self, url):
        self.url = url
        page = urllib2.urlopen(url)
        html = page.read()
        soup = BeautifulSoup(html, 'html.parser')

        try:
            self.objectDescription = soup.select('#main-col-body > div.section > div.titlepage > div > div > h1')[0].text
            splitDescription = self.objectDescription.split('::')
            self.objectCategory = splitDescription[1]
            self.objectName = splitDescription[2]
            self.schemaDescription = soup.select('.highlights + .section #JSON > pre > code')[0].text
            self.propertyList = map(lambda e: e.text, soup.select('.variablelist > dl > dt'))
            self.propertyDescriptionList = map(lambda e: re.sub('[\s]+', ' ', e.text), soup.select('.variablelist > dl > dd > p'))
            properties = dict(zip(self.propertyList, self.propertyDescriptionList))
            self.requiredProperties = [ k for k, v in properties.items() if 'required: yes' in v.lower() ]
        except(e):
            print e

        self.templateProps = {
          'doc': self.url,
          'objectDescription': self.objectDescription,
          'schemaDescription': self.schemaDescription,
          'className': self.objectName,
          'validProperties': json.dumps(self.propertyList),
          'requiredProperties': json.dumps(self.requiredProperties)
        }

    def getJavascriptClass(self):
        jsTemplate = Template(open('templates/javascript.jinja').read())

        return jsTemplate.render(self.templateProps)

if __name__ == '__main__':
    url = sys.argv[1]
    scraper = Scraper(url)
    print scraper.getJavascriptClass()
