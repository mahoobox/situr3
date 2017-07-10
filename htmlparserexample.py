from html.parser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_data(self, datos):
        print ("Encountered some data  :", datos)
        global mostrados
        mostrados = datos

# instantiate the parser and fed it some HTML
parsero = MyHTMLParser()
parsero.feed('<html><head><title>Test</title></head>'
            '<body><h1>hola yo soy el texto que está en medio</h1></body></html><p>esta es la descripción</p>')
print (mostrados)