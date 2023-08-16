#used in simmilar function
from difflib import SequenceMatcher
# web scraper
from bs4 import BeautifulSoup
# regular expressions
import re
# allows html graphing
import graphviz  # type: ignore
# get list of all files in directory(for cleaned html)
import glob
# import statistics 
# import numpy
from collections import defaultdict, Counter
# import numpy as np
# work with paths in any os

#######################################################
# Object HTMLelements:
# Contains all the information we extracte from each
# HTMLelement and stores them for future use
######################################################
class HTMLelement:
    def __init__(self, ID, tag='html', parent=None, Xpath='/', classNames=None, level=-1, frequency=-1, content= "", template = None, children=[], allContent = "", score=0):
        self.ID = ID
        self.tag = tag
        self.parent = parent
        self.Xpath = Xpath
        self.classNames = classNames
        self.level = level
        self.frequency = frequency
        self.content = content
        self.allContent = (allContent)
        self.template = template
        self.color = "white"
        self.template = template
        self.children = children
        self.avgSimilarityWithSiblings = 0
        self.score = score
    ########################################################
    # Formating for how the object is formated when printed
    # ######################################################        
    def __str__(self):
        rep =  "\t{"
        rep += "\n\t\t\"ID\":"+str(self.ID)+","
        rep += "\n\t\t\"ParentId\": "+str(self.parent)+","
        rep += "\n\t\t\"Score Given\": "+str(round(self.score, 2))+","
        rep += "\n\t\t\"ClassTag\": \""+str(self.tag)+"\","
        rep += "\n\t\t\"Level\": "+str(self.level)+","
        rep += "\n\t\t\"X-Path\": \""+str(self.Xpath)+"\","
        rep += "\n\t\t\"ClassNames\": \""+str(self.classNames)+"\","
        rep += "\n\t\t\"Content\": \""+str(self.content)+"\","
        rep += "\n\t\t\"All Content\": \""+str(self.allContent)+"\","
        rep += "\n\t\t\"Children\": "+str(self.children)+","
        rep += "\n\t\t\"Number of Children\": "+str(len(self.children))+","
        rep += "\n\t\t\"Similarity With Siblings\": "+str(self.avgSimilarityWithSiblings)+","
        # rep += "\n\t\t\"template\": \""+str(self.template)+"\","
        rep += "\n\t\t\"Frequency\":"+str(self.frequency)+"\n\t}"
        return rep

##########################################
# Function similar( string a, string b ): 
# using a generic similarity algorithm to
# return the ration of how similar two
# strings are to one another 
############################################
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
    # return False

def commonSubstring(a:str, b: str):
    m = len(a)
    n = len(b)
    # Create a table to store lengths of
    # longest common suffixes of substrings.
    # Note that LCSuff[i][j] contains length
    # of longest common suffix of X[0..i-1] and
    # Y[0..j-1]. The first row and first
    # column entries have no logical meaning,
    # they are used only for simplicity of program
    LCSuff = [[0 for i in range(n + 1)]
                 for j in range(m + 1)]
 
    # To store length of the
    # longest common substring
    length = 0
 
    # To store the index of the cell
    # which contains the maximum value.
    # This cell's index helps in building
    # up the longest common substring
    # from right to left.
    row, col = 0, 0
 
    # Following steps build LCSuff[m+1][n+1]
    # in bottom up fashion.
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                LCSuff[i][j] = 0
            elif a[i - 1] == b[j - 1]:
                LCSuff[i][j] = LCSuff[i - 1][j - 1] + 1
                if length < LCSuff[i][j]:
                    length = LCSuff[i][j]
                    row = i
                    col = j
            else:
                LCSuff[i][j] = 0
 
    # if true, then no common substring exists
    if length == 0:
        return -1
        # return
 
    # allocate space for the longest
    # common substring
    resultStr = ['0'] * length
 
    # traverse up diagonally form the
    # (row, col) cell until LCSuff[row][col] != 0
    while LCSuff[row][col] != 0:
        length -= 1
        resultStr[length] = a[row - 1] # or Y[col-1]
 
        # move diagonally up to previous cell
        row -= 1
        col -= 1
 
    # required longest common substring
    return(''.join(resultStr))


def lcs(X, Y):
    # find the length of the strings
    m = len(X)
    n = len(Y)
 
    # declaring the array for storing the dp values
    L = [[None]*(n + 1) for i in range(m + 1)]
 
    """Following steps build L[m + 1][n + 1] in bottom up fashion
    Note: L[i][j] contains length of LCS of X[0..i-1]
    and Y[0..j-1]"""
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0 :
                L[i][j] = 0 # type: ignore
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1]+1 # type: ignore
            else: 
                L[i][j] = max(L[i-1][j], L[i][j-1]) # type: ignore
 
    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
    return (int(L[m][n]) / min(m,n)) # type: ignore
