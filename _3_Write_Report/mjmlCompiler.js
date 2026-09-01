const mjml2html = require("mjml");

let input = "";

process.stdin.on("data", chunk => {
    input += chunk;
});

process.stdin.on("end", async () => {
    try {
        const result = await mjml2html(input);
        console.log(result.html);
    } catch (error) {
        console.error(error);
        process.exit(1);
    }
});