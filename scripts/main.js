// Prevent the default context menu from appearing on right-click
const chartDiv = document.getElementById("chart");
chartDiv.addEventListener("contextmenu", (event) => {
    event.preventDefault();
});

// Share link
const shareLink = document.getElementById("share");
const thisTitle = document.title;
shareLink.addEventListener("click", handleShareClick);

function handleShareClick(event) {
  if (navigator.share) {
    navigator.share({
      title: thisTitle,
      url: url
    })
    .catch(console.error);
  } else {
    alert("Web Share API is not supported");
  }
}

// Install PWA
let installPrompt = null;
const installLink = document.getElementById("install");
window.addEventListener("beforeinstallprompt", handleBeforeInstallPrompt);
window.addEventListener("appinstalled", handleAppInstalled);
installLink.addEventListener("click", handleInstallClick);

function disableInAppInstallPrompt() {
  installPrompt = null;
  installLink.setAttribute("hidden", "");
}

function handleBeforeInstallPrompt(event) {
  event.prompt();
  installPrompt = event;
  installLink.removeAttribute("hidden");
}

function handleAppInstalled() {
  disableInAppInstallPrompt();
}

async function handleInstallClick() {
  if (!installPrompt) {
    return;
  }
  const result = await installPrompt.prompt();
  console.log(`Install prompt was: ${result.outcome}`);
  disableInAppInstallPrompt();
}


// Apply filter.csv
const inputFileLabel = document.getElementById("inputFileLabel");
const chooseFileButton = document.getElementById("inputFile");
chooseFileButton.addEventListener("change", function(event) {
  processCsv(event);
  chooseFileButton.value = null;
});

function processCsv(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      const csvContent = e.target.result;
      localStorage.setItem('filterCsv', csvContent);
      refreshChart();
    };
    reader.readAsText(file);
  }
}


// Searchbox
const searchbox = document.getElementById("searchbox");
searchbox.addEventListener("keypress", handleEnterKey);

function handleEnterKey(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    const inputValue = this.value.trim().toLowerCase();
    if (inputValue) {
      selectTreemapItemByLabel(inputValue);
      this.value = '';
    }
  }
}

/*
// Searchbox autocomplete
function getTicketList() {
  // TODO: вместо tsv-файла использовать выборку элементов с чарта как в 
  // function selectTreemapItemByLabel(label) {
  const url = `data/securities-by-sector/moex.tsv?_=${new Date().toISOString().split('T')[0]}`;
  const columnIndex = 1;
  const tickerList = [];
  fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error("Something's wrong");
      }
      return response.text();
    })
    .then(data => {
      const lines = data.split('\n');
      
      for (let line of lines) {
        const values = line.split('\t');
        if (values.length > columnIndex) {
          tickerList.push(values[columnIndex].trim());
        }
      }
      // document.getElementById('output').innerText = tickerList.join('\n');
      // const inputValue = this.value.trim().toLowerCase();
    })
    .catch(error => {
      console.error('Error:', error);
    });
    
    return tickerList;
}

const suggestions = getTicketList();

function autocomplete(inputElement, suggestions) {
  inputElement.addEventListener("input", function () {
    const value = this.value;
    closeAllLists();
    if (!value) return false;

    const suggestionList = document.createElement("div");
    suggestionList.setAttribute("class", "autocomplete-items");
    this.parentNode.appendChild(suggestionList);

    suggestions.forEach((item) => {
      if (item.substr(0, value.length).toUpperCase() === value.toUpperCase()) {
        const suggestionItem = document.createElement("div");
        suggestionItem.innerHTML = "<strong>" + item.substr(0, value.length) + "</strong>";
        suggestionItem.innerHTML += item.substr(value.length);
        suggestionItem.addEventListener("click", function () {
          inputElement.value = item;
          closeAllLists();
          if (item) {
            selectTreemapItemByLabel(item);
            this.value = '';
          }
        });
        suggestionList.appendChild(suggestionItem);
      }
    });
  });

  function closeAllLists() {
    const items = document.getElementsByClassName("autocomplete-items");
    while (items[0]) {
      items[0].parentNode.removeChild(items[0]);
    }
  }

  document.addEventListener("click", function (e) {
    closeAllLists(e.target);
  });
}

autocomplete(searchbox, suggestions);
*/

