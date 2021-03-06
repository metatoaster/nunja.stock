// the lines cannot be broken due to strict requirement that the content
// must also be parsed as JSON from within Python.
/* eslint max-len: "off" */

var exports = {
    "null rendering":
    [{"mainEntity": {
        "colnames": [],
        "rownames": [],
        "rows": [],
    }}, [
        "<div data-nunja=\"nunja.stock.molds/grid\">",
        "<table class=\"\">",
        "  <thead>",
        "  </thead>",
        "  <tbody>",
        "  </tbody>",
        "</table>",
        "</div>"
    ]],

    "column rendering":
    [{"mainEntity": {
        "colnames": ["Jan", "Feb", "Mar", "Apr", "May"],
        "rownames": [],
        "rows": [["31", "28", "31", "30", "31"]]
    }}, [
        "<div data-nunja=\"nunja.stock.molds/grid\">",
        "<table class=\"\">",
        "  <thead>",
        "    <tr class=\"\">",
        "      <th>Jan</th><th>Feb</th><th>Mar</th><th>Apr</th><th>May</th>",
        "    </tr>",
        "  </thead>",
        "  <tbody>",
        "    <tr class=\"\">",
        "      <td>31</td>",
        "      <td>28</td>",
        "      <td>31</td>",
        "      <td>30</td>",
        "      <td>31</td>",
        "    </tr>",
        "  </tbody>",
        "</table>",
        "</div>"
    ]],

    "column rendering with header row":
    [{"mainEntity": {
        "colnames": ["Jan", "Feb", "Mar", "Apr", "May"],
        "rownames": ["Days"],
        "rows": [["31", "28", "31", "30", "31"]]
    }}, [
        "<div data-nunja=\"nunja.stock.molds/grid\">",
        "<table class=\"\">",
        "  <thead>",
        "    <tr class=\"\">",
        "      <th></th><th>Jan</th><th>Feb</th><th>Mar</th><th>Apr</th><th>May</th>",
        "    </tr>",
        "  </thead>",
        "  <tbody>",
        "    <tr class=\"\">",
        "      <th>Days</th>",
        "      <td>31</td>",
        "      <td>28</td>",
        "      <td>31</td>",
        "      <td>30</td>",
        "      <td>31</td>",
        "    </tr>",
        "  </tbody>",
        "</table>",
        "</div>"
    ]],

    "row rendering":
    [{"mainEntity": {
        "colnames": [],
        "rownames": ["Jan", "Feb", "Mar", "Apr", "May"],
        "rows": [["31"], ["28"], ["31"], ["30"], ["31"]]
    }}, [
        "<div data-nunja=\"nunja.stock.molds/grid\">",
        "<table class=\"\">",
        "  <thead>",
        "  </thead>",
        "  <tbody>",
        "    <tr class=\"\">",
        "      <th>Jan</th>",
        "      <td>31</td>",
        "    </tr>",
        "    <tr class=\"\">",
        "      <th>Feb</th>",
        "      <td>28</td>",
        "    </tr>",
        "    <tr class=\"\">",
        "      <th>Mar</th>",
        "      <td>31</td>",
        "    </tr>",
        "    <tr class=\"\">",
        "      <th>Apr</th>",
        "      <td>30</td>",
        "    </tr>",
        "    <tr class=\"\">",
        "      <th>May</th>",
        "      <td>31</td>",
        "    </tr>",
        "  </tbody>",
        "</table>",
        "</div>"
    ]],

    "row rendering with header row with first header cell":
    [{"mainEntity": {
        "first_header_cell": "Month",
        "colnames": ["Days"],
        "rownames": ["Jan", "Feb", "Mar", "Apr", "May"],
        "rows": [["31"], ["28"], ["31"], ["30"], ["31"]]
    }}, [
        "<div data-nunja=\"nunja.stock.molds/grid\">",
        "<table class=\"\">",
        "  <thead>",
        "    <tr class=\"\">",
        "      <th>Month</th><th>Days</th>",
        "    </tr>",
        "  </thead>",
        "  <tbody>",
        "    <tr class=\"\">",
        "      <th>Jan</th>",
        "      <td>31</td>",
        "    </tr>",
        "    <tr class=\"\">",
        "      <th>Feb</th>",
        "      <td>28</td>",
        "    </tr>",
        "    <tr class=\"\">",
        "      <th>Mar</th>",
        "      <td>31</td>",
        "    </tr>",
        "    <tr class=\"\">",
        "      <th>Apr</th>",
        "      <td>30</td>",
        "    </tr>",
        "    <tr class=\"\">",
        "      <th>May</th>",
        "      <td>31</td>",
        "    </tr>",
        "  </tbody>",
        "</table>",
        "</div>"
    ]],

    "incomplete row names":
    [{"mainEntity": {
        "colnames": ["Days"],
        "rownames": ["Jan", "Feb"],
        "rows": [["31"], ["28"], ["31"], ["30"], ["31"]]
    }}, [
        "<div data-nunja=\"nunja.stock.molds/grid\">",
        "<table class=\"\">",
        "  <thead>",
        "    <tr class=\"\">",
        "      <th></th><th>Days</th>",
        "    </tr>",
        "  </thead>",
        "  <tbody>",
        "    <tr class=\"\">",
        "      <th>Jan</th>",
        "      <td>31</td>",
        "    </tr>",
        "    <tr class=\"\">",
        "      <th>Feb</th>",
        "      <td>28</td>",
        "    </tr>",
        "    <tr class=\"\">",
        "      <th></th>",
        "      <td>31</td>",
        "    </tr>",
        "    <tr class=\"\">",
        "      <th></th>",
        "      <td>30</td>",
        "    </tr>",
        "    <tr class=\"\">",
        "      <th></th>",
        "      <td>31</td>",
        "    </tr>",
        "  </tbody>",
        "</table>",
        "</div>"
    ]],

    "multi row/col":
    [{"mainEntity": {
        "first_header_cell": "x",
        "colnames": ["1", "2", "3"],
        "rownames": ["1", "2", "3"],
        "rows": [[1, 2, 3], [2, 4, 6], [3, 6, 9]],
    }}, [
        "<div data-nunja=\"nunja.stock.molds/grid\">",
        "<table class=\"\">",
        "  <thead>",
        "    <tr class=\"\">",
        "      <th>x</th><th>1</th><th>2</th><th>3</th>",
        "    </tr>",
        "  </thead>",
        "  <tbody>",
        "    <tr class=\"\">",
        "      <th>1</th>",
        "      <td>1</td>",
        "      <td>2</td>",
        "      <td>3</td>",
        "    </tr>",
        "    <tr class=\"\">",
        "      <th>2</th>",
        "      <td>2</td>",
        "      <td>4</td>",
        "      <td>6</td>",
        "    </tr>",
        "    <tr class=\"\">",
        "      <th>3</th>",
        "      <td>3</td>",
        "      <td>6</td>",
        "      <td>9</td>",
        "    </tr>",
        "  </tbody>",
        "</table>",
        "</div>"
    ]],

    "multi row/col with meta css":
    [{"mainEntity": {
        "first_header_cell": "x",
        "colnames": ["1", "2", "3"],
        "rownames": ["1", "2", "3"],
        "rows": [[1, 2, 3], [2, 4, 6], [3, 6, 9]]
    }, "meta": {
        "css_class": {
            "table": "table",
            "table.thead.tr": "main header",
            "table.tbody.tr": "body row"
        }
    }}, [
        "<div data-nunja=\"nunja.stock.molds/grid\">",
        "<table class=\"table\">",
        "  <thead>",
        "    <tr class=\"main header\">",
        "      <th>x</th><th>1</th><th>2</th><th>3</th>",
        "    </tr>",
        "  </thead>",
        "  <tbody>",
        "    <tr class=\"body row\">",
        "      <th>1</th>",
        "      <td>1</td>",
        "      <td>2</td>",
        "      <td>3</td>",
        "    </tr>",
        "    <tr class=\"body row\">",
        "      <th>2</th>",
        "      <td>2</td>",
        "      <td>4</td>",
        "      <td>6</td>",
        "    </tr>",
        "    <tr class=\"body row\">",
        "      <th>3</th>",
        "      <td>3</td>",
        "      <td>6</td>",
        "      <td>9</td>",
        "    </tr>",
        "  </tbody>",
        "</table>",
        "</div>"
    ]]

};

// requirejs export shim
define([], function() {
    return exports;
});
