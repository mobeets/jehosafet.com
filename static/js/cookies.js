function makeKey(key) {
    return key.replace(/ /g, '-');
}
function unKey(key) {
    return key.replace(/-/g, ' ');
}

function loadData(lookup){ 
    keys = Object.keys(lookup);
    console.log(keys);
    val = '<ul>';
    for (i in keys){
        key = keys[i];
        val += '<li><div class="item" id="' + makeKey(key) + '">' + key + '</div></li>'
    }
    val += '</ul>\n'
    $('#nouns').html(val);
};

function updateResult(val, swap, kind) {
    items = [];
    for (i in val[kind]){
        x = val[kind][i]['phrase'];
        if (kind == 'less'){
            act = swap ? 'more' : 'less';
        } else {
            act = swap ? 'less' : 'more';
        }
        items.push(x + ' <i>' + act + '</i>');
    }
    out = '';
    if (items.length){
        out += items.join(', ') + '.';
    }
    $('#' + kind + '-result').html(out);
}

function loadKeyData(key) {
    opt = $('#opt-text').html().toLowerCase();
    // key = event.target.id;
    $('.item').removeClass('item-selected');
    $('#' + key).addClass('item-selected');
    val = lookup[unKey(key)];

    $('#result-title').html('<h1>you should</h1>');

    swap = opt == 'less';
    updateResult(val, swap, 'less');
    updateResult(val, swap, 'more');

}

function toggleOption() {
    val = $("#opt-text").html();
    new_val = val == 'LESS' ? 'MORE' : 'LESS';
    $("#opt-text").html(new_val);
    
    item = $(".item-selected");
    if (item.length){
        key = item[0].id;
        loadKeyData(key);
    }
}

require(["cookies-data"], function(util) {
    $("#opt-text").click(toggleOption);
    loadData(lookup);
    $(".item").click(function(event) { loadKeyData(event.target.id); });
});