// Update URL
const url = new URL(window.location.href);
const urlDate = url.searchParams.get("date");
const urlChartType = url.searchParams.get("chartType");
const urlCurrency = url.searchParams.get("currency");
const urlDataType = url.searchParams.get("dataType");

let date = urlDate ? new Date(`${urlDate}T13:00:00`) : new Date();

if (date.getUTCHours() < 8) {
  date.setDate(date.getUTCDate() - 1);
}

while (date.getDay() === 0 || date.getDay() === 6) {
  date.setDate(date.getUTCDate() - 1);
}
var formattedDate = date.toISOString().split('T')[0];
document.getElementById("dateInput").value = formattedDate;
document.getElementById("dateInput").max = new Date().toISOString().split('T')[0];

const dateInput = document.getElementById("dateInput");
if (urlDate) { urlDate.value = urlDate };

const chartTypeInput = document.getElementById("chartType");
if (urlChartType && ["treemap", "history", "listings"].includes(urlChartType)) { chartTypeInput.value = urlChartType };

const currency = document.getElementById("currencySelector");
if (urlCurrency && ["USD", "EUR", "CNY", "RUB"].includes(urlCurrency)) { currency.value = urlCurrency };

const dataTypeInput = document.getElementById("dataType");
if (urlDataType && ["marketcap", "value", "trades"].includes(urlDataType)) { dataTypeInput.value = urlDataType };

chartTypeInput.addEventListener("change", refreshChart);
currency.addEventListener("change", refreshChart);
dataTypeInput.addEventListener("change", refreshChart);
dateInput.addEventListener("change", refreshChart);


function toggleInput() {
  const chartTypeValue = document.getElementById("chartType").value;
  const dataTypeValue = document.getElementById("dataType").value;
  const erasefilterLink = document.getElementById("erasefilter");
  
  url.searchParams.set('currency', currency.value);
  url.searchParams.set('chartType', chartTypeValue);
  url.searchParams.set('dataType', dataTypeValue);
  url.searchParams.set('date', dateInput.value);
  
  switch (chartTypeValue) {
    case "treemap":
      currency.disabled = false;
      dataType.disabled = false;
      dateInput.disabled = false;
      searchbox.disabled = false;
      break;
    case "history":
      dataType.disabled = false;
      dateInput.disabled = true;
      searchbox.disabled = true;
      inputFileLabel.setAttribute("hidden", "");
      erasefilterLink.setAttribute("hidden", "");
      if (dataTypeValue == 'trades' ) {
        currency.disabled = true;
      }
      else {
        currency.disabled = false;
      }
      url.searchParams.delete('date');
      break;
    case "listings":
      currency.disabled = true;
      dataType.disabled = true;
      dateInput.disabled = true;
      searchbox.disabled = true;
      inputFileLabel.setAttribute("hidden", "");
      erasefilterLink.setAttribute("hidden", "");
      url.searchParams.delete('date');
      break;
  }
  history.replaceState(null, '', url);
};

function selectTreemapItemByLabel(label) {
  label = label.toLowerCase();
  const chartDiv = document.getElementById('chart');

  var boxes = chartDiv.querySelectorAll('g.slice.cursor-pointer');
  let skipItems = 18;
  // switch (dataTypeValue) {
  //   case "marketcap":
  //     skipItems = 18;
  //     break;
  //   case "value":
  //     skipItems = 18;
  //     break;
  //   case "trades":
  //     skipItems = 18;
  //     break;
  // }
  for (var i = skipItems; i < boxes.length; i++) {
    var box = boxes[i];
    if (box.innerHTML.toLowerCase().includes(`<b>${label}</b>`)) {
      box.dispatchEvent(new MouseEvent('click'));
      break;
    }
  }
};

