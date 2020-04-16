"use strict";

function changeNeigh() {
    // Clear #crime-picker and div-chart
    $('#crime-picker').empty();
    $('#div-chart').empty();
    let iframe = $('#mapframe');
    iframe.attr('src', "/mapNeigh");
    const formContainer = $('#neighborhoods');
    const selectBox = document.getElementById("neighs");
    const selectedValue = selectBox.options[selectBox.selectedIndex].value;
    $.post('/selectNeigh', {
        "neigh_id": selectedValue
    }, (res) => {
        console.log(res)
        keys = Object.keys(res)
        const divcat = $('<div id="div-cat"></div>')
        const label = $("<br><label> </label>")
        divcat.append(label);
        let selectcat = $('<select id="cat" class="browser-default custom-select" name="cat" onchange="changeCat();">');
        divcat.append(selectcat);
        $('#crime-picker').append(divcat);
        const cat1 = $("<option selected>Select a category </option>");
        selectcat.append(cat1);
        for (let i of keys) {
            const cat = $("<option value=" + i + ">" + i + "</option>");
            selectcat.append(cat);
        }
    });
}

function changeCat() {
    const category = document.getElementById("cat");
    const selectedcat = category.options[category.selectedIndex].value;
    const namecat = $("#cat option:selected").html();
    console.log(selectedcat)
    console.log("namecat" + namecat)
    const selectBox = document.getElementById("neighs");
    const selectedValue = selectBox.options[selectBox.selectedIndex].value;
    $.post('/selectcat', {
        "neigh_id": selectedValue
        , "cat_name": namecat
    }, (res) => {
        console.log(res)
        const list_x = Object.keys(res);
        const list_y = Object.values(res);
        console.log(list_x)
        console.log(list_y)
        const chartDiv = $('#div-chart');
        const canvas = $('<canvas style="display: block; width: 509px; height: 254px;" width="509" height="254" class="chartjs-render-monitor"></canvas>');
        chartDiv.append(canvas);
        const MONTHS = ['January/2018', 'February/2018', 'March/2018', 'April/2018', 'May/2018', 'June/2018', 'July/2018', 'August/2018', 'September/2018', 'October/2018', 'November/2018', 'December/2018', 'January/2019', 'February/2019', 'March/2019', 'April/2019', 'May/2019', 'June/2019', 'July/2019', 'August/2019', 'September/2019', 'October/2019', 'November/2019', 'December/2019'];
        let config = {
            type: 'line'
            , data: {
                labels: MONTHS
                , datasets: [{
                    label: 'Crime dataset of ' + namecat
                    , backgroundColor: '#FFEBCD'
                    , borderColor: '#A52A2A'
                    , data: list_y
                , }]
            }
            , options: {
                responsive: true
                , title: {
                    display: true
                    , text: 'Number of crimes per month'
                }
                , tooltips: {
                    mode: 'index'
                    , intersect: false
                , }
                , hover: {
                    mode: 'nearest'
                    , intersect: true
                }
                , scales: {
                    xAxes: [{
                        display: true
                        , scaleLabel: {
                            display: true
                            , labelString: 'Months'
                        }
                    }]
                    , yAxes: [{
                        display: true
                        , scaleLabel: {
                            display: true
                            , labelString: 'Number of crimes'
                        }
                    }]
                }
            }
        };
        new Chart(canvas, config);
    });
    let iframe = $('#mapframe');
    iframe.attr('src', "/dropmarkers");
}
