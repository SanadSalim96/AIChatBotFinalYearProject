
# add directories for calling submodule
import os, sys
currentDir = os.path.dirname(os.path.realpath(__file__))
parrentDir = os.path.dirname(currentDir)
sys.path.append(parrentDir)

class ResolverMainPage:

    def AboutPage():
        from webScraping import aboutPage
        return aboutPage.readAboutSQU()

    def FFSearch(name):
         from webScraping import facultyStaff
         if name is not None:
            listingName = name.split()
            listingName.remove(listingName[0])
            name = ' '.join(listingName)
         return facultyStaff.searchFF(name)
    
    def engineer():
        from webScraping.scrapingENG2 import Engineer
        return Engineer.electrical()


    



def resloverIntents(int, arg = None):
    return {
        'AboutSQU' : ResolverMainPage.AboutPage(),
        'Electrical': ResolverMainPage.engineer(),
        'searchFF' : ResolverMainPage.FFSearch(arg),
    }.get(int, 0) # return 0 if the resolver doesnt find match requests

print(resloverIntents('Electrical'))