async function getCurrencyRates(currencyType) {
  const startDate = '2011-12-19';
  const response = await fetch(`data/FIXME${currencyType}.csv?_=${new Date().toISOString().split('T')[0]}`);
  const textResponse = await response.text();
  const data = textResponse.split('\n').map(row => row.split(','));

  const currencyRates = {};
  data.forEach(row => {
    const [Date, , , , Close] = row;
    if (Date >= startDate) {
      currencyRates[Date] = Number(Close);
    }
  });
  return currencyRates;
}

async function getCurrencyRateByDate(date) {
  const currencyType = document.getElementById('currencySelector').value;
  const currencyRates = await getCurrencyRates(currencyType);
  
  let rate = currencyRates[date];
  let d = new Date(date);
  while (typeof rate == 'undefined') {
    d.setDate(d.getUTCDate() - 1);
    let prevDate = d.toISOString().split('T')[0];
    rate = currencyRates[prevDate];
  }
  
  return rate;
}

async function prepHistogramData() {
  const currencyType = document.getElementById('currencySelector').value;
  try {
    const startDate = '2011-12-19';

    let response = await fetch(`data/securities-by-sector/moex.tsv?_=${new Date().toISOString().split('T')[0]}`);
    response = await response.text();
    let data = response.split('\n')
      .slice(1, 32)
      .map(row => row.split('\t'));
    let traceColors = {};
    data.forEach(row => {
      const [, label, , , , , , traceColor] = row;
      traceColors[label] = traceColor;
    });

    const currencyRates = await getCurrencyRates(currencyType);
    const oneOverY = Object.values(currencyRates);
    let chartData = {};
    if (!chartData[currencyType]) {
      chartData[currencyType] = {
        name: currencyType,
        customdata: oneOverY,
        type: "scatter",
        mode: "lines",
        yaxis: "y2",
        hoverinfo: "all",
        hovertemplate: "%{x|%x}<br>%{customdata:,.2f}<br>RUB per %{fullData.name}<extra></extra>",
        x: Object.keys(currencyRates),
        y: Object.values(currencyRates).map(y => y > 0 ? 1 / y : null)
      };
    }

    response = await fetch(`https://raw.githubusercontent.com/datasets/oil-prices/refs/heads/main/data/brent-daily.csv`);
    response = await response.text();
    data = response.split('\n')
      .map(row => row.split(','));
    const brentRates = {};
    data.forEach(row => {
      const [Date, Close] = row;
      if (Date >= startDate) {
        brentRates[Date] = Number(Close);
      }
    });

    if (!chartData['brent']) {
      chartData['brent'] = {
        name: 'Brent',
        type: "line",
        mode: "lines",
        yaxis: "y3",
        hoverinfo: "all",
        hovertemplate: "%{x|%x}<br>%{y:,.2f}<br>USD per %{fullData.name}<extra></extra>",
        x: Object.keys(brentRates),
        y: Object.values(brentRates)
      };
    }

    response = await fetch(`data/securities-by-sector/moex.tsv?_=${new Date().toISOString().split('T')[0]}`);
    response = await response.text();
    data = response.split('\n')
      .slice(1)
      .map(row => row.replace(/\r/g, '').split('\t'))
      .filter(row => row.some(cell => cell));

    data.forEach(row => {
      let y;
      const [date, marketValue, marketTrades, marketCap, traceName] = row;

      const dataTypeValue = document.getElementById('dataType').value;
      // const traceNameExcludeList = ['cb_bond', 'corporate_bond', 'etf_ppif', 'euro_bond', 'exchange_bond', 'exchange_ppif',
      //                               'Foreign Companies', 'ifi_bond', 'interval_ppif', 'municipal_bond', 'ofz_bond',
      //                               'private_ppif', 'public_ppif', 'state_bond', 'stock_mortgage', 'subfederal_bond'];
      const traceNameExcludeList = ['Foreign Companies'];

      switch(dataTypeValue){
        case "marketcap":
          y = parseFloat(marketCap);
          if (traceNameExcludeList.includes(traceName)) {
            return;
          }
          break;
        case "value":
          y = parseFloat(marketValue);
          break;
        case "trades":
          y = parseFloat(marketTrades);
          break;
      }

      if (!chartData[traceName]) {
        chartData[traceName] = {
          name: traceName,
          type: "scatter",
          mode: "lines",
          stackgroup: "one",
          connectgaps: true,
          hoverinfo: "all",
          hovertemplate: "%{x|%x}<br>%{y:,.0f}<br>%{fullData.name}<extra></extra>",
          marker: {
            color: traceColors[traceName]
          },
          x: [],
          y: []
        };
      }

      if (currencyType !== 'RUB' && (dataTypeValue == 'marketcap' || dataTypeValue == 'value')) {
        var rate = currencyRates[date];
        var d = new Date(date);
        while (typeof rate == 'undefined') {
          d.setDate(d.getUTCDate() - 1);
          let prevDate = d.toISOString().split('T')[0];
          rate = currencyRates[prevDate];
        }
        y = y / rate;
      }

      chartData[traceName].x.push(date);
      chartData[traceName].y.push(y);
    }); 

    const jsonChartData = Object.values(chartData);
    const filteredData = jsonChartData.filter(trace => {
        return trace.y.some(v => v !== null && v !== 0 && !isNaN(v));
    });

    return filteredData;

  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;
  }
};

