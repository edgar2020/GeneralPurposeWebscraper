 # ucr-webpage-extraction
### About
There is a great deal of data and information stored in websites on the internet. However, each website has a different structure. Even websites that look similar will have an incredible amount of structural difference between them. To extract useful information from each website, it is necessary to create a custom “web scraper” for each website. A web scraper is a piece of software that is used to extract data from a website. Creating a custom web scraper for each new website is very costly and does not scale easily. This project aims to solve this issue by creating an adept and versatile web scraper that automatically studies the website to find repeated structures within the websites code. Our web scraper then uses its findings to output the desired data from within repeated structures. 

This project is a part of UC Riverside's Data Science Summer 2023 Fellowship. Mariam Salloum and Analisa Flores are the supervisors for the 2023 Fellowship cohort. The project group consists of Blessing Nwogu, Edgarventura Melendrez, and Zichao Xiao. The project is done in collaboration with the company DataSeal.io, henceforth referred to as DataSeal. DataSeal owns the right to this project. DataSeal permits us to retain a copy of the project for resume purposes.

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

