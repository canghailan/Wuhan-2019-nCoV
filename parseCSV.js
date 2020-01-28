// 不支持转义
function parseCSV(csv) {
    var lines = csv.split('\n');
    var keys = lines[0].split(',');
    return lines.slice(1).map(function (line) {
        var values = line.split(',');
        var o = {};
        keys.forEach(function (key, index) {
            o[key] = values[index];
        });
        return o;
    });
}