function unpack(rows, keyIndex) {
  const headers = rows[0];
  const key = headers.indexOf(keyIndex);

  if (key === -1) {
    throw new Error(`Key "${keyIndex}" not found in headers.`);
  }

  return rows.slice(1).map(function (row) {
    return row[key];
  });
}

async function applyFilter(csv) {
  let data = csv.split('\n')
    .map(row => row.replace(/\r/g, '').split(','))
    .filter(row => row.some(cell => cell));
  const filterCsv = {
    ticker: [],
    // date: [],
    // price: [],
    // ammount: [],
    // operation: [],
  };
  data.forEach(row => {
    const [ticker, date, price, ammount, operation] = row;
    filterCsv["ticker"].push(ticker);
    // filterCsv["date"].push(date);
    // filterCsv["price"].push(price);
    // filterCsv["ammount"].push(ammount);
    // filterCsv["operation"].push(operation);
  });
  return filterCsv;
}

async function prepTreemapData() {
  let tickerList;
  const localFilterCsv = localStorage.getItem('filterCsv');
  const erasefilterLink = document.getElementById('erasefilter');
  if (localFilterCsv !== undefined && localFilterCsv !== null) {
    tickerList = await applyFilter(localFilterCsv);
    inputFileLabel.setAttribute("hidden", "");
    erasefilterLink.removeAttribute("hidden");
  }
  else {
    localStorage.removeItem('filterCsv');
    inputFileLabel.removeAttribute("hidden");
    erasefilterLink.setAttribute("hidden", "");
  }

  const currencyType = document.getElementById('currencySelector').value;
  const dataType = document.getElementById('dataType').value;
  const date = document.getElementById('dateInput').value;
  const currencyRates = await getCurrencyRates(currencyType);

  let rate = 1
  if (currencyType != 'RUB') {
    rate = await getCurrencyRateByDate(date);
  }

  const rows = await fetch(`data/securities-by-sector/moex.tsv?_=${new Date().toISOString().split('T')[0]}`)
    .then(response => response.text())
    .then(text => {
      return text.split('\n').map(row => row.split('\t'));
    });
    let chartData = {
      sector: [],
      ticker: [],
      size: [],
      priceChange: [],
      cap: [],
      prevCap: [],
      customdata: []
    };

    let labels = unpack(rows, 'labels');
    let parents = unpack(rows, 'parents');
    let shortnames = unpack(rows, 'shortname');
    // let shortnamesRus = unpack(rows, 'shortname_rus');
    // let namesRus = unpack(rows, 'name_rus');

    for (let i = 0; i <= 30; i++) {
      chartData["sector"].push(parents[i]);
      chartData["ticker"].push(labels[i]);
      chartData["size"].push(0);
      chartData["priceChange"].push(NaN);
      chartData["cap"].push(0);
      chartData["prevCap"].push(0);
      chartData["customdata"].push(["Moscow Exchange", labels[i], NaN, NaN, labels[i], NaN, NaN, NaN]);
    }

    let path = `data/${date}/moex.json`.replace(/-/g, '/');

    if (date === new Date().toISOString().split('T')[0]) {
      path = path + `?_=${new Date().getTime()}`;
    }

    let moexJson = await fetch(path)
      .then(response => response.json());

    let isToday = false;

    if (moexJson.marketdata) {
      moexJson = moexJson.marketdata.data.filter(entry => entry[1] === 'TQBR');
      isToday = true;
    }
    else {
      moexJson = moexJson.securities.data
      isToday = false;
    }
    moexJson.forEach(item => {
      let ticker = item[0];

      let currency, openPrice, closePrice, volume, value, numTrades, marketCapDaily;
      
      if (tickerList && !tickerList["ticker"].includes(ticker)) {
        return;
      }
      
      if (isToday) {
        currency = '';
        openPrice = item[9] == null ? 0 : item[9];
        closePrice = item[12] == null ? 0 : item[12];
        volume = item[27] == null ? 0 : item[27];
        value = item[28] == null ? 0 : item[28];
        numTrades = item[26] == null ? 0 : item[26];
        marketCapDaily = item[50] == null ? 0 : item[50];
      }
      else {
        currency = item[1];
        openPrice = item[2] == null ? 0 : item[2];
        closePrice = item[3] == null ? 0 : item[3];
        volume = item[4] == null ? 0 : item[4];
        value = item[5] == null ? 0 : item[5];
        numTrades = item[6] == null ? 0 : item[6];
        marketCapDaily = item[7] == null ? 0 : item[7];
      }

      value = value / rate;
      marketCapDaily = marketCapDaily / rate;

      let priceChange, prevMarketCap;

      if (openPrice === 0) {
        priceChange = 0;
        prevMarketCap = marketCapDaily;
      }
      else {
        priceChange = (100 * (closePrice - openPrice)) / openPrice;
        prevMarketCap = marketCapDaily / (1 + priceChange * 0.01);
      }

      let sizeValue;

      switch(dataType) {
        case "marketcap":
          sizeValue = marketCapDaily;
          break;
        case "value":
          sizeValue = value;
          break;
        case "trades":
          sizeValue = numTrades;
          break;
      }

      let sector;
      let index = labels.indexOf(ticker);
      if (index === -1) {
        sector = "Others";
        sectorIndex = labels.indexOf(sector);
        chartData["size"][sectorIndex] = chartData["size"][sectorIndex] + sizeValue;
        chartData["cap"][sectorIndex] = chartData["cap"][sectorIndex] + marketCapDaily;
        chartData["prevCap"][sectorIndex] = chartData["prevCap"][sectorIndex] + prevMarketCap;
        chartData["customdata"].push([sector, ticker, marketCapDaily, priceChange, ticker, closePrice, value, numTrades]);
      } else {
        sector = parents[index];
        if (sector === "Foreign Companies") {
          return;
        }
        sectorIndex = labels.indexOf(sector);
        chartData["size"][sectorIndex] = chartData["size"][sectorIndex] + sizeValue;
        chartData["cap"][sectorIndex] = chartData["cap"][sectorIndex] + marketCapDaily;
        chartData["prevCap"][sectorIndex] = chartData["prevCap"][sectorIndex] + prevMarketCap;
      
        let name = shortnames[index];
        chartData["customdata"].push([sector, ticker, marketCapDaily, priceChange, name, closePrice, value, numTrades]);
      }
          
      chartData["sector"].push(sector);
      chartData["ticker"].push(ticker);
      chartData["size"].push(sizeValue);
      chartData["priceChange"].push(priceChange);
      chartData["cap"].push(marketCapDaily);
      chartData["prevCap"].push(prevMarketCap);
    });

    for (let i=1; i <= 30; i++) {
      chartData["customdata"][i][2] = chartData["cap"][i];
      chartData["priceChange"][i] = (100 * (chartData["cap"][i] - chartData["prevCap"][i])) / chartData["prevCap"][i];
      chartData["customdata"][i][3] = chartData["priceChange"][i];

      chartData["size"][0] = chartData["size"][0] + chartData["size"][i];
      chartData["cap"][0] = chartData["cap"][0] + chartData["cap"][i];
      chartData["prevCap"][0] = chartData["prevCap"][0] + chartData["prevCap"][i];
      chartData["priceChange"][0] = (100 * (chartData["cap"][0] - chartData["prevCap"][0])) / chartData["prevCap"][0];
    }
    chartData["customdata"][0] = ["Moscow Exchange", "Moscow Exchange", chartData["cap"][0], chartData["priceChange"][0], "Moscow Exchange", NaN, NaN, NaN];
    return chartData;
}

