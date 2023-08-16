const puppeteer = require('puppeteer-extra');
// const tree = require('./htmlTree.js')
// const jsdom = require("jsdom");
// const Stack = require('./stack.js');
const fs = require('fs/promises');
const { type } = require('os');
const StealthPlugin = require('puppeteer-extra-plugin-stealth')

puppeteer.use(StealthPlugin())


async function extractPage(url, saveTo)
{
    console.log("Starting...")
    const browser = await puppeteer.launch({headless:true})
    const page = await browser.newPage();
    // opens url
    console.log("Opening URL... "+ url)
    await page.goto(url, {
        waitUntil: "networkidle0",
        timeout: 0
    })
    console.log("Taking Screenshot...")
    await page.screenshot({path: "./screenshot/"+saveTo+".png", fullPage: true})

    // web scraping part
    console.log("content grab...")
    const contentGrab = await page.evaluate(() => {
        return Array.from(document.querySelectorAll("html")).map(x => x.outerHTML);
    });
    console.log("Closing Browser...");
    await browser.close();
    console.log("Browser Closed...");
    
    // await cleanExtractedData(contentGrab, saveTo);
    
    // await fs.writeFile(saveTo, contentGrab)
    return contentGrab;
}

async function cleanExtractedData(content, saveTo)
{
    console.log("Starting Clean...")
    // console.log(content);
    // const data1 = (await fs.readFile(path)).toString();
    data = content.toString();
    //remove elements we dont want such as svg, path, script
    // data = data.replaceAll(">", ">\n");
    // data = data.replaceAll("</", "\n</");
    
    // TODO: make it so that it works using an array of unwanted elements, for example unwanted = ['svg', 'path'...]
        // var expression = `<${elem}.*?>(.|\n)*?<\/${elem}>`;
        // remove head tag
        expression = `<head.*?>(.|\n)*?<\/head>`;
        re = new RegExp(expression, 'g');
        data = data.replaceAll(re, "");

        // remove <footer>
        expression = `<footer.*?>(.|\n)*?<\/footer>`;
        re = new RegExp(expression, 'g');
        data = data.replaceAll(re, "\n");

        // fix body 
        expression = `<body.*?>`;
        re = new RegExp(expression, 'g');
        data = data.replaceAll(re, "<body>");
        
        // remove <link>
        expression = `<link.*?>`;
        re = new RegExp(expression, 'g');
        data = data.replaceAll(re, "\n");
        
        // remove <style>
        expression = `<style.*?>(.|\n)*?<\/style>`;
        re = new RegExp(expression, 'g');
        data = data.replaceAll(re, "\n");
        
        //remove svg
        var expression = `<svg.*?>(.|\n)*?<\/svg>`;
        var re = new RegExp(expression, 'g');
        data = data.replaceAll(re, "\n");
        
        // remove <script>
        expression = `<script.*?>(.|\n)*?<\/script>`;
        re = new RegExp(expression, 'g');
        data = data.replaceAll(re, "\n");

        
        // remove <footer>
        expression = `<noscript.*?>(.|\n)*?<\/noscript>`;
        re = new RegExp(expression, 'g');
        data = data.replaceAll(re, "\n");

        // remove <form> 
        expression = `<form.*?>(.|\n)*?<\/form>`;
        re = new RegExp(expression, 'g');
        data = data.replaceAll(re, "\n");
        

        // remove style tags
        expression = `style="(.)*?"`;
        re = new RegExp(expression, 'g');
        data = data.replaceAll(re, "");
        
        // remove onload tags
        expression = `onload="(.)*?"`;
        re = new RegExp(expression, 'g');
        data = data.replaceAll(re, "");
        
        // remove id tags
        expression = `id="(.)*?"`;
        re = new RegExp(expression, 'g');
        data = data.replaceAll(re, "");
       
        // remove testid tags
        expression = `data-testid="(.)*?"`;
        re = new RegExp(expression, 'g');
        data = data.replaceAll(re, "");

        // remove ariel-label tags
        expression = `aria-label="(.|\n)*?"`;
        re = new RegExp(expression, 'g');
        data = data.replaceAll(re, "");

        // remove comments tags
        expression = `<!--(.|\n)*?-->`;
        re = new RegExp(expression, 'g');
        data = data.replaceAll(re, "\n");

    data = data.replaceAll(">", ">\n");
    // remove excesive whitespace
    // expression = `\n(\s)+`;
    // re = new RegExp(expression, 'g');
    // data = data.replaceAll(re, "");
    // await fs.writeFile(saveTo, data)
    
    expression = `(\n)+`;
    re = new RegExp(expression, 'g');
    data = data.replaceAll(re, "\n");
    await fs.writeFile('html_files/'+saveTo+".html", data)

    console.log("Done Cleaning...")
}

async function readFile(filename) {
    try {
      const contents = (await fs.readFile(filename, 'utf-8')).toString();
  
      const arr = contents.split(/\r?\n/);
  
    //   console.log(arr); // 👉️ ['One', 'Two', 'Three', 'Four']
  
      return arr;
    } catch (err) {
      console.log(err);
      return [];
    }
  }
module.exports = { readFile, extractPage, cleanExtractedData }