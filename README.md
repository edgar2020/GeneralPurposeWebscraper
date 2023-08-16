 # ucr-webpage-extraction

### Installation
1. Get a HTML files of a website
2. Clone the repo
   ```sh
   git clone https://github.com/DurtHoldings/ucr-webpage-extraction.git
   ```
3. Install BeautifulSoup packages
   ```sh
   pip install beautifulsoup4
   ```
### Commands
- Help command will provide infomation for each command
    ```sh
    python templateXpathFinder.py -h
    ```
- Run the program
   - `-f file_path.html` is required in order to pass in an HTML file as a parameter.  
       ```sh
       python templateXpathFinder.py -f <file_path>.html 
       ```
   - `-d file_path.html` is an optional prameter that takes in a file_path for the output destination. Without specification, the output will go to the commandline.  
     ```sh
     python templateXpathFinder.py -f the_path_of_your_file.html -d <output_file_path>.txt
     ```
  - `--show-content` is an optional parameter that will display the textual content of the XPaths found
    ```sh
    python templateXpathFinder.py -f <file_path>.html --show-content
    ```
  - `--min-number-of-decendants` is an optional parameter that modifies the minimum number of decendants needed for an element to be considered as candidate templates. Only takes in positive integers integers. The default is 1
     ```sh
     python templateXpathFinder.py -f file_name.html --min-number-of-decendants 5
     ```
  - `--number-of-descendants-similarity` is an optional parameter that modify the similarity in number of decendents between two pairs of descendants. The smaller the number the more similar the number of decendants will need to be. Only takes floats between range [0,1].
     ```sh
     python templateXpathFinder.py -f file_name.html --number-of-descendants-similarity 0.35
     ```
  - `--min-classname-similarity` is an optional parameter that modify the threshold of classname similarity. Classname similarity is found using the ratio between length of the longest common substring and the length of the shortest of the two element's classname. If the ration exceeds the parameter's value then the classnames are deemed similar enough for considreation. Only takes floats between range [0,1].
     ```
     python templateXpathFinder.py -f file_name.html --min-classname-similarity 0.25
     ```
  - `--keyword` is an optional parameter that can select a template by keyword. The program will then also select other elements that use the same template, regardless of if it contains the keyword or not
     ```
     python templateXpathFinder.py -f file_name.html --keyword "Bill Gates"
     ```

