const extract = require('./webExtractor.js');


async function getHTMLFromUrls()
{
    const url_counter = {}
    urls = await extract.readFile('./input_files/ucr-entity-extraction-seeds.txt');
    // urls.forEach( await forEachPage(url) );
    urls = urls.slice(171);
    for await( const url of urls)
    {
        try {
            let domain = (new URL(url));
            domain = domain.hostname.replace('www.','');
            // remove the .com
            var end = domain.lastIndexOf('.');
            domain = domain.substring(0, end);
            domain = domain.replace('.', '_');
            if( url_counter[domain] )
            {
                url_counter[domain] += 1;
            }
            else
            {
                url_counter[domain] = 1;
            }
            // console.log(this[index]);
            saveToFile = "./cleaned_"+domain+"_"+url_counter[domain];
            // console.log(saveToFile);
            content = await extract.extractPage(url, saveToFile);
            await extract.cleanExtractedData(content, saveToFile);
        } catch (error) {
            console.log(error)
            continue
        }
    }



    // console.log(urls);
    

}

// saveToFile = "./htmlExtracted.html"
// content = extract.extractPage(url[0], 'cleaned.html');
// extract.cleanExtractedData(saveToFile,'cleaned.html')
// extract.DFS_DOM('./html_files/cleaned.html')


getHTMLFromUrls();