function refreshTreemap() {
  toggleInput();
  prepTreemapData()
    .then(function (chartData) {
      const texttemplate = `<b>%{label}</b><br>
%{customdata[4]}<br>
%{customdata[5]:,.2f} (%{customdata[3]:.2f}%)<br>
C: %{customdata[2]:,.0f}<br>
V: %{customdata[6]:,.0f}<br>
T: %{customdata[7]:,.0f}`;
      const hovertemplate = `<b>%{customdata[1]}</b><br>
%{customdata[4]}<br>
Share price: %{customdata[5]:,.4f}<br>
Price change: %{customdata[3]:.2f}%<br>
Cap: %{customdata[2]:,.0f}<br>
Value: %{customdata[6]:,.0f}<br>
Trades: %{customdata[7]:,.0f}<br>
percentParent: %{percentParent:.2p}<br>
percentRoot: %{percentRoot:.2p}
<extra></extra>`;
      let data = [{
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
          t: 20,
          b: 20
        },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
      }

      var config = {
        responsive: true,
        displaylogo: false,
        displayModeBar: false,
        scrollZoom: true
      }
      Plotly.react('chart', data, layout, config);
    })
    .catch(function(error) {
      alert("Oops! There's no data. Please select another date.");
      console.error(error);
    });
}