# end of function lcs

###############################################
# Function: viz_tree( obj tree )
# takes in the array of objects that represents our tree
# takes in the tree and uses the graphviz library to generate
# a graph visualization
##############################################
def viz_tree(tree):
    treeCopy = tree
    w = graphviz.Digraph('./output_files/individualSiteOutput/HTML_tree', format="svg")
    w.attr(ranksep="1")
    for node in treeCopy:
        parentID = str(node.ID)
        parentNode = '('+str(node.ID)+')'+node.tag+" :: "+str(round(node.score, 2))
        w.node(parentID,  parentNode, style="filled", fillcolor=node.color)
        for childNum in node.children:
            child = treeCopy[childNum]
            childID = str(child.ID) 
            w.edge(parentID, childID)
    w.view()  

##########################################
# function: get_class_hierarchy(file_path):
# takes in a files path of the input file as a parameter
# reads in the html, and receursively iterates through
# all the html elements extracting information from them
# as it does
###########################################
def get_class_hierarchy(file_path):
    def xpath_soup(element):
        """
            # Generate xpath from BeautifulSoup4 element.
            # :param element: BeautifulSoup4 element.
            # :type element: bs4.element.Tag or bs4.element.NavigableString
            # :return: xpath as string
            # :rtype: str
            # Usage
        """
        components = []
        child = element if element.name else element.parent
        for parent in child.parents:  # is of type: bs4.element.Tag
            siblings = parent.find_all(child.name, recursive=False)
            components.append(
                child.name if 1 == len(siblings) else '%s[%d]' % (
                    child.name,
                    next(i for i, s in enumerate(siblings, 1) if s is child)
                    )
                )
            child = parent
        components.reverse()
        return '/%s' % '/'.join(components)

    with open(file_path, 'r', encoding="UTF-8") as file:
        html = file.read()
    # Parse the HTML document
    soup = BeautifulSoup(html, 'html.parser')

    # Find all elements with a 'class' attribute
    htmlElem = soup.find("html")
    htmlElemCopy = soup.find_all(class_=True)

    # Extract the class names
    class_names = []
    tags = []
    for elem in htmlElemCopy:
        class_name = elem.attrs.get('class')
        class_string = ' '.join(class_name) if class_name else ''
        class_names.append(class_string)
        tags.append(elem.name)
    # print(tags)

    class_counts = Counter(class_names)

    # children = htmlElem.findChildren(recursive=False)

    visited = set() # Set to keep track of visited nodes of graph.
    elementData = []
    ########################################################
    # dfs (array visisted, HTMLDOMElement node, int depth, int parent)
    # visited is an array of all the htmlElements that have already been demoed
    # HTMLDOMElement node passes in the current node we want to extract
    # depth is just the depth that the node is found in the html tree
    # parent is the ID of the parent class

    # the function is a recuresive DFS algorithm that expands the 
    # entire HTML Tree

    # returns the array of all the HTML elements explored
    # index corresponds to their ID
    ##########################################################
    def dfs(visited, node, depth, parent):  #function for dfs
        # print(type(node)) 
        class_name = ""
        if node.has_attr("class"):
            class_name=node['class']
            class_string = ' '.join(class_name) if class_name else ''
            class_name= class_string
        
        lastElem = len(elementData)
        
        ID = lastElem
        tag = node.name
        parentID = parent
        # XPATH = ""
        # if parentID >= 0:
        #     XPATH = ( str(elementData[parentID].Xpath)+'/'+ node.name)
        XPATH = (xpath_soup(node))
        freq = class_counts[class_name]
        txt = (node)
        allContent = str(txt.text).strip()
        allContent = re.sub("\n\n", "|||", allContent)
        allContent = re.sub("(\|\|\|){2,}", " |||", allContent)
        allContent = re.sub("\n", " ", allContent)
        allContent = re.sub(" +", " ", allContent)
        txt = txt.find(string=True, recursive=False)
        txt = str(txt).replace("\n", "")
        txt = str(txt).replace("None", "")

        tagValues = defaultdict(lambda: 1)
        tagValues["ContentBlock"] =  0
        tagValues["img"] =  1
        tagValues["a"] =  1
        tagValues["button"] =  1

        score = tagValues[tag]
        elementData.append(HTMLelement(ID,tag, parentID, XPATH, class_name, depth, freq, "", node, [], (allContent), score ))

        if len(txt) > 0:
            tag = "ContentBlock"
            parentID = lastElem
            lastElem = len(elementData)
            ID = lastElem
            XPATH = ( str(elementData[parentID].Xpath) )
            contentDepth = depth+1
            freq = 0
            score = tagValues[tag]
            elementData.append(HTMLelement(ID,tag, parentID, XPATH, "", contentDepth, freq, txt, None, [], (allContent), score ))

        if node not in visited:
            visited.add(node)
            for child in node.findChildren(recursive=False):
                dfs(visited, child, depth+1, lastElem)
    # Driver Code
    print("Following is the Depth-First Search...")
    dfs(visited, htmlElem, 0, -1)
    print("DFS Complete...")

    #######################################
    # adds the information of children to
    # each of the node that has children
    ######################################
    count = 0
    for elem in elementData:
        # get parent ID
        parentIDOfCur = elem.parent
        # Only html will have a parent ID that is less than 0
        if parentIDOfCur >= 0:
            elementData[parentIDOfCur].children.append(elem.ID)


    #################################
    # scoreing algorithm
    # (Needs Work / may not be necessary)
    #################################
    def addScore(nodeID):
        for e in elementData[nodeID].children:
            childScore = addScore(e)
            elementData[nodeID].score = elementData[nodeID].score + childScore
        return elementData[nodeID].score
    
    addScore(0)

    #####################################
    # pick template algorithms
     # (Needs Work )
    ###################################
    def depthIsMoreThan(score1, score2, val = 1):
        smallerScore = min(score1, score2)
        r = (smallerScore > val)
        return r
    def scoresAreWithinPercent(score1, score2, val = 0.2):
        largerScore = max(score1, score2)
        r = abs(score1 - score2) < (largerScore*val)
        return r 
    def hasContent(objContent, val=0):
        if len(objContent) > val:
            r = True
        else:
            r = False
        return r 
    def contentSimilar(obj1, obj2, val = 0.2):
        if similar(obj1, obj2) > val:
            r = True
        else:
            r = False
        return r 
    def classNamesAreSimilar(className1, className2, val = 0.5):
        # if neither has a className assune true, that it is a template
        len1 = len(className1)
        len2 = len(className2)
        if( len1 == 0 and len2 == 0 ):
            r = True
        # if both have classNames do the calculation
        elif( len1 > 0 and len2 > 0 ):
            # similarEnough = (similar(className1, className2) > val)
            # lcsLongEnough = (lcs(className1, className2) > val)
            commonSubstringRatioGoodEnough = ( (len(str(commonSubstring(className1, className2))) / min(len1, len2)) > val)
            r = commonSubstringRatioGoodEnough
            # r = similarEnough or lcsLongEnough or commonSubstringRatioGoodEnough
            # print("depth " + str(r))
        # if only one has a classname and the other doesnt assume not the same
        else:
            r = False
        return r
    def conditionsMet(obj1, obj2):
        cond1 = depthIsMoreThan(obj1.score, obj2.score, 2)
        cond2 = scoresAreWithinPercent(obj1.score, obj2.score, 0.15)
        cond3 = classNamesAreSimilar(obj1.classNames, obj2.classNames, 0.65)
        cond4 = hasContent(obj1.allContent)
        cond5 = hasContent(obj2.allContent)
        cond6 = True
        cond6 = contentSimilar(obj1.allContent, obj2.allContent, 0.30)
        return ( cond1 and cond2 and cond3 and cond4 and cond5 and cond6)
    
    
    parentCanidates=[]
    templateCanidates=[]
    canidateFound = False
    dontVisitElems = []
    for elem in elementData:  
        if(elem.ID not in dontVisitElems):
            canidateFound = False 
            for a in elem.children:
                for b in elem.children:
                    if a!=b:
                        a_elem = elementData[a]
                        b_elem = elementData[b]
                        if conditionsMet(a_elem, b_elem):
                            elem.color="yellow"
                            parentCanidates.append(elem)
                            for c in elem.children:
                                c_elem = elementData[c]
                                if( classNamesAreSimilar( a_elem.classNames, c_elem.classNames) or classNamesAreSimilar( b_elem.classNames, c_elem.classNames)):
                                    templateCanidates.append(c_elem.classNames)
                                    c_elem.color="pink"
                                    dontVisitElems.extend(elem.children)
                            canidateFound = True
                            break
                    if canidateFound: break
                if canidateFound: break
                    
        templateCanidates = list(set(templateCanidates))
        parentCanidates = list(set(parentCanidates))
        
    return elementData, parentCanidates, templateCanidates


