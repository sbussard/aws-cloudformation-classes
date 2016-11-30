from scraper import Scraper

base_url = 'http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/'
extension = 'html'
docs = open('docs.txt').read().split('\n')
docurls = map(lambda doc: base_url + doc + '.' + extension, docs)

def write_javascript_classes():
    output_dir = '../output'

    for url in docurls:
        aws_object = Scraper(url)
        output_file = open(output_dir + '/' + aws_object.objectName + '.js', 'w')
        output_file.write(aws_object.getJavascriptClass())
        output_file.close()

if __name__ == '__main__':
    print 'writing javascript classes...'
    write_javascript_classes()