function refreshHistogram() {
  var currency = document.getElementById('currencySelector').value;
  toggleInput();

  prepHistogramData()
    .then(function(chartData) {
      var layout = {
        showlegend: true,
        legend: {
          visible: true,
          traceorder: "normal",
          orientation: "h",
          x: 0,
          xanchor: "left",
          y: 0.89,
          yanchor: "top",
          bgcolor: 'rgba(65, 69, 84, 0)',
          bordercolor: 'rgba(65, 69, 84, 0)',
          borderwidth: 0,
        },
        updatemenus: [{
          type: 'buttons',
          buttons: [
            {
              label: 'Show/Hide Legend',
              method: 'relayout',
              args: [{ 'showlegend': true }],
              args2: [{ 'showlegend': false }]
            },
          ],
          direction: 'right',
          showactive: true,
          x: 0.02,
          xanchor: 'left',
          y: 1.0,
          yanchor: 'top',
          bgcolor: 'rgba(65, 69, 84, 1)',
          bordercolor: 'rgba(65, 69, 84, 1)',
          borderwidth: 0,
          font: {
            lineposition: 'none',
            color: 'black',
            size: 14,
            variant: 'all-small-caps'
          }
        }],
        yaxis: {
          visible: true,
          fixedrange: true,
          side: "right",
          showgrid: true,
        },
        yaxis2: {
          title: 'Currency Rate',
          overlaying: 'y',
          visible: false,
          fixedrange: true,
          side: 'left',
        },
        yaxis3: {
          title: 'Oil prices',
          overlaying: 'y',
          visible: false,
          fixedrange: true,
          side: 'left',
        },
        xaxis: {
          type: "date",
          fixedrange: false,
          // tickangle: -35,
          tickformatstops: [
            enabled = false,
            {
              dtickrange: [null, 'M1'],
              value: '%e\n%b %Y'
            },
            {
              dtickrange: ['M1', 'M12'],
              value: '%b\n%Y'
            },
            {
              dtickrange: ['M12', null],
              value: '%Y'
            }
          ],
          rangeslider: {
            visible: true,
          },
          rangeselector: {
            visible: true,
            activecolor: "#000000",
            bgcolor: "rgb(38, 38, 39)",
            buttons: [{
              step: 'month',
              stepmode: 'backward',
              count: 1,
              label: '1m'
            }, {
              step: 'month',
              stepmode: 'backward',
              count: 6,
              label: '6m'
            }, {
              step: 'year',
              stepmode: 'todate',
              count: 1,
              label: 'YTD'
            }, {
              step: 'year',
              stepmode: 'backward',
              count: 1,
              label: '1y'
            }, {
              step: 'all',
            }]
          },
          showgrid: true,
        },
        autosize: true,
        margin: {
          l: 0,
          r: 30,
          t: 0,
          b: 20
        },
        plot_bgcolor: "rgb(65, 69, 84)",
        paper_bgcolor: "rgb(65, 69, 85)",
        font: {
          family: "Arial",
          size: 12,
          color: "rgba(245, 246, 249, 1)"
        }
      }

      var config = {
        responsive: true,
        displaylogo: false,
        displayModeBar: true,
        modeBarButtonsToRemove: ['toImage', 'lasso2d', 'select2d'],
        scrollZoom: true
      }
      Plotly.react('chart', chartData, layout, config);
    })
    .catch(function(error) {
      console.error(error);
    });
}