# genereates the tree visualizer
# viz_tree(elements)

# print out info from each element data to element_info 
def printElementInfoToFile(file, data):
    with open(file, 'w', encoding="utf-8") as file:
        
        file.write("[\n")
        for elem in data[:-1]:
            file.write(str(elem)+",\n")
        file.write(str(data[-1])+"\n")
        file.write("]")

# print our the parent canidates we found 
def printCanidatesToFile(file, data):
    with open(file, 'w', encoding="utf-8") as file:
        counter = 0
        for canidate in data:
            counter += 1
            file.write("<!-- ------------------------------------\n")
            file.write("Canidate "+str(counter) +"\n" )
            file.write(str(canidate)+"\n")
            file.write("Code: -->\n")
            file.write(str(canidate.template)+"\n")
def printXpathToFile(file, data):
    with open(file, 'w', encoding="utf-8") as file:
        counter = 0
        for value in data:
            counter += 1
            file.write("<!-- ------------------------------------\n")
            file.write("Xpath: "+str(value.Xpath) +"\n" )
            file.write("Content: \n\t" )
            file.write(str(value.allContent.replace("||| ", "\n\t"))+"\n")
            file.write("Code: -->\n\n")

# print out classNames we identified
def printClassNamesIdentified(file, data):
    with open(file, 'w', encoding="utf-8") as file:
        counter = 0
        for className in data:
            counter += 1
            file.write("-------------------------------------\n")
            file.write("Canidate "+str(counter) +"\n" )
            file.write(str(className)+"\n")
            file.write("\n")




