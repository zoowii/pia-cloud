$(function () {
    var database = null;

    function isSelectResult(data) {
        return _.isArray(data) && data.length > 0 && !_.isString(data[0]);
    }

    function isInsertResult(data) {
        if (_.isArray(data) && data.length > 0 && _.isString(data[0])) {
            return true;
        } else {
            return false;
        }
    }

    var $resultTable = $(".result-window table");
    $(".execute-sql-btn").click(function () {
        var sql = $("[name=sql-field]").val();
        $.post(sqlUrl, {
            sql: sql.trim(),
            database: database
        }, function (json) {
            if (json.success) {
                database = json.data['database'];
                console.log(json.data);
                var result = json.data.result;
                if (isSelectResult(result)) {
                    $resultTable.find('thead').html('');
                    $resultTable.find('tbody').html('');
                    var firstRow = result[0];
                    var heads = [];
                    for (var key in firstRow) {
                        heads.push(key);
                    }
                    for (var i = 0; i < heads.length; ++i) {
                        var $th = $("<th></th>");
                        $th.text(heads[i]);
                        $resultTable.find('thead').append($th);
                    }
                    _.each(result, function (row) {
                        var $tr = $("<tr></tr>");
                        for (var i = 0; i < heads.length; ++i) {
                            var $td = $("<td></td>");
                            if (row[heads[i]] !== undefined) {
                                $td.html('' + row[heads[i]]);
                            }
                            $tr.append($td);
                        }
                        $resultTable.find('tbody').append($tr);
                    });
                } else if (isInsertResult(result)) {
                    $resultTable.find('thead').html('');
                    $resultTable.find('tbody').html('');
                    $resultTable.find('thead').append($("<th>id</th>"));
                    _.each(result, function (row) {
                        var $tr = $("<tr></tr>");
                        var $td = $("<td></td>");
                        $td.html(row);
                        $tr.append($td);
                        $resultTable.find('tbody').append($tr);
                    });
                } else {
                    alert(JSON.stringify(result));
                }
            }
        }, 'json');
    });
});