async function loadData() {
  const totalSecurities = new Map();
  const today = new Date();
  const startDate = new Date('1994-01-01');

  for (let date = startDate; date <= today; date.setMonth(date.getMonth() + 1)) {
    const dateString = date.toISOString().slice(0, 7); // Format to 'YYYY-MM'
    totalSecurities.set(`${dateString}`, 0);
  }

  const newSecurities = new Map(totalSecurities);
  const delistedSecurities = new Map(totalSecurities);

  const response = await fetch(`data/securities-by-sector/moex.tsv?_=${new Date().toISOString().split('T')[0]}`);
  const data = await response.text();
  const rows = data.split('\n').slice(32);
  const excludeList = ["cb_bond", "corporate_bond", "etf_ppif",
                       "euro_bond", "exchange_bond", "exchange_ppif", "Foreign Companies",
                       "ifi_bond", "interval_ppif", "municipal_bond", "ofz_bond",
                       "private_ppif", "public_ppif", "state_bond", "stock_mortgage", "subfederal_bond"];

  rows.forEach(row => {
    const columns = row.split('\t');
    const parent = String(columns[0]);
    if (excludeList.includes(parent)) {
      return;
    }
    
    let historyFrom = columns[5];
    let historyTill = columns[6];
    if (historyFrom == undefined || historyTill == undefined) {
      return;
    }

    historyFrom = String(historyFrom).slice(0, 7);
    historyTill = String(historyTill).slice(0, 7);
    
    if (historyFrom !== '') {
      if (totalSecurities.has(historyFrom)) {
        totalSecurities.set(historyFrom, totalSecurities.get(historyFrom) + 1);
        newSecurities.set(historyFrom, newSecurities.get(historyFrom) + 1);
      } else {
        totalSecurities.set(historyFrom, 1);
        newSecurities.set(historyFrom, 1);
      }
    }

    if (historyTill !== '') {
      if (totalSecurities.has(historyTill)) {
        totalSecurities.set(historyTill, totalSecurities.get(historyTill) - 1);
        delistedSecurities.set(historyTill, delistedSecurities.get(historyTill) - 1);
      } else {
        totalSecurities.set(historyTill, -1);
        delistedSecurities.set(historyTill, -1);
      }
    }
  });

  const dates = Array.from(totalSecurities.keys());
  const values = Array.from(totalSecurities.values());

  return { dates, values };
}