def analyzeOneHtmlFile(htmlFile, outputLocation, printStatus):
    elements, par_canidate, temp_canidate = get_class_hierarchy(htmlFile)
    if printStatus:
        printElementInfoToFile('output_files/individualSiteOutput/element_info.json', elements)
        print("Number of parent canidates: " + str( len(par_canidate)) )
        printCanidatesToFile( 'output_files/individualSiteOutput/ParentCanidates.html', par_canidate)
        print("Number of ClassName canidates: " + str( len(temp_canidate)) )
        printClassNamesIdentified('output_files/individualSiteOutput/classNameCanidates.txt', temp_canidate)
        viz_tree(elements)
    print("Working with: "+str(htmlFile))
    print("Outputing Template to: "+str(outputLocation))

    # gets the one with most content
    # class canidateScore
    
    # for each canidate
    #   for each child that match the description of template (pink color)
    #       we average the len of content in each of the children
    #   we select the parent who on average has the most content per child
    #   return the XPath of the children who match the description
    currBestScore = 0
    currentBestParentCanidate = None
    for canidate in par_canidate:
        totalContentOfChildren = 0
        numberOfTemplateChildren = 0
        childContent = []
        for child in canidate.children:
            if elements[child].color == "pink" or elements[child].color == "yellow":
                totalContentOfChildren += len(elements[child].allContent)
                childContent.append(elements[child].allContent)
                numberOfTemplateChildren += 1
        avgContentPerTemplateChild = totalContentOfChildren / numberOfTemplateChildren

        # calculatedScore = (avgContentPerTemplateChild * 0.6 + numberOfTemplateChildren * 0.4)
        calculatedScore = avgContentPerTemplateChild
        if( calculatedScore > currBestScore):
            currentBestParentCanidate = canidate
            currBestScore = avgContentPerTemplateChild

    templateXpath = []
    if( currentBestParentCanidate == None):
        with open(outputLocation, 'w', encoding="utf-8") as file:
            file.write(" No template identified")
            file.write(" No template identified")
            file.write(" No template identified")
            file.write(" No template identified")
    else:
        for child in currentBestParentCanidate.children:
            if elements[child].color == 'pink' or elements[child].color == 'yellow':
                templateXpath.append(elements[child])
        printXpathToFile(outputLocation, templateXpath)
    # return templateXpath

    # printCanidatesToFile(outputLocation, templateXpath)


def analyzeMultipeHTMLFiles(htmlFiles):
    counter = 0
    for file in htmlFiles:
        print("("+str(counter)+")")
        counter += 1
        outputFile = str(file).replace('.\\html_files\\', './output_files/idealTemplatesFound/template_')
        analyzeOneHtmlFile(file, outputFile, False)

