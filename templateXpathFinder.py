from difflib import SequenceMatcher
from bs4 import BeautifulSoup
import argparse, os
# import re
# import glob
# import statistics 
# import numpy
# from collections import defaultdict, Counter
# import numpy as np
# work with paths in any os

#######################################################
# Object HTMLelements:
# Contains all the information we extracte from each
# HTMLelement and stores them for future use
######################################################
class HTMLelement:
    def __init__(self, ID, tag='html', parent=None, Xpath='/', classNames=None, level=-1, content= "", template = None, children=[], allContent = "", score=0):
        self.ID = ID
        self.tag = tag
        self.parent = parent
        self.Xpath = Xpath
        self.classNames = classNames
        self.level = level
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
        rep += "\n\t\t\"Similarity With Siblings\": "+str(self.avgSimilarityWithSiblings)+""
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

##########################################
# function: get_class_hierarchy(file_path):
# takes in a files path of the input file as a parameter
# reads in the html, and receursively iterates through
# all the html elements extracting information from them
# as it does
###########################################
def get_class_hierarchy(file_path, minimumDecendants, scoreSimilarity, similarClassnames, contetentSimilarity, keyword):
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

    for data in soup(['style', 'script', 'head', 'footer', 'noscript', 'form', 'link', 'svg']):
        # Remove tags
        data.decompose()

    REMOVE_ATTRIBUTES = [
    'lang','language','onmouseover','onmouseout','script','style','font',
    'dir', 'aria-label', 'data-testid', 'onload', 'id']

    for attr_del in REMOVE_ATTRIBUTES:
        [s.attrs.pop(attr_del) for s in soup.find_all() if attr_del in s.attrs]


    # print(soup.prettify())
        
    # print(soup)

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

    # class_counts = Counter(class_names)

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
        # freq = class_counts[class_name]
        txt = (node)
        allContent = str(txt.text).strip()
        allContent = allContent.replace("\n","\t")
        allContent = allContent.replace("\t\t"," ")
        # allContent = re.sub("\t\t", " ", allContent)
        # allContent = re.sub("(\|\|\|){2,}", " |||", allContent)
        # allContent = re.sub("\n", " ", allContent)
        # allContent = re.sub(" +", " ", allContent)
        txt = txt.find(string=True, recursive=False)
        # txt = str(txt).replace("\n", "")
        txt = str(txt).replace("None", "")

        # tagValues = defaultdict(lambda: 1)
        # tagValues["ContentBlock"] =  0
        # tagValues["img"] =  1
        # tagValues["a"] =  1
        # tagValues["button"] =  1

        # score = tagValues[tag]
        score = 1
        # if tag == "ContentBlock":
        #     score = 0
        elementData.append(HTMLelement(ID,tag, parentID, XPATH, class_name, depth, "", node, [], (allContent), score ))

        if len(txt) > 0:
            tag = "ContentBlock"
            parentID = lastElem
            lastElem = len(elementData)
            ID = lastElem
            XPATH = ( str(elementData[parentID].Xpath) )
            contentDepth = depth+1
            # freq = 0
            score = 0
            elementData.append(HTMLelement(ID,tag, parentID, XPATH, "", contentDepth, txt, None, [], (allContent), score ))

        if node not in visited:
            visited.add(node)
            for child in node.findChildren(recursive=False):
                dfs(visited, child, depth+1, lastElem)
    # Driver Code
    # print("Following is the Depth-First Search...")
    dfs(visited, htmlElem, 0, -1)
    # print("DFS Complete...")

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
        r = (smallerScore > val)  # type: ignore
        return r
    def scoresAreWithinPercent(score1, score2, val = 0.2):
        largerScore = max(score1, score2)
        r = abs(score1 - score2) < (largerScore*val)  # type: ignore
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
    def containsKeyWord(obj1, obj2, k):
        if (k == None):
            return True
        o1 = obj1.strip().lower()
        o1 = " ".join(o1.split())
        o2 = obj2.strip().lower()
        o2 = " ".join(o2.split())

        r = False
        if k.lower() in o1 or k.lower() in o2:
            r = True
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
    def conditionsMet(obj1, obj2, minDesc, scoreSim, simClassnames, contSim, keyword):
        cond1 = depthIsMoreThan(obj1.score, obj2.score, minDesc)  # does the sibling with less decendants have at least x amount of decendants  
        cond2 = scoresAreWithinPercent(obj1.score, obj2.score, scoreSim) # do both siblings 
        cond3 = classNamesAreSimilar(obj1.classNames, obj2.classNames, simClassnames)
        cond4 = hasContent(obj1.allContent)
        cond5 = hasContent(obj2.allContent)
        # cond6 = True
        cond6 = contentSimilar(obj1.allContent, obj2.allContent, contSim)
        cond7 = containsKeyWord(obj1.allContent, obj2.allContent, keyword)
        return ( cond1 and cond2 and cond3 and cond4 and cond5 and cond6 and cond7)
    
    
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
                        if conditionsMet(a_elem, b_elem, minimumDecendants, scoreSimilarity, similarClassnames, contetentSimilarity, keyword):
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
def printXpathToFile(file, data, printStat):
    with open(file, 'w', encoding="utf-8") as file:
        counter = 0
        for value in data:
            counter += 1
            file.write(str(value.Xpath)+"\n")
            if(printStat):
                file.write(str(value.allContent)+"\n\n")

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