async function refreshListings() {
  const { dates, values } = await loadData();

  const trace = {
    name: 'new/delisted securities',
    type: 'bar',
    x: dates,
    y: values,
    connector: { line: { color: 'rgb(63, 63, 63)' } },
    textposition: "outside",
    hoverinfo: "x+y+text+value",
    hovertemplate: '%{x|%x}<br>%{y}<extra></extra>',
    text: values.map(v => v > 0 ? '+' + v : v),
    marker: {
      color: values.map(value => value >= 0 ? 'green' : 'red'),
    },
    xaxis: 'x',
    yaxis: 'y2',
  };

  let total = [];
  let sum = 0;
  for (let i = 0; i < values.length; i++) {
    sum += values[i];
    total.push(sum);
  }
  const traceTotal = {
    name: 'total',
    type: 'bar',
    x: dates,
    y: total,
    connector: { line: { color: 'rgb(63, 63, 63)' } },
    textposition: "outside",
    hoverinfo: "x+y+text+value",
    text: total.map(v => v > 0 ? + v : v),
    marker: {
      color: 'blue',
    },
    xaxis: 'x',
    yaxis: 'y',
  };

  const layout = {
    grid: { rows: 1, columns: 1, pattern: 'independent' },
    // dragmode: false,
    showlegend: true,
    legend: {
      visible: true,
      traceorder: "normal",
      orientation: "h",
      x: 0,
      xanchor: "left",
      y: 0.89,
      yanchor: "bottom",
      bgcolor: 'rgba(0, 0, 0, 0)',
      bordercolor: 'rgba(0, 0, 0, 0)',
      borderwidth: 0,
    },
    xaxis: {
      type: "date",
      fixedrange: false,
      // tickangle: -35, // -90,
      // tickmode: "array",
      // tickformat: "%Y",
      // tickvals: tickvals,
      tickformatstops: [
        enabled = false,
        {
          dtickrange: [null, 'M1'],
          value: '%e\n%b %Y'
        },
        {
          dtickrange: ['M1', 'M12'],
          value: '%b\n%Y'
        },
        {
          dtickrange: ['M12', null],
          value: '%Y'
        }
      ],
      rangeslider: {
        visible: true,
      },
      rangeselector: {
        visible: true,
        activecolor: "#000000",
        bgcolor: "rgb(38, 38, 39)",
        buttons: [{
          step: 'month',
          stepmode: 'backward',
          count: 1,
          label: '1m'
        }, {
          step: 'month',
          stepmode: 'backward',
          count: 6,
          label: '6m'
        }, {
          step: 'year',
          stepmode: 'todate',
          count: 1,
          label: 'YTD'
        }, {
          step: 'year',
          stepmode: 'backward',
          count: 1,
          label: '1y'
        }, {
          step: 'all',
        }]
      }
    },
    yaxis: {
      visible: true,
      // title: 'total # of securities',
      range: [0, 500],
      side: 'right',
      domain: [0.175, 1.0],
      showgrid: false,
      fixedrange: true,
    },
    yaxis2: {
      visible: true,
      // title: '# of new/delisted',
      range: [-15, 70],
      domain: [0.0, 1.0],
      showgrid: false,
      fixedrange: true,
    },
    autosize: true,
    margin: {
      l: 0,
      r: 30,
      t: 0,
      b: 20
    },
    plot_bgcolor: "rgba(65, 69, 84, 0)",
    paper_bgcolor: "rgba(65, 69, 85, 0)",
    font: {
      family: "Arial",
      size: 12,
      color: "rgba(245, 246, 249, 1)"
    }
  };
  var config = {
    responsive: true,
    displaylogo: false,
    displayModeBar: true,
    modeBarButtonsToRemove: ['toImage', 'lasso2d', 'select2d'],
    scrollZoom: true
  }

  Plotly.react("chart", [traceTotal, trace], layout, config);
}

function refreshChart() {
  const chartType = document.getElementById("chartType").value;
  toggleInput();
  switch (chartType) {
    case "treemap":
      refreshTreemap();
      break;
    case "history":
      refreshHistogram();
      break;
    case "listings":
      refreshListings();
      break;
  }
};

refreshChart();

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("scripts/service-worker.js")
  });
}