# FIle we are working with
files = (glob.glob(".\\html_files\\*.html"))
# quick use 
# 9 = advanced-people-search_1.html
# 14 = airbnb_1
workingFiles = []
notWorkingFiles = []
# workingFiles.append(files[0:62])
workingFiles = (files)
# workingFiles.pop(139)
# workingFiles.pop(79)
# workingFiles.pop(66)
# workingFiles.pop(65)
# workingFiles.pop(64)
# workingFiles.pop(63)


# things that are not working
# amazon not working, was not scrapped correctly
notWorkingFiles.append(files[63:66])
# concillion_1 not working because there was not templates that matched our criteria
notWorkingFiles.append(files[79])
# thatThem_4 does not work becuase it has no html
notWorkingFiles.append(files[139])
# chosenFiles = [ files[1] ]
# analyzeOneHtmlFile(files[96], "TestFile.html", True)
analyzeMultipeHTMLFiles(workingFiles)

# ----------------------------------------------------
# Not working:
# 1) ucr-webpage-extraction/output_files/idealTemplatesFound/template_cleaned_advanced-people-search_2.html
    # only one use of tempalte, fails to find the correct template
    # still wrong template, but different one this time, needs more view
# 4) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_amazon_1.html
# 5) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_amazon_2.html
# 6) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_amazon_3.html
# 7) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_amazon_4.html
    # no tempalte found, likely due to error in html of amazon, which messes up our parser
# 9) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_arrestfacts_1.html
    # no tempalte found, only one use of the template, however its odd that no other template was selected
    # now seleting an XPath, but not the correct content, need further look
# 10) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_councilion_1.html
    #  no tempalte found, makes sense becasue the page provided by the link does not find any information, no info to extract
# 12) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_cyberbackgroundchecks_1.html
# 13) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_cyberbackgroundchecks_4.html
    # wrong template, it is too zoomed in, need to grab an outer template    
# 18) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_findpeoplesearch_1.html
# 19) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_findpeoplesearch_2.html
# 20) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_findpeoplesearch_3.html
# 21) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_findpeoplesearch_4.html
# 22) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_findpeoplesearch_5.html
    # wrong template, link was not loading, could not verify cause of issue
# 23) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_idtrue_1.html
    # only faild in this one, link sends us to a home menu, does not actually display any block content that we
    # would be looking for
# 24) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_members_infotracer_1.html
    # only faild in this one, link sends us to a home menu, does not actually display any block content that we
    # would be looking for
# 25) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_peoplefinders_1.html
    # in both cases seems like we are searching tempaltes inside the main templates 
# 28) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_peopleseachnow_2.html
    # in both cases seems like we are searching tempaltes inside the main templates, otherwords
    # wrong template
# 31) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_rocketreach_1.html
# 32) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_rocketreach_2.html
# 33) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_rocketreach_3.html
# 34) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_rocketreach_4.html
# 35) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_rocketreach_5.html
# 36) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_rocketreach_6.html
# 37) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_rocketreach_7.html
    # permissions denied due to search limits and anti-bot protocals
    # got permission this time, however did not get correct value
# 40) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_spokeo_1.html
    # extractding the wrong tempalte, somehow got a template for nav, unsure how it didnt give 
    # preference to the correct template based on currect criteria
# 41) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_thatsthem_1.html
# 42) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_thatsthem_2.html
# 43) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_thatsthem_3.html
# 44) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_thatsthem_4.html
# 45) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_thatsthem_5.html
    # no tempalte found, due to antibot prototocols
# 46) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_usphonebook_1.html
    # wrong template, too zoomed in, is template inside main template
# 48) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_vrbo_1.html
# 49) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_vrbo_2.html
# 50) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_vrbo_3.html
# 51) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_vrbo_4.html
# 52) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_vrbo_5.html
# 53) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_vrbo_6.html
# 54) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_vrbo_7.html
# 55) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_vrbo_8.html
# 56) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_vrbo_9.html
    # is grabing the information from a calander dropdown menu, instead of the actuall 
    # correct template
# 57) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_wellnut_2.html
    # No tempalte found, the name searched did not pop up any results
    # also the suggestion only displays one name, which at the moment our algorithm cannot 
    # detect due to needing multiple uses of the tempalte.
    # Needs mmore viewing  
# 58) radis
    # broke this one, now grabing wrong values 
# 59) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_publicrecordsnow_2
    # breaks when used to work, however there is still at least one working version
# 30) ucr-webpage-extraction\output_files\idealTemplatesFound\template_cleaned_publicrecordsnow_1.html
    # is block content, but the wrong block content
    # now works at the cost of the other ne not working 
# 60) what data should proprtyIQ grab? there are multiple templates that looks just as 
    # valid as a response as anotherm maybe