function refreshChart(date) {
  date = date.target.value;

  d3.tsv('data/issues-by-sector.tsv')
    .then(function (rows) {
      function unpack(rows, key) {
        return rows.map(function (row) {
          return row[key]
        });
      }

      var chartData = {};
      chartData["sector"] = [];
      chartData["ticker"] = [];
      chartData["size"] = [];
      chartData["priceChange"] = [];
      chartData["prevSize"] = [];
      chartData["customdata"] = [];

      var labels = unpack(rows, 'labels');
      var parents = unpack(rows, 'parents');
      var shortnames = unpack(rows, 'shortname');
      var shortnamesRus = unpack(rows, 'shortname_rus');
      var namesRus = unpack(rows, 'name_rus');

      for (let i = 0; i <= 36; i++) {
        chartData["sector"].push(parents[i]);
        chartData["ticker"].push(labels[i]);
        chartData["size"].push(0);
        chartData["priceChange"].push(NaN);
        chartData["prevSize"].push(0);
        chartData["customdata"].push(["Moscow Exchange", labels[i], NaN, NaN, labels[i], NaN]);
      };

      if (date === new Date().toISOString().split('T')[0]) {
        var isToday = true;
        var path = `data/iss/history/engines/stock/totals/boards/MRKT/securities-${date}.json?_=' + new Date().getTime()`;
      }
      else {
        isToday = false;
        path = `data/iss/history/engines/stock/totals/boards/MRKT/securities-${date}.json`;
      }
      return $.getJSON(`${path}`)
        .then(function (moexJson) {
          if (isToday) {
            moexJson = moexJson.marketdata.data.filter(entry => entry[1] === 'TQBR')
          }
          else {
            moexJson = moexJson.securities.data
          }
          moexJson.forEach(item => {
            var ticker = item[0];
            if (RegExp('^[a-zA-Z0-9]+-RM').test(ticker))
              return;

            if (isToday) {
              var currency = '';
              var openPrice = item[9] == null ? 0 : item[9];
              var closePrice = item[12] == null ? 0 : item[12];
              var volume = item[27] == null ? 0 : item[27];
              var value = item[16] == null ? 0 : item[16];
              var numTrades = item[26] == null ? 0 : item[26];
              var marketCapDaily = item[50] == null ? 0 : item[50];
            }
            else {
              var currency = item[1];
              var openPrice = item[2] == null ? 0 : item[2];
              var closePrice = item[3] == null ? 0 : item[3];
              var volume = item[4] == null ? 0 : item[4];
              var value = item[5] == null ? 0 : item[5];
              var numTrades = item[6] == null ? 0 : item[6];
              var marketCapDaily = item[7] == null ? 0 : item[7];
            }

            if (openPrice == 0) {
              var priceChange = 0;
              var prevMarketCap = marketCapDaily;
            }
            else {
              var priceChange = 100 * (closePrice - openPrice) / openPrice;
              var prevMarketCap = marketCapDaily / (1 + priceChange * 0.01)
            }

            var sector = "Others";
            var index = labels.indexOf(ticker);
            if (index == -1) {
              sector = "Others";
              chartData["size"][labels.indexOf("Others")] = chartData["size"][labels.indexOf("Others")] + marketCapDaily;
              chartData["prevSize"][labels.indexOf("Others")] = chartData["prevSize"][labels.indexOf("Others")] + prevMarketCap;
              chartData["customdata"].push([sector, ticker, marketCapDaily, priceChange, ticker, closePrice]);
            } else {
              sector = parents[index];
              chartData["size"][labels.indexOf(sector)] = chartData["size"][labels.indexOf(sector)] + marketCapDaily;
              chartData["prevSize"][labels.indexOf(sector)] = chartData["prevSize"][labels.indexOf(sector)] + prevMarketCap;

              var name = shortnames[index];
              chartData["customdata"].push([sector, ticker, marketCapDaily, priceChange, name, closePrice]);
            };

            chartData["sector"].push(sector);
            chartData["ticker"].push(ticker);
            chartData["size"].push(marketCapDaily);
            chartData["priceChange"].push(priceChange);
            chartData["prevSize"].push(prevMarketCap);
          });

          for (let i = 1; i <= 36; i++) {
            chartData["customdata"][i][2] = chartData["size"][i];
            chartData["priceChange"][i] = 100 * (chartData["size"][i] - chartData["prevSize"][i]) / chartData["prevSize"][i];
            chartData["customdata"][i][3] = chartData["priceChange"][i];

            chartData["size"][0] = chartData["size"][0] + chartData["size"][i];
            chartData["prevSize"][0] = chartData["prevSize"][0] + chartData["prevSize"][i];
            chartData["priceChange"][0] = 100 * (chartData["size"][0] - chartData["prevSize"][0]) / chartData["prevSize"][0];
          };
          chartData["customdata"][0] = ["Moscow Exchange", "Moscow Exchange", chartData["size"][0], chartData["priceChange"][0], "Moscow Exchange", NaN];

          var texttemplate = '<b>%{label}</b><br>%{customdata[4]}<br>%{customdata[5]:,.2f} (%{customdata[3]:.2f}%)<br>Cap: ₽%{value:,.0f}';
          var hovertemplate = '<b>%{customdata[1]}</b><br>%{customdata[4]}<br>Share price: %{customdata[5]:,.4f}<br>Price change: %{customdata[3]:.2f}%<br>Cap: ₽%{customdata[2]:,.0f}<br>percentParent: %{percentParent:.2p}<br>percentRoot: %{percentRoot:.2p}<extra></extra>';

          var data = [{
            type: "treemap",
            labels: chartData["ticker"],
            level: "Moscow Exchange",
            parents: chartData["sector"],
            values: chartData["size"],
            marker: {
              colors: chartData.priceChange,
              colorscale: [[0, 'rgb(246,53,56)'], [0.5, 'rgba(65, 69, 84, 1)'], [1, 'rgb(48,204,90)']],
              cmin: -3,
              cmid: 0,
              cmax: 3,
              line: {
                width: 2,
                color: "rgb(64,68,83)"
              }
            },
            text: chartData.customdata[4],
            textinfo: "label+text+value",
            customdata: chartData.customdata,
            branchvalues: "total",
            texttemplate: texttemplate,
            hovertemplate: hovertemplate,
            pathbar: {
              visible: true,
              edgeshape: ">",
              side: "top"
            }
          }];

          var layout = {
            showlegend: false,
            autosize: true,
            margin: {
              l: 0,
              r: 0,
              t: 0,
              b: 20
            },
            paper_bgcolor: "rgb(0,0,0,0)",
            plot_bgcolor: "rgb(0,0,0,0)",
            annotations: [{
              name: 'wm',
              text: '<a style="color: grey;" href="https://ruslanbay.github.io/moex">ruslanbay.github.io/moex</a><br><a style="color: grey;" href="https://www.linkedin.com/in/ruslanbay">linkedin.com/in/ruslanbay</a><br><a style="color: grey;" href="https://github.com/ruslanbay">github.com/ruslanbay</a>',
              xref: 'paper',
              yref: 'paper',
              x: 0.03,
              y: 0.03,
              showarrow: false,
              opacity: 0.9,
              align: 'left',
              font: {
                size: 16,
                color: 'rgb(120, 108, 144)'
              }
            }]
          }

          var config = {
            responsive: true,
            displaylogo: false,
            displayModeBar: false,
            scrollZoom: true
          }
          Plotly.react('chart', data, layout, config);
        })
        .catch(error => alert("Oops! There's no data. Please select another date."));
    });
}
