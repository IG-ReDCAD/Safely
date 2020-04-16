"use strict";

const userId = $('#userid').data('userId');

$.get(`/chart.json/${userId}`, (results) => {
  const chartsContainer = $('#charts');
  for (let route of results) {
    const routeDiv = $("<div><h5>" + route.route_name + "</h5></div>");
    const canvas = $('<canvas width="1200" height="350"></canvas>');
    routeDiv.append(canvas);
    chartsContainer.append(routeDiv);

    const list_colors = ["#8B0000", "#FF0000", "#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9", "#c45850"]
    const list_cat = Object.keys(route.crimes_by_category);
    const list_sum = Object.values(route.crimes_by_category)

    new Chart(canvas, {
      type: 'doughnut',
      data: {
        labels: list_cat,
        // [results.sumcat[index][0][0], results.sumcat[index][1][0], results.sumcat[index][2][0], results.sumcat[index][3][0], results.sumcat[index][4][0]],
        datasets: [{
          label: "Number of crimes",
          backgroundColor: list_colors,
          data: list_sum
            // [results.sumcat[index][0][1],results.sumcat[index][1][1],results.sumcat[index][2][1],results.sumcat[index][3][1],results.sumcat[index][4][1]]
        }]
      },
      options: {
        title: {
          display: true,
          text: ''
        }
      }
    });
  }
});