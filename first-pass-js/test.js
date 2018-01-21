let fs = require('fs')
let pd = require('pretty-data').pd
let Entities = require('html-entities').XmlEntities;

fs.readFile('test.html', "utf-8", (err, data) => {
    if (err) throw err

    console.log(pd.xmlmin(data))

})