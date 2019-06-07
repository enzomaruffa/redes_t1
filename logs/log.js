let terminals = document.getElementsByClassName('quarter')
console.log('terminals' + terminals)
for (var k = 0; k < terminals.length; k++) {
    terminals[k].addEventListener('scroll', function(e) {
        console.log('aaaa')
        for (var j = 0; j < terminals.length; j++) {
            terminals[j].scrollTop = e.target.scrollTop;
        }
    });
}