def analyzeOneHtmlFile(htmlFile, outputLocation, printStatus, 
                       minNumberOfDecendantsToConsider, similarityPercentOfDecendantsBetweenElemenent, 
                       classNameSimilarity, contentSimilarity, keyword ):
    elements, par_canidate, temp_canidate = get_class_hierarchy(htmlFile, minNumberOfDecendantsToConsider, similarityPercentOfDecendantsBetweenElemenent, classNameSimilarity, contentSimilarity, keyword)

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
    if outputLocation != None:
        templateXpath = []
        if( currentBestParentCanidate == None):
            with open(outputLocation, 'w', encoding="utf-8") as file:
                file.write("No template identified")
        else:
            for child in currentBestParentCanidate.children:
                if elements[child].color == 'pink' or elements[child].color == 'yellow':
                    templateXpath.append(elements[child])
            printXpathToFile(outputLocation, templateXpath, printStatus)
    else: 
        templateXpath = []
        if( currentBestParentCanidate == None):
            # with open(outputLocation, 'w', encoding="utf-8") as file:
            print("No template identified")
        else:
            for child in currentBestParentCanidate.children:
                if elements[child].color == 'pink' or elements[child].color == 'yellow':
                    print(elements[child].Xpath)
                    # print(str(printStatus))
                    if(printStatus):
                        print(elements[child].allContent)
                        print()
    # return templateXpath

    # printCanidatesToFile(outputLocation, templateXpath)

def validate_file(f):
    if not os.path.exists(f):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(f))
    return f
def validate_int(n):
    num = int(n)
    if num <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % n)
    return num
def validate_ratio(r):
    num = float(r)
    if num < 0 or num >1:
        raise argparse.ArgumentTypeError("%s is an invalid positive ratio in range[0:1] value" % r)
    return num

def createParser():
    # parser defenition
    parser = argparse.ArgumentParser(
        prog="templateXpathFinder",
        description='''This program is indented to take a local HTMLFILE and 
                        return the XPath of content blocks being used. It works
                        most effectively on websites that have multiple instanzes
                        of the desired template being used, however the program 
                        can still fail if there is error in the HTML block, 
                        there is only one isntance of the template, or if there
                        many other templates that also contains sufficient amount
                        of content'''
                        )
    # parser arguments
    parser.add_argument("-f", "--file-Input", dest="filename", required=True, type=validate_file,
                            help="takes in an HTML file as input, REQUIRED", metavar="FILE")
    parser.add_argument("-d", "--output-Destination", dest="destFile", required=False, type=validate_file,
                            help="file to store output, will output to terminal without it", metavar="FILE")
    parser.add_argument('--show-content', action='store_true', dest="showContent", help="Will display the content found in each XPath, can be usefull in validating the correctness of the templates found")
   
    parser.add_argument('--min-number-of-decendants', required=False, type=validate_int, dest="minNumberOfDecendants",
                        help='''Positive integer. Compare two HTML elemnts, the value passed in represents the minimum 
                                number of decendants each element must have. If they do not meet this criteria the elements
                                will not be furthure considered as a potential template. Default is 1''', default=1)
    
    parser.add_argument('--number-of-descendants-similarity', required=False, type=validate_ratio, dest="percentSimilarityofElements",
                        help='''Positive Float in Range [0:1]. Compare two HTML elements. Multiply the element with the most  
                                number of decendants by the value passed in. This is our difference threshold. 
                                If the difference in number of decendants from both elements is less than the threshold above, the 
                                two elements meet this criteria to be considered potential tempaltes. Default is 0.15''', default=0.15)
    
    parser.add_argument('--min-classname-similarity', required=False, type=validate_ratio, dest="minClassnameSimilarity",
                        help='''Positive Float in Range [0:1]. Compare two the classnames of two HTML elements using a longest 
                                common substring algorithm. The algorithm find the length of the LCS between the classnames and 
                                divides that value by the length of shortest of the two classnames. If the resulting ratio 
                                is larger than value passed in, the two elements meet this criteria to be considered potential 
                                tempaltes. Default is 0.65''', default=0.65)
    
    parser.add_argument('--min-content-similarity', required=False, type=validate_ratio, dest="minContentSimilarity",
                        help='''Positive Float in Range [0:1]. Compare two the textual content of two HTML elements using a sequence 
                                matching similarity algorithm. The algorithm returns a ratio repesing the similart of the content of 
                                both elements if the similarity surpasses the value passed in the two elements meet this criteria to 
                                be considered potential tempaltes. Default is 0.3''', default=0.3)
    parser.add_argument('--keyword', required=False, type=str, dest="keyword",
                        help='''Type Str. At least one of the templates must contain the given key word in order to be considered''', default=None)
    
    
    parser.set_defaults(showContent=False)
    args = parser.parse_args()

    # print(str(args.minNumberOfDecendants))
    # print(str(args.percentSimilarityofElements))
    # print(str(args.showContent))
    # print(str(args.minClassnameSimilarity))
    # print(str(args.minContentSimilarity))
    # print(str(args.keyword))
    analyzeOneHtmlFile(args.filename, args.destFile, args.showContent, args.minNumberOfDecendants, 
                    args.percentSimilarityofElements, args.minClassnameSimilarity, args.minContentSimilarity,
                    args.keyword )


createParser()