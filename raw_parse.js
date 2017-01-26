let fs = require('fs')

fs.readFile('data/raw.html', "utf-8", (err, data) => {
  if (err) throw err

  let lexicon = split_lexicon(data)

  lexicon.forEach((data, index) => {
    let out;
    switch (index) {
      case 0:
        break;
      case 1:
        out = do_title(data)
        write_section(data, "00-title.html")
        break;
      case 2:
        out= do_preface(data)
        write_section(data, "01-preface.html")
        break;
      case 3:
        out = do_abbr(data)
        write_section(data, "02-abbr.html")
        break;
      case 4:
        out = do_lex(data)
        write_section(data, "03-heb_lex.html")
        break;
      case 5:
        out = do_lex(data)
        write_section(data, "04-aram_lex.html")
        break;
      case 6:
        out = do_lex(data)
        write_section(data, "05-addenda.html")
        break;
      default:
        console.log("Too many sections!")
        break;
    }
  });

});


function split_lexicon(data){
  // Splits raw.html into H1 sections
  data = data
    .split("<h1>")
  return data.map( section => {
    section = section.split("</h1>")
    return {
      title: section[0],
      content: section[1]
    }
  })

}

function write_section(obj, path){
  fs.writeFile('data/lexicon/'+ path, obj.content , err => {
    if (err) throw err;
  })
}

function cleanup(content){
  return content
    .replace(/<!--/g, "")
    .replace(/-->/g, "")
    .replace(/<p class="p">(.*)<\/p>/g, '$1')
}

function do_title(title){
  title = format_h1(title)
  title.content = title.content
    .replace(/<p class="center">(.*)<\/p>/g, "$1")

  return title

}
function do_preface(preface){
  preface = format_h1(preface)
  preface.content = preface.content
    .replace(/<p class="p">(.*)<\/p>/g, "<p>$1</p>")
  return preface
}
function do_abbr(abbr){
  abbr = format_h1(abbr)
  abbr.content = abbr.content
    .replace(/<li style="list-style-type:none">(.*)<\/li>/g, "<li>$1</li>")
    .replace(/<p class="p">(.*)<\/p>/g, "<p>$1</p>")
  return abbr
}
function do_lex(lex){
  lex.content = lex.content
    .replace(/<!--(.*?)-->/g, "$1")
    .replace(/<p class="p">(.*)<\/p>/g, "$1")
  return lex
}
function do_lex(lex){
  lex.content = lex.content
    .replace(/<!--(.*?)-->/g, "$1")
    .replace(/<p class="p">(.*)<\/p>/g, "$1")
  return lex
}
function do_addenda(addenda){
  return addenda
}

function format_h1(section){
  section.content = "<h1>" + section.title + "</h1>\n" + section.content
  return section
}
