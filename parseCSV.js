// 不支持转义
function parseCSV(csv, dtype) {
    var lines = csv.split('\n');
    var keys = lines[0].split(',');
    return lines.slice(1).map(function (line) {
        var values = line.split(',');
        var o = {};
        keys.forEach(function (key, index) {
            var type = dtype ? dtype[key] : undefined;
            o[key] = type ? type(values[index]) : values[index];
        });
        return o;
    });
}