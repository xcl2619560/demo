def info(object, spacing=10, collapse=1):   
    """Print methods and doc strings.
    
    Takes module, class, list, dictionary, or string."""
    methodList = [method for method in dir(object) if callable(getattr(object, method))]
    processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
    print "\n".join(["%s %s" %
                      (method.ljust(spacing),
                       processFunc(str(getattr(object, method).__doc__)))
                     for method in methodList])
class Hello(object):
    '''this class will print 'say hello'.
    '''
    def __init__(self, string = None):
        self.string = string
        #self.sayHello()
        
    def sayHello(self):
        print "&&&&&& ",self.string
        
if __name__ == "__main__":
    a = Hello('hello world.')
    print info(a).__doc__
    #print info.__doc__