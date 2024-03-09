let availableKeywords = [
    'Restaurants',
    'Bars',
    'Cafes',
    'Museums',
    'Galleries',
    'Aquariums',
    'Churches',
    'Cathedrals',
    'Natural attractions',
    'Monuments',
];

const resultBox = document.querySelector(".result-box");
const inputBox = document.getElementById("input-box");

inputBox.onkeyup = function() {
    let result = [];
    let input = inputBox.value.toLowerCase();
    if (input.length > 0) {
        result = availableKeywords.filter((keyword) => {
            return keyword.toLowerCase().includes(input);
        });
        console.log(result);
        display(result);

        if (!result.length) {
            resultBox.innerHTML = "";
        }
    }    
}

function display(result){
    const content = result.map((list)=>{
        return "<li onclick=selectInput(this)>" + list + "</li>";
    });

    resultBox.innerHTML = "<ul>" + content.join('') + "</ul>";
}

function selectInput(list){
    inputBox.value = list.innerHTML;
    resultBox.innerHTML = "";
